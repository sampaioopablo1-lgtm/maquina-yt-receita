#!/usr/bin/env python3
"""O parque de duracao nao carregava o FORMATO, e a segunda metade do pedido do
dono (um LONGO e um CURTO por canal por dia) nao tinha dono.

MEDIDO em 23/10 as 21:3x. O `do_registro` copiava `pacote`, `canal`,
`youtube_id`, `em` e `cenas` do registro do notice e **jogava fora o `formato` e
o `slug`** — os dois unicos campos que distinguem o LONGO do SHORT de um pacote.
E o `pacote` nao serve de chave: os tres pacotes de 19/10 estao como
`<pacote>-longo` e os de 22/10 em diante tem o MESMO `pacote` duas vezes.

O que este arquivo cobra e PROPRIEDADE e nao identidade (743/753/761): nenhum
assert depende de um pacote, de um id nem de uma contagem absoluta — o acervo
cresce uma peca por rodada, e contagem absoluta sobre populacao que cresce e
identidade disfarcada de medida (a licao de 22/10 as 14:4x).
"""
import ast
import inspect
import json
import os
import re
import sys
import textwrap

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import canal as CA                      # noqa: E402
import duracao_a_medir as DM            # noqa: E402
import longo_por_canal as LC            # noqa: E402

SQL = os.path.join(RAIZ, "docs", "pendente", "videos-a-inserir.sql")

# HISTORIA: a medicao que me fez quase relatar um defeito que nao existe. Nenhum
# assert depende destes numeros — o que se cobra e a PROPRIEDADE de os dois
# modos de contar divergirem.
MEDIDA_DE_21H = {"tuplas": 211, "longos": 6, "linhas_insert": 205,
                 "indeterminadas_reparadas": 9}

PISO_DE_VACUIDADE = 100


def _fonte(fn):
    return textwrap.dedent(inspect.getsource(fn))


def _corpo(fn):
    """A fonte SEM o docstring — os modulos CITAM a forma proibida na prosa que
    os explica, e casar prosa pega a explicacao em vez do codigo (a licao do
    `test_NAO_virou_portao` do acento)."""
    arv = ast.parse(_fonte(fn))
    f = arv.body[0]
    corpo = f.body[1:] if (f.body and isinstance(f.body[0], ast.Expr)
                           and isinstance(f.body[0].value, ast.Constant)
                           and isinstance(f.body[0].value.value, str)) else f.body
    return "\n".join(ast.unparse(n) for n in corpo)


def _parque(tmp, linhas):
    cam = os.path.join(str(tmp), "duracoes.jsonl")
    with open(cam, "w", encoding="utf-8") as f:
        for r in linhas:
            f.write(json.dumps(r, ensure_ascii=False, sort_keys=True) + "\n")
    return cam


def _linha(pacote, yid, em, **extra):
    r = {"pacote": pacote, "youtube_id": yid, "em": em,
         "prev_edge": 41.5, "prev_piper": 35.0, "provedor": "edge",
         "job": "1"}
    r.update(extra)
    return r


# ---------------------------------------------------------------- o DISCO

def test_o_parque_do_disco_sabe_o_formato_de_TODA_peca():
    regs = DM.carrega()
    assert len(regs) >= PISO_DE_VACUIDADE, (
        "parque com %d linhas: abaixo deste piso 'nenhuma sem formato' nao mede "
        "nada" % len(regs))
    sem = [r["pacote"] for r in regs if DM.formato(r) is None]
    assert not sem, (
        "estas peças nao sabem o proprio formato: %s. Reparar com o valor LIDO "
        "do dono (o `videos-a-inserir.sql`), nunca inferir por `cenas` nem pela "
        "previsao — isso e o 733." % sem[:8])


def test_os_DOIS_formatos_existem_no_disco():
    """Sem os dois lados, `formato` nao distingue nada e este arquivo passa por
    vacuidade."""
    fs = {DM.formato(r) for r in DM.carrega()}
    assert "longo" in fs, (
        "nenhum LONGO no parque: a pergunta do dono perde o objeto e esta nota "
        "tem de ser RELIDA, nao o numero movido")
    assert "shorts" in fs, "nenhum SHORT no parque — varredura quebrada"


