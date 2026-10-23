# -*- coding: utf-8 -*-
"""O cruzamento do titulo chaveava por PACOTE, e um pacote emite DOIS notices.

**FALSO POSITIVO MEDIDO em 23/10 as 13:5x, no PRIMEIRO pacote desde que o
`divergencia_de_titulo` nasceu** (08:4x do mesmo dia, visto so em short solto).
Um pacote publica longo e short com o MESMO `pacote` e `youtube_id` diferentes;
o dicionario chaveado por pacote guardava o ULTIMO notice e comparava a linha do
SHORT contra o titulo do LONGO.

O custo nao foi de relato: o `registro_da_rodada` LEVANTA nessa divergencia,
logo os quatro parques nao foram escritos e a rodada quase relatou ao dono que a
maquina havia subido o short com o titulo do longo — quando os notices crus
dizem o contrario. **Detector que inventa achado e pior que nao ter detector
(725), e os meus deram falso positivo na primeira execucao varias vezes.**

A forma dos testes: a fixture REPRODUZ o caso (dois notices, mesmo pacote), a
contraprova vai nos DOIS sentidos (divergencia de verdade continua acusada, e
short solto continua funcionando), e o caso real de 23/10 fica como HISTORIA sem
nenhum assert dependendo dele (743/753/761).
"""
import ast
import inspect
import os
import sys
import textwrap

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import anotacoes_do_run as AR  # noqa: E402

# HISTORIA: o pacote e os dois ids do caso medido. Nenhum assert depende deles
# — os ids mudam a cada publicacao, e cravar um seria identidade onde ha
# propriedade.
CASO_DE_13H = {
    "pacote": "epomeno-epipedo-069",
    "short": "D07pVhb6Qrc",
    "longo": "e_irNzHj1jc",
}

T_LONGO = "O Fakelos ton Exi Erotiseon: Poio Charti Apanta Ti"
T_SHORT = "Ena charti, mia erotisi"


def _notice(pac, formato, yid, titulo):
    return ("PUBLICADO %s %s youtube_id=%s titulo=%s em=2026-10-23T13:46:14Z"
            % (pac, formato, yid, titulo))


def _lida(mensagens):
    return {"run": "1", "jobs": [{"id": "9", "nome": "retomar",
                                  "conclusao": "success",
                                  "mensagens": list(mensagens)}]}


def _ancora_pacote():
    """Um PACOTE do disco, DERIVADO: `longo` cheio e `## TITULO SHORT` na copy.

    Nomear um pacote seria identidade onde ha propriedade (743/753/761) — e o
    `linhas_dos_notices` ABRE a spec, logo pacote inventado some da leitura e o
    arquivo passaria por vacuidade.
    """
    import glob
    import json
    import registro_videos as RV
    for f in sorted(glob.glob(os.path.join(RAIZ, "fabrica", "specs",
                                           "*.json"))):
        try:
            sp = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        if not sp.get("longo") or not sp.get("short"):
            continue
        ts = RV.titulo_short(sp)
        if ts:
            return os.path.basename(f)[:-5], ts
    pytest.fail(
        "nenhum PACOTE do disco tem `longo`, `short` e `## TITULO SHORT` —"
        " perdi a ancora, e sem ela este arquivo nao mede o defeito")


def _pacote(t_short=None, t_longo=T_LONGO):
    """Um pacote de verdade: DOIS notices com o MESMO `pacote`.

    O titulo do SHORT no notice vem, por padrao, do titulo que a propria SPEC
    declara — e e assim que as duas leituras CONCORDAM peca por peca, que e o
    caso em que a chave por pacote acusava sem motivo.
    """
    pac, ts = _ancora_pacote()
    return _lida([
        _notice(pac, "shorts", "AAAAAAAAAAA", ts if t_short is None else t_short),
        _notice(pac, "longo", "BBBBBBBBBBB", t_longo),
    ])


def _ancora_solto():
    import glob
    import json
    import registro_videos as RV
    for f in sorted(glob.glob(os.path.join(RAIZ, "fabrica", "specs",
                                           "*.json"))):
        try:
            sp = json.load(open(f, encoding="utf-8"))
        except Exception:
            continue
        if sp.get("longo") or not sp.get("short"):
            continue
        ts = RV.titulo_short(sp)
        if ts:
            return os.path.basename(f)[:-5], ts
    pytest.fail("nenhum short SOLTO com titulo proprio no disco: perdi a ancora")


def _solto(titulo=None):
    pac, ts = _ancora_solto()
    return _lida([_notice(pac, "shorts", "CCCCCCCCCCC",
                          ts if titulo is None else titulo)])


def _fonte(fn):
    return textwrap.dedent(inspect.getsource(fn))


def _corpo_sem_docstring(fn):
    f = ast.parse(_fonte(fn)).body[0]
    corpo = f.body
    if (corpo and isinstance(corpo[0], ast.Expr)
            and isinstance(corpo[0].value, ast.Constant)
            and isinstance(corpo[0].value.value, str)):
        corpo = corpo[1:]
    return ast.Module(body=corpo, type_ignores=[])


def test_a_fixture_REPRODUZ_o_caso_dois_notices_um_pacote():
    """Sem os dois notices no MESMO pacote o arquivo nao mede nada."""
    d = AR.publicado(_pacote())
    assert len(d) == 2, "a fixture deixou de emitir duas pecas"
    assert len({x["pacote"] for x in d}) == 1, (
        "as duas pecas tem de ter o MESMO pacote — e isso que produz o defeito")
    assert len({x["youtube_id"] for x in d}) == 2, (
        "os youtube_id tem de ser distintos, senao nao ha o que chavear")


