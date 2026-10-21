# -*- coding: utf-8 -*-
"""O portao de token abortou o render de um SHORT por causa da legenda do LONGO.

Medido em 21/10/2026 as 06:1x, no run `39554457072`: a concessao do Google do
`labtreinamento` perdeu o `youtube.force-ssl` (e ganhou `yt-analytics.readonly`),
e o `confere_token.py` abortou o render do `labtreinamento-s098` — **um short
solto** — com `ESCOPO FALTANDO ... enviar a faixa de legenda do longo`.

A peca nao tem longo e nao envia legenda nenhuma: no `publicar.py` a chamada de
`captions.insert` mora DENTRO do `if os.path.exists(longo)`. Logo o portao era
**MAIS SEVERO que o passo que ele guarda** — e esse defeito ja esta nomeado, em
letra, no docstring do proprio `token_do_canal` deste arquivo, para o outro eixo
(ler o REST quando o `publicar.py` le o ENV). Mesma forma, segundo eixo.

E a consequencia foi ATIVA, nao latente: com **256** das 396 specs do disco
sendo short solto, isso parava a linha inteira por um escopo que a publicacao
delas nao usa.

O que este arquivo NAO permite e afrouxar: pacote COM longo continua abortando,
e a contraprova vai nos dois sentidos.
"""
import ast
import glob
import importlib.util
import json
import re
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
FORCE_SSL = "https://www.googleapis.com/auth/youtube.force-ssl"
UPLOAD = "https://www.googleapis.com/auth/youtube.upload"


def _mod(nome):
    spec = importlib.util.spec_from_file_location(
        nome, RAIZ / "fabrica" / ("%s.py" % nome))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


CT = _mod("confere_token")
FP = _mod("formato_da_peca")