def test_as_DUAS_convencoes_de_pacote_existem_e_DIVERGEM():
    """A razao de o `pacote` nao servir de chave. Se elas convergirem, o defeito
    perdeu o objeto e isto se rele."""
    pacs = [r["pacote"] for r in DM.carrega()]
    com_sufixo = [p for p in pacs if p.endswith("-longo")]
    import collections
    rep = [p for p, n in collections.Counter(pacs).items() if n > 1]
    assert com_sufixo, (
        "nenhum `<pacote>-longo` no parque — a primeira convencao desapareceu e "
        "esta nota tem de ser relida")
    assert rep, (
        "nenhum `pacote` repetido no parque — a segunda convencao desapareceu e "
        "esta nota tem de ser relida")


def test_a_contagem_por_LINHA_e_por_TUPLA_do_SQL_DIVERGEM():
    """O defeito do meu proprio parser, RECONFERIDO contra o disco: foi a
    contagem por LINHA que me disse 'zero longos'. Propriedade, nao numero."""
    txt = open(SQL, encoding="utf-8").read()
    linhas = [l for l in txt.splitlines() if l.startswith("insert into videos")]
    tup = re.findall(r"\('([^']*)','publicado','([^']*)'", txt)
    assert len(linhas) >= PISO_DE_VACUIDADE, "SQL curto demais para medir"
    assert len(tup) > len(linhas), (
        "as duas contagens coincidem (%d tuplas, %d linhas): o pacote escreve "
        "UMA linha com DUAS tuplas, logo se elas coincidem nao ha pacote no "
        "arquivo e esta nota se rele" % (len(tup), len(linhas)))
    assert any(f == "longo" for _, f in tup), (
        "nenhuma tupla de formato `longo` no SQL do dono — era isto que o meu "
        "parser dizia, e era FALSO")


# ------------------------------------------------- o `formato` e a RECUSA

def test_formato_devolve_o_CAMPO_quando_ele_existe():
    assert DM.formato({"pacote": "x-021", "formato": "longo"}) == "longo"
    assert DM.formato({"pacote": "x-021", "formato": "shorts"}) == "shorts"


def test_formato_DERIVA_so_das_duas_convencoes_escritas():
    assert DM.formato({"pacote": "canalx-068-longo"}) == "longo"
    assert DM.formato({"pacote": "canalx-s104"}) == "shorts"


def test_formato_RECUSA_em_vez_de_palpitar():
    """Pacote nu sem o campo e INDETERMINADO — e `None` aqui e recusa."""
    assert DM.formato({"pacote": "canalx-021"}) is None
    assert DM.formato({"pacote": "canalx-021", "cenas": 64}) is None
    assert DM.formato({"pacote": "canalx-021", "prev_edge": 653.5}) is None
    assert DM.formato({"pacote": "canalx-021", "formato": "LONGO "}) is None


def test_formato_NAO_pode_inferir_por_cenas_nem_por_previsao():
    corpo = _corpo(DM.formato)
    for proibido in ("cenas", "prev_edge", "prev_piper"):
        assert proibido not in corpo, (
            "`formato` le %r: inferir o formato por aqui e o 733, que me custou "
            "tres rodadas inferindo o provedor pela distancia entre previsao e "
            "real" % proibido)


def test_o_do_registro_DESCE_o_formato_e_o_slug_do_dono():
    corpo = _corpo(DM.do_registro)
    for campo in ("formato", "slug"):
        assert ('reg_videos.get(%r)' % campo) in corpo.replace('"', "'"), (
            "o `do_registro` nao desce %r do dono — era este descarte o defeito"
            % campo)
    assert "-short" not in corpo and "endswith" not in corpo, (
        "o `do_registro` esta RECOMPUTANDO o formato: ele tem UM dono, o "
        "`registro_videos.linhas_dos_notices`, e recomputar aqui cria o segundo")