def test_a_CHAVE_por_pacote_de_fato_ACUSAVA_e_a_por_id_nao():
    """Sem este par, *"eu errei a chave"* seria afirmacao minha e nao medida."""
    lida = _pacote()
    texto = "\n".join(m for j in lida["jobs"] for m in j["mensagens"])
    import corpus_atrasado as CA
    por_pacote = {p: t for p, _y, t in CA.titulos_dos_notices(texto)}
    antigos = [ln for ln in AR.publicado(lida)
               if (ln.get("titulo") or "").strip()
               != (por_pacote.get(ln.get("pacote")) or "").strip()]
    assert antigos, (
        "a chave por PACOTE parou de acusar nesta fixture — o defeito nao se"
        " reproduz e esta nota tem de ser RELIDA")
    d = AR.divergencia_de_titulo(lida)
    assert d["divergentes"] == [], (
        "a chave nova ainda acusa um pacote cujos titulos CONCORDAM peca por"
        " peca: %s" % d["divergentes"])


def test_as_DUAS_pecas_do_pacote_sao_PAREADAS():
    d = AR.divergencia_de_titulo(_pacote())
    assert d["pares"] == 2, (
        "o pacote tem duas pecas e o cruzamento pareou %d — com uma, metade do"
        " pacote fica sem testemunha" % d["pares"])


def test_contraprova_divergencia_de_VERDADE_continua_acusada():
    """Senao chavear por id seria so uma forma de nunca acusar."""
    lida = _pacote(t_short="UM TITULO QUE A LINHA NAO TEM")
    d = AR.divergencia_de_titulo(lida)
    assert len(d["divergentes"]) == 1, (
        "o cruzamento deixou de acusar divergencia real: %s" % d)
    x = d["divergentes"][0]
    assert x["do_notice"] == "UM TITULO QUE A LINHA NAO TEM"
    assert x["da_linha"] != x["do_notice"]
    assert x.get("youtube_id"), (
        "a acusacao tem de nomear a PECA: com o pacote so, um pacote de duas"
        " pecas nao diz qual das duas")


def test_o_lado_do_LONGO_e_VACUO_e_isso_vai_DITO():
    """**Este teste e uma RETRATACAO de um assert meu da primeira versao.**

    Eu cobrei que um longo com titulo divergente fosse acusado, *"para a
    acusacao nao ficar presa a um formato"*. **Era o TESTE errado, nao o
    modulo:** a linha de `videos` do LONGO copia o titulo do proprio notice
    (`titulo if e_longo else (titulo_short(spec) or titulo)`), logo os dois
    lados do cruzamento sao o MESMO valor e o longo nao pode divergir por
    construcao.

    O que fica cobrado e a propriedade verdadeira, e ela e uma limitacao que
    vale escrita: **o cruzamento so tem dentes no SHORT** — que e exatamente
    onde o incidente de 19/10 as 14:4x ocorreu. Se algum dia a linha do longo
    passar a ter fonte propria, este teste reprova e a nota se rele.
    """
    import registro_videos as RV
    fonte = textwrap.dedent(inspect.getsource(RV.linhas_dos_notices))
    assert "titulo if e_longo else" in fonte, (
        "a linha do LONGO deixou de copiar o titulo do notice: agora ela tem"
        " fonte propria e o cruzamento passa a ter dentes nos dois lados —"
        " releia esta nota em vez de a apagar")
    d = AR.divergencia_de_titulo(_pacote(t_longo="OUTRO TITULO QUALQUER"))
    assert d["divergentes"] == [], (
        "o longo apareceu como divergente, e ele nao pode: os dois lados dele"
        " sao o mesmo valor")
    assert d["pares"] == 2, (
        "as duas pecas seguem PAREADAS — o lado do longo e vacuo, nao ausente")


def test_short_SOLTO_continua_funcionando():
    """O caso em que a funcao nasceu, e que nao pode ter regredido."""
    d = AR.divergencia_de_titulo(_solto())
    assert d["pares"] == 1
    assert d["divergentes"] == []
    d2 = AR.divergencia_de_titulo(_solto(titulo="TITULO DIFERENTE"))
    assert len(d2["divergentes"]) == 1


def test_a_chave_e_o_youtube_id_por_AST():
    corpo = _corpo_sem_docstring(AR.divergencia_de_titulo)
    fonte = ast.unparse(corpo)
    assert "do_notice[yid]" in fonte or "do_notice.get(yid" in fonte, (
        "a leitura do notice nao e feita pelo `youtube_id`")
    assert "do_notice[pac]" not in fonte and "do_notice.get(pac" not in fonte, (
        "a chave voltou a ser o PACOTE, e um pacote emite dois notices")


def test_as_duas_leituras_continuam_DELEGADAS():
    corpo = _corpo_sem_docstring(AR.divergencia_de_titulo)
    chamadas = {ast.unparse(n.func) for n in ast.walk(corpo)
                if isinstance(n, ast.Call)}
    assert "CA.titulos_dos_notices" in chamadas, (
        "a testemunha tem de vir do dono do notice")
    assert "publicado" in chamadas, (
        "a linha de `videos` tem de vir do dono dela")
    proibidos = {"re.findall", "re.search", "re.compile", "open"}
    assert not (chamadas & proibidos), (
        "o corpo reparseia o notice (%s): seria o TERCEIRO dono da forma dele"
        % sorted(chamadas & proibidos))


def test_o_motivo_e_o_725_continuam_escritos():
    fonte = _fonte(AR.divergencia_de_titulo)
    for pedaco in ("13:5x", "725", "youtube_id", "DOIS notices"):
        assert pedaco in fonte, (
            "o motivo saiu do modulo (%r): conserto sem motivo escrito volta"
            " calado" % pedaco)
    assert CASO_DE_13H["pacote"] in fonte, (
        "o caso medido saiu do modulo — ele e a procedencia do conserto")