def _specs():
    """Varredura do DISCO: os dois lados tem de existir de verdade."""
    curtas, pacotes = [], []
    for p in sorted(glob.glob(str(RAIZ / "fabrica" / "specs" / "*.json"))):
        try:
            sp = json.loads(Path(p).read_text(encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(sp, dict):
            continue
        (pacotes if sp.get("longo") else curtas).append(sp)
    return curtas, pacotes


def test_a_varredura_nao_passa_por_VACUIDADE():
    curtas, pacotes = _specs()
    assert len(curtas) + len(pacotes) >= 200, (
        "menos de 200 specs lidas (%d) — a varredura quebrou, e um arquivo que "
        "varre nada passa verde" % (len(curtas) + len(pacotes)))


def test_os_DOIS_lados_existem_no_disco():
    """Se o acervo virar de um formato so, esta nota se rele em vez de ficar.

    Ela existe porque os dois formatos convivem: o conjunto de escopos depende
    disso. Com um lado vazio o arquivo mediria uma distincao que nao existe.
    """
    curtas, pacotes = _specs()
    assert len(curtas) >= 50 and len(pacotes) >= 20, (
        "short solto=%d, pacote=%d — um dos lados praticamente desapareceu"
        % (len(curtas), len(pacotes)))


def test_o_short_solto_NAO_precisa_do_escopo_da_legenda():
    """A pergunta e feita ao DONO, nao reimplementada aqui."""
    curtas, _ = _specs()
    sp = curtas[0]
    preciso = CT.escopos_necessarios(sp)
    assert UPLOAD in preciso, "short solto tem de exigir videos.insert"
    assert FORCE_SSL not in preciso, (
        "short solto ainda exige o escopo da legenda; foi isso que abortou o "
        "run 39554457072")


def test_o_pacote_COM_longo_continua_exigindo_os_DOIS():
    """Contraprova no outro sentido: sem ela bastaria devolver sempre um escopo.

    Longo sem legenda e longo mudo para a busca (aprendizado 93), e publicacao
    nao se desfaz — este lado NAO afrouxa.
    """
    _, pacotes = _specs()
    preciso = CT.escopos_necessarios(pacotes[0])
    assert FORCE_SSL in preciso and UPLOAD in preciso, preciso


def test_spec_AUSENTE_cai_no_conjunto_ESTRITO():
    """Nao saber que peca e nao e licenca para ser permissivo.

    E assim que o `diagnostico.yml` chama este arquivo: sem spec.
    """
    assert CT.escopos_necessarios(None) == dict(CT.ESCOPOS_NECESSARIOS)
    assert FORCE_SSL in CT.escopos_necessarios(None)


def test_captions_insert_mora_DENTRO_do_if_do_longo():
    """A PROVA de que o short nao envia legenda sai do `publicar.py`, por AST.

    Sem isto, "o short nao usa force-ssl" seria afirmacao minha. O docstring
    deste arquivo CITA `captions.insert` em prosa, logo casar texto pegaria a
    explicacao em vez do codigo (a licao do `test_NAO_virou_portao` do acento).
    """
    fonte = (RAIZ / "fabrica" / "publicar.py").read_text(encoding="utf-8")
    arvore = ast.parse(fonte)

    def chamadas_de_legenda(no):
        return [c for c in ast.walk(no)
                if isinstance(c, ast.Call) and isinstance(c.func, ast.Name)
                and c.func.id == "legenda"]

    todas = chamadas_de_legenda(arvore)
    assert todas, ("nenhuma chamada a `legenda()` no publicar.py — o nome mudou "
                   "e esta prova passou a nao medir nada")
    guardadas = []
    for no in ast.walk(arvore):
        if isinstance(no, ast.If) and "longo" in ast.unparse(no.test):
            guardadas.extend(chamadas_de_legenda(no))
    fora = [c for c in todas if not any(c is g for g in guardadas)]
    assert not fora, (
        "ha chamada de captions.insert FORA do ramo do longo (linhas %s) — "
        "se o short passou a enviar legenda, ele volta a precisar de force-ssl "
        "e esta nota tem de ser relida" % [c.lineno for c in fora])


def test_o_portao_NOMEIA_o_escopo_que_falta_em_vez_de_calar():
    """O short passa, E o relato diz que o PACOTE segue abortado neste canal.

    Filtrar em silencio faria a rodada seguinte descobrir por render abortado,
    que e justamente o que custou esta. E a disciplina do `origens_sem_uso`:
    nomear em vez de esconder.
    """
    fonte = (RAIZ / "fabrica" / "confere_token.py").read_text(encoding="utf-8")
    corpo = ast.parse(fonte)
    main = next(n for n in ast.walk(corpo)
                if isinstance(n, ast.FunctionDef) and n.name == "main")
    texto = ast.unparse(main)
    assert "ESCOPO_LEGENDA not in concedidos" in texto, (
        "o `main` deixou de conferir o escopo que ESTA peca nao usa; o aviso "
        "sobre o pacote desaparece com ele")
    assert "::warning" in texto and "force-ssl" in texto, (
        "o aviso saiu do relato, ou deixou de dizer qual escopo falta")


def test_o_render_e_o_PORTAO_leem_a_MESMA_funcao():
    """Os dois que decidem o que a peca publica tem de responder igual.

    O `etapas.py` escolhe o caminho de render e o `confere_token.py` escolhe o
    escopo exigido. Se um deles achar que ha longo e o outro nao, a peca sobe
    sem legenda com portao verde — que e a forma do defeito de 20/08.
    """
    for arquivo, alvo in (("etapas.py", "formato_da_peca"),
                          ("confere_token.py", "formato_da_peca")):
        fonte = (RAIZ / "fabrica" / arquivo).read_text(encoding="utf-8")
        arvore = ast.parse(fonte)
        importa = any(
            (isinstance(n, ast.Import) and any(a.name == alvo for a in n.names))
            or (isinstance(n, ast.ImportFrom) and n.module == alvo)
            for n in ast.walk(arvore))
        assert importa, "%s nao importa o %s" % (arquivo, alvo)
        assert re.search(r"(FP|formato_da_peca)\.(so_short|tem_longo)\(", fonte), (
            "%s importa o dono e nao o CHAMA — import sem chamada e a classe "
            "dos layouts mortos" % arquivo)


def test_o_workflow_PASSA_a_spec_ao_portao():
    """O defeito era de CHAMADOR: sem a spec o portao usa o conjunto estrito."""
    yml = (RAIZ / ".github" / "workflows" / "frota.yml").read_text(
        encoding="utf-8")
    linha = [l for l in yml.splitlines() if "confere_token.py" in l
             and l.strip().startswith("run:")]
    assert linha, "o passo que chama o confere_token desapareceu do frota.yml"
    assert "spec.json" in linha[0], (
        "o frota.yml voltou a chamar o portao SEM a spec, e ai ele aborta todo "
        "short solto quando falta o escopo da legenda: %s" % linha[0])


def test_a_CONTAGEM_dos_ramos_e_reconferida_contra_o_disco():
    """O modulo declara 20 ramos em 12 modulos e 23 defaults — numero que
    envelhece calado se ninguem o reconferir (753).

    Ele existe para dizer, em letra, que "UM dono" NAO vale na escala da frota:
    este arquivo e dono dos dois que decidem o que a peca publica, e os outros
    ramos seguem respondendo sozinhos.
    """
    def folha(n):
        return (isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                and n.func.attr == "get" and n.args
                and isinstance(n.args[0], ast.Constant)
                and n.args[0].value == "longo")

    ramos, modulos = 0, set()
    for p in sorted(glob.glob(str(RAIZ / "fabrica" / "*.py"))):
        try:
            arvore = ast.parse(Path(p).read_text(encoding="utf-8"))
        except SyntaxError:
            continue
        for no in ast.walk(arvore):
            testes = []
            if isinstance(no, (ast.If, ast.IfExp)):
                testes = [no.test]
            elif isinstance(no, ast.UnaryOp) and isinstance(no.op, ast.Not):
                testes = [no.operand]
            elif (isinstance(no, ast.Call) and isinstance(no.func, ast.Name)
                  and no.func.id == "bool"):
                testes = no.args
            elif isinstance(no, ast.Assert):
                testes = [no.test]
            for t in testes:
                if any(folha(s) for s in ast.walk(t)):
                    ramos += 1
                    modulos.add(Path(p).name)
    fonte = (RAIZ / "fabrica" / "formato_da_peca.py").read_text(encoding="utf-8")
    assert "**20**" in fonte and "**12**" in fonte, (
        "a medida dos ramos saiu do modulo; sem ela a promessa de 'UM dono' "
        "volta a parecer verdadeira")
    assert abs(ramos - 20) <= 3 and abs(len(modulos) - 12) <= 2, (
        "a contagem de ramos mudou (%d ramos em %d modulos contra 20 em 12 "
        "escritos no modulo) — releia a divida em vez de mover o numero"
        % (ramos, len(modulos)))


def test_o_motivo_continua_escrito_nos_DOIS_modulos():
    """Conserto sem motivo escrito volta calado."""
    ct = (RAIZ / "fabrica" / "confere_token.py").read_text(encoding="utf-8")
    fp = (RAIZ / "fabrica" / "formato_da_peca.py").read_text(encoding="utf-8")
    assert "MAIS SEVERO" in ct and "captions.insert" in ct, (
        "o `confere_token` perdeu a razao de o conjunto depender do formato")
    assert "39554457072" in ct, (
        "o run que mediu o defeito saiu do modulo; procedencia ausente convida "
        "a readotar o conjunto estrito 'por seguranca'")
    assert "256" in fp and "140" in fp, (
        "a medida do disco (256 short solto contra 140 pacote) saiu do dono")