def _pacote_do_disco():
    """Um PACOTE real (spec com `longo` e `short`), DERIVADO do disco.

    O dono do notice ABRE a spec, logo pacote inventado nao resolve e o teste
    passaria por vacuidade — e nomear um pacote aqui seria identidade onde ha
    propriedade (743/753/761), com o acervo crescendo a cada rodada."""
    import glob
    for cam in sorted(glob.glob(os.path.join(RAIZ, "fabrica", "specs",
                                             "*.json"))):
        try:
            d = json.load(open(cam, encoding="utf-8"))
        except Exception:
            continue
        if d.get("longo") and d.get("short"):
            return os.path.basename(cam)[:-5]
    return None


def test_a_peca_que_passa_pelo_dono_sai_com_formato():
    """O caminho INTEIRO: notice -> `linhas_dos_notices` -> `do_registro`."""
    import registro_videos as RV
    pac = _pacote_do_disco()
    if not pac:
        pytest.fail("perdi a ancora: nenhuma spec do disco tem `longo` E "
                    "`short`, logo este teste nao mede o caminho do PACOTE")
    regs = RV.linhas_dos_notices(
        "PUBLICADO %s shorts youtube_id=aaaaaaaaaaa titulo=T "
        "em=2026-10-23T10:00:00Z\n"
        "PUBLICADO %s longo youtube_id=bbbbbbbbbbb titulo=L "
        "em=2026-10-23T10:00:00Z" % (pac, pac))
    assert len(regs) == 2
    vistos = set()
    for r in regs:
        par = (619.0, 540.0) if r.get("formato") == "longo" else (41.5, 35.0)
        linha = DM.do_registro(r, par[0], par[1], "edge", "1")
        f = DM.formato(linha)
        assert f is not None, "a peca passou pelo dono e saiu SEM formato"
        vistos.add(f)
    assert vistos == {"longo", "shorts"}, vistos


# ------------------------------------------------------- o QUADRO e o VAO

def test_canal_sem_longo_sai_com_vao_None_e_NUNCA(tmp_path):
    cam = _parque(tmp_path, [
        _linha("kolejny-poziom-s001", "a" * 11, "2026-10-23T10:00:00Z"),
        _linha("labtreinamento-010-longo", "b" * 11, "2026-10-22T10:00:00Z"),
        _linha("epomeno-epipedo-s001", "c" * 11, "2026-10-23T09:00:00Z"),
    ])
    q = LC.quadro(agora="2026-10-23T12:00:00", caminho=cam)
    assert q["canais"]["kolejny-poziom"]["vao_h"] is None
    assert q["canais"]["kolejny-poziom"]["n_longos"] == 0
    assert "kolejny-poziom" in q["nunca"] and "epomeno-epipedo" in q["nunca"]
    # contraprova no outro sentido: o canal COM longo tem vao finito e positivo
    v = q["canais"]["labtreinamento"]["vao_h"]
    assert v is not None and v > 0, v
    assert q["canais"]["labtreinamento"]["n_longos"] == 1


def test_o_MAIOR_vao_e_o_canal_que_esta_ha_mais_tempo_sem_longo(tmp_path):
    cam = _parque(tmp_path, [
        _linha("labtreinamento-010-longo", "a" * 11, "2026-10-23T10:00:00Z"),
        _linha("epomeno-epipedo-010-longo", "b" * 11, "2026-10-20T10:00:00Z"),
        _linha("kolejny-poziom-010-longo", "c" * 11, "2026-10-22T10:00:00Z"),
    ])
    q = LC.quadro(agora="2026-10-23T12:00:00", caminho=cam)
    assert q["mais_antigo"] == "epomeno-epipedo", q["mais_antigo"]
    assert not q["nunca"]
    # e canal SEM longo nenhum vence qualquer vao finito
    cam2 = _parque(tmp_path, [
        _linha("labtreinamento-010-longo", "a" * 11, "2020-01-01T10:00:00Z"),
        _linha("kolejny-poziom-s001", "c" * 11, "2026-10-23T10:00:00Z"),
    ])
    q2 = LC.quadro(agora="2026-10-23T12:00:00", caminho=cam2)
    assert q2["mais_antigo"] in q2["nunca"], (
        "um vao de anos venceu um canal com ZERO longos — zero e o caso "
        "extremo, nao a ausencia de dado")


