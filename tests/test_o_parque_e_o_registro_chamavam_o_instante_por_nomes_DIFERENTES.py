"""O parque e o registro chamavam o MESMO instante por nomes diferentes.

Medido em 20/10 as 09:3x, e e a segunda rodada seguida em que eu erro o mesmo
passo a mao. Os dois modulos que leem o MESMO `::notice:: PUBLICADO` divergem no
nome do instante: o `registro_videos.linhas_dos_notices` devolve `publicado_em`,
e o `duracao_a_medir.OBRIGATORIOS` pede `em`. Eu montava o dicionario do parque
redigitando o mapeamento a cada rodada, e o `valida` me levantou por
`prev_edge`/`prev_piper` numa rodada e por `em` na seguinte.

A falha e RUIDOSA e nao permissiva — o `valida` levanta, pelo 733 —, logo ela
nunca parqueou peca errada. O que ela custa e uma passada por rodada e a chance
de eu soltar o passo no meio, que e exatamente como o corpus atrasou sete
rodadas (726). `do_registro` poe o mapeamento num dono so.
"""
import ast
import io
import os
import sys

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FABRICA = os.path.join(RAIZ, "fabrica")
MODULO = os.path.join(FABRICA, "duracao_a_medir.py")
sys.path.insert(0, FABRICA)

import duracao_a_medir as DM  # noqa: E402
import registro_videos as RV  # noqa: E402

NOTICE = ("PUBLICADO epomeno-epipedo-s074 shorts youtube_id=tUE21qPa2S8 "
          "titulo=Το πάγιο δεν πολλαπλασιάζεται em=2026-10-20T09:19:46Z")


def _reg():
    linhas = RV.linhas_dos_notices(NOTICE)
    assert len(linhas) == 1, linhas
    return linhas[0]


def test_os_DOIS_donos_de_fato_DIVERGEM_no_nome():
    """A medida que torna o conserto necessario, reconferida nos dois modulos.

    Se um dia os dois passarem a usar o MESMO nome, este teste reprova e a nota
    se rele — em vez de o mapeamento ficar aqui sem objeto.
    """
    r = _reg()
    assert "publicado_em" in r, sorted(r)
    assert "em" not in r, sorted(r)
    assert "em" in DM.OBRIGATORIOS, DM.OBRIGATORIOS
    assert "publicado_em" not in DM.OBRIGATORIOS, DM.OBRIGATORIOS


def test_ele_REPRODUZ_o_dicionario_que_eu_montei_a_mao():
    """Sem isto a nota nao prova que o instrumento serve a decisao tomada."""
    reg = DM.do_registro(_reg(), 41.55, 36.81, "edge", "118550315664")
    assert reg == {
        "pacote": "epomeno-epipedo-s074",
        "canal": "epomeno-epipedo",
        "youtube_id": "tUE21qPa2S8",
        "em": "2026-10-20T09:19:46Z",
        "cenas": 12,
        "prev_edge": 41.55,
        "prev_piper": 36.81,
        "provedor": "edge",
        "job": "118550315664",
    }, reg


def test_todo_campo_OBRIGATORIO_sai_preenchido():
    """Cobrado como PROPRIEDADE sobre a constante, nao por lista minha."""
    reg = DM.do_registro(_reg(), 41.55, 36.81, "edge", "118550315664")
    faltam = [c for c in DM.OBRIGATORIOS if not reg.get(c)]
    assert faltam == [], faltam


def test_ele_ACEITA_registro_que_ja_use_o_nome_do_parque():
    """Contraprova no outro sentido: propriedade, nao identidade de chave."""
    r = dict(_reg())
    r["em"] = r.pop("publicado_em")
    reg = DM.do_registro(r, 41.55, 36.81, "edge", "118550315664")
    assert reg["em"] == "2026-10-20T09:19:46Z"


def test_ele_LEVANTA_quando_o_instante_nao_vem_de_lado_nenhum():
    """Ausencia de instante nao vira parque silencioso."""
    r = dict(_reg())
    r.pop("publicado_em")
    with pytest.raises(ValueError) as e:
        DM.do_registro(r, 41.55, 36.81, "edge", "118550315664")
    assert "em" in str(e.value)


def test_as_previsoes_e_o_PROVEDOR_seguem_vindo_DE_FORA():
    """A disciplina do 733: nao ha default para elas, e isso e deliberado.

    Elas sao medicao da RODADA — a previsao sai do `ensaio`, o provedor da
    ANOTACAO do job — e nao estao no notice. Dar-lhes padrao aqui faria a
    rodada futura INFERIR o provedor, que e o erro que o 733 nomeia.
    """
    arvore = ast.parse(io.open(MODULO, encoding="utf-8").read())
    alvo = [n for n in ast.walk(arvore)
            if isinstance(n, ast.FunctionDef) and n.name == "do_registro"]
    assert len(alvo) == 1
    assert alvo[0].args.defaults == [], "nenhum destes argumentos tem padrao"
    nomes = [a.arg for a in alvo[0].args.args]
    for esperado in ("prev_edge", "prev_piper", "provedor", "job"):
        assert esperado in nomes, (esperado, nomes)
    with pytest.raises(ValueError):
        DM.do_registro(_reg(), 41.55, 36.81, "", "118550315664")
    with pytest.raises(ValueError):
        DM.do_registro(_reg(), 41.55, 36.81, "edge", "")


def test_o_mapeamento_tem_UM_dono():
    """Por AST: `publicado_em` so pode aparecer dentro do `do_registro`.

    Uma segunda traducao em outra funcao e a assinatura que congelou a legenda,
    e aqui ela reapareceria como "o parque recebeu o instante de dois lugares".
    """
    arvore = ast.parse(io.open(MODULO, encoding="utf-8").read())
    donos = set()
    for no in ast.walk(arvore):
        if not isinstance(no, ast.FunctionDef):
            continue
        for dentro in ast.walk(no):
            if (isinstance(dentro, ast.Constant)
                    and isinstance(dentro.value, str)
                    and dentro.value == "publicado_em"):
                donos.add(no.name)
    assert donos == {"do_registro"}, donos


def test_ele_DELEGA_a_validacao_em_vez_de_refazer():
    """Por AST: a lista de obrigatorios tem um dono, o `valida`."""
    arvore = ast.parse(io.open(MODULO, encoding="utf-8").read())
    alvo = [n for n in ast.walk(arvore)
            if isinstance(n, ast.FunctionDef) and n.name == "do_registro"][0]
    chamados = {getattr(n.func, "id", None) or getattr(n.func, "attr", None)
                for n in ast.walk(alvo) if isinstance(n, ast.Call)}
    assert "valida" in chamados, chamados
    fonte = io.open(MODULO, encoding="utf-8").read()
    assert fonte.count("OBRIGATORIOS = (") == 1


def test_o_MOTIVO_continua_escrito_no_modulo():
    fonte = io.open(MODULO, encoding="utf-8").read()
    for marca in ("publicado_em", "RUIDOSA", "726", "733", "a mao"):
        assert marca in fonte, (
            "conserto sem o motivo escrito volta calado: falta %r" % marca)


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-q"]))