def test_a_janela_tem_limite_de_CIMA(tmp_path):
    """Sem ele, instante no FUTURO conta — o defeito medido em 20/10 as 13:2x no
    irmao `concentracao_frota`."""
    cam = _parque(tmp_path, [
        _linha("kolejny-poziom-010-longo", "a" * 11, "2026-10-23T10:00:00Z"),
        _linha("kolejny-poziom-011-longo", "b" * 11, "2026-10-24T10:00:00Z"),
        _linha("kolejny-poziom-012-longo", "c" * 11, "2026-10-01T10:00:00Z"),
    ])
    j = LC.na_janela(24.0, agora="2026-10-23T12:00:00", caminho=cam)
    assert j["kolejny-poziom"]["longo"] == 1, (
        "a janela contou %d longos: ou o futuro entrou, ou o limite de baixo "
        "vazou" % j["kolejny-poziom"]["longo"])


def test_o_CANAL_sai_do_dono_e_nao_do_campo(tmp_path):
    """57 das 169 linhas do parque nao tem o campo `canal`: ler o campo
    perderia essas peças em silencio."""
    cam = _parque(tmp_path, [
        _linha("kolejny-poziom-010-longo", "a" * 11, "2026-10-23T10:00:00Z"),
    ])
    q = LC.quadro(agora="2026-10-23T12:00:00", caminho=cam)
    assert q["canais"]["kolejny-poziom"]["n_longos"] == 1, (
        "registro SEM o campo `canal` nao foi atribuido — o canal tem de sair "
        "do `canal.do_pacote`")
    corpo = _corpo(LC.pecas)
    assert 'r.get("canal")' not in corpo and "r.get('canal')" not in corpo, (
        "o `pecas` le o campo `canal` da linha em vez de o derivar")
    assert "CA.do_pacote" in corpo


def test_a_peca_sem_formato_sai_NOMEADA_e_nao_contada_como_short(tmp_path):
    cam = _parque(tmp_path, [
        _linha("kolejny-poziom-021", "a" * 11, "2026-10-23T10:00:00Z"),
        _linha("kolejny-poziom-s001", "b" * 11, "2026-10-23T11:00:00Z"),
    ])
    sf = LC.sem_formato(cam)
    assert [p["youtube_id"] for p in sf] == ["a" * 11], sf
    j = LC.na_janela(24.0, agora="2026-10-23T12:00:00", caminho=cam)
    assert j["kolejny-poziom"] == {"longo": 0, "shorts": 1}, (
        "a peca de formato DESCONHECIDO entrou numa das contagens: supor o "
        "formato aqui e o 733 em forma de contagem")
    r = LC.relato(agora="2026-10-23T12:00:00", caminho=cam)
    assert "SEM FORMATO" in r and "a" * 11 in r, r


# ------------------------------------------------------- forma do relato

def test_a_frase_do_vao_tem_UM_dono_e_sai_nos_TRES_ramos(tmp_path):
    arv = ast.parse(open(LC.__file__, encoding="utf-8").read())
    donos = []
    for n in ast.walk(arv):
        if isinstance(n, ast.FunctionDef):
            corpo = "\n".join(ast.unparse(x) for x in n.body)
            if "NUNCA publicou longo" in corpo or "ultimo longo" in corpo:
                donos.append(n.name)
    assert donos == ["_linha_do_vao"], (
        "a frase do vao tem %d donos (%s) — duas copias divergem em horas, "
        "como a linha do PUBLICADO divergiu do veredito em 23/10 as 14:4x"
        % (len(donos), donos))

    # OS TRES RAMOS NAO COEXISTEM na mesma fixture, e isso e propriedade do
    # modulo: canal sem longo nenhum VENCE qualquer vao finito, logo o ramo do
    # MAIOR VAO so se ve quando os tres canais tem longo. Duas fixturas.
    cam = _parque(tmp_path, [
        _linha("labtreinamento-010-longo", "a" * 11, "2026-10-23T10:00:00Z"),
        _linha("epomeno-epipedo-010-longo", "b" * 11, "2026-10-20T10:00:00Z"),
        _linha("kolejny-poziom-s001", "c" * 11, "2026-10-23T11:00:00Z"),
    ])
    r = LC.relato(agora="2026-10-23T12:00:00", caminho=cam)
    assert "NUNCA publicou longo" in r          # ramo 1
    assert "ultimo longo" in r                  # ramo 2

    cam2 = _parque(tmp_path, [
        _linha("labtreinamento-010-longo", "a" * 11, "2026-10-23T10:00:00Z"),
        _linha("epomeno-epipedo-010-longo", "b" * 11, "2026-10-20T10:00:00Z"),
        _linha("kolejny-poziom-010-longo", "c" * 11, "2026-10-22T10:00:00Z"),
    ])
    r2 = LC.relato(agora="2026-10-23T12:00:00", caminho=cam2)
    assert "MAIOR VAO" in r2                    # ramo 3
    assert "NUNCA publicou longo" not in r2, (
        "o ramo do NUNCA disparou num parque em que os tres tem longo")
    # e o ramo do MAIOR VAO nao pode marcar mais de um canal
    assert r2.count("MAIOR VAO") == 1, r2


def test_o_relato_NAO_decide_o_canal():
    """A escolha e do `passo_zero`/`concentracao_frota`. Portao aqui mudaria a
    regra de producao, que e parametro do DONO (§10)."""
    r = LC.relato()
    assert "NOMEIA e NAO decide" in r
    assert LC.main(["longo_por_canal.py"]) == 0


def test_o_MOTIVO_e_a_RETRATACAO_continuam_escritos():
    fonte = open(LC.__file__, encoding="utf-8").read()
    assert "18:4x" in fonte, (
        "a procedencia (o laco escrito na mao de 23/10 as 18:4x) saiu do modulo")
    assert "falso" in fonte.lower() and "211" in fonte, (
        "a retratacao da minha contagem por LINHA saiu do modulo — sem ela a "
        "rodada seguinte repete o `grep -c 'insert into videos'`")


def test_o_passo_zero_CHAMA_o_instrumento():
    """Import sem chamada e a classe dos layouts mortos: o `irmaos_da_origem`
    passou cinco dias sem chamador nenhum fora do teste dele (20/10, 08:2x)."""
    import passo_zero as PZ
    arv = ast.parse(open(PZ.__file__, encoding="utf-8").read())
    chama = False
    for n in ast.walk(arv):
        if (isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
                and isinstance(n.func.value, ast.Name)
                and n.func.value.id == "longo_por_canal"):
            chama = True
    assert chama, "o `passo_zero` importa o `longo_por_canal` e nao o chama"
    texto = PZ.relato(modo_da_rota="negado_por_politica")
    assert "LONGO POR CANAL" in texto
    assert "o DONO pediu ao menos UM longo e UM curto" in texto


def test_o_passo_zero_NAO_recomputa_o_formato():
    """A conta tem UM dono. Recomputar aqui e a assinatura que congelou a
    legenda."""
    import passo_zero as PZ
    fonte = open(PZ.__file__, encoding="utf-8").read()
    arv = ast.parse(fonte)
    for n in ast.walk(arv):
        if isinstance(n, ast.FunctionDef):
            corpo = "\n".join(ast.unparse(x) for x in n.body)
            assert "-longo" not in corpo, (
                "o `passo_zero` deriva formato por conta propria em %s" % n.name)
