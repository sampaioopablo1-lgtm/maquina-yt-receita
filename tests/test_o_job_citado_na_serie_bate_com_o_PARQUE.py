"""Eu escrevi um job id INVENTADO na procedencia da serie, e quase ficou.

MEDIDO em 19/10 as 07:2x. Ao acrescentar o ponto do `epomeno-epipedo-s066` eu
escrevi a nota com `python3 -c "..."` dentro do bash, e:

  1. a CRASE do heredoc comeu texto — o `CLAUDE.md` avisa isso em letra, e e a
     segunda vez que me pega nesta sessao;
  2. no lugar do job verdadeiro eu escrevi `117928061886`, que **nao existe** —
     o job daquele render e `117916386985`. Era um numero da minha cabeca.

**E a parte que importa: a nota garbled ainda PASSAVA em tudo.** Nenhum teste
olhava se o job citado na serie corresponde ao job que o PARQUE gravou para
aquele pacote, e o parque e a fonte de verdade — ele recebe o job na publicacao,
quando ele ainda esta na mao.

Eu so vi porque fui conferir o id contra o `duracoes-a-medir.jsonl` por outro
motivo. **Procedencia inventada e pior que procedencia ausente**, porque ela
convida a conferir no lugar errado: quem fosse ler as anotacoes do
`117928061886` levaria 404 e concluiria que o provedor nao foi medido.

Este arquivo cruza os DOIS donos do mesmo fato — a marca `# job` na serie e o
campo `job` do parque — e reprova quando divergem.
"""
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import serie_residuo as SR  # noqa: E402

PARQUE = os.path.join(RAIZ, "docs", "pendente", "duracoes-a-medir.jsonl")
PONTO = re.compile(
    r'\("([^"]+)",\s*[\d.]+,\s*\d+,\s*"\w+"\),\s*#\s*job\s*(\d+)')


def _jobs_da_serie():
    fora = {}
    for linha in SR._texto(SR.ARQ_SERIE).splitlines():
        m = PONTO.search(linha)
        if m:
            fora[m.group(1)] = m.group(2)
    return fora


def _jobs_do_parque():
    fora = {}
    with open(PARQUE, encoding="utf-8") as f:
        for linha in f:
            linha = linha.strip()
            if not linha:
                continue
            d = json.loads(linha)
            if d.get("job"):
                fora[d["pacote"]] = str(d["job"])
    return fora


def test_a_varredura_acha_os_DOIS_lados():
    serie, parque = _jobs_da_serie(), _jobs_do_parque()
    assert len(serie) >= 40, (
        f"so {len(serie)} pontos da serie tem marca de job — a regex deixou de "
        "casar, e ai todo este arquivo passaria calado")
    assert len(parque) >= 40, f"o parque encolheu para {len(parque)} linhas"
    assert len(set(serie) & set(parque)) >= 40, (
        "os dois lados pararam de se cruzar: sem pacote em comum este arquivo "
        "nao mede nada")


def test_todo_job_citado_na_serie_bate_com_o_do_PARQUE():
    serie, parque = _jobs_da_serie(), _jobs_do_parque()
    divergem = [(p, serie[p], parque[p]) for p in sorted(set(serie) & set(parque))
                if serie[p] != parque[p]]
    assert not divergem, (
        "a serie cita job diferente do que o parque gravou na publicacao — "
        "procedencia inventada e pior que ausente: "
        + "; ".join(f"{p}: serie {a} contra parque {b}" for p, a, b in divergem))


def test_o_job_INVENTADO_de_07_2x_nao_voltou():
    """Ancorado no caso real, e e o unico numero cravado aqui de proposito:
    ele e o ERRO, nao a medida."""
    texto = SR._texto(SR.ARQ_SERIE)
    assert "117928061886" not in texto, (
        "o job inventado voltou para a serie")
    assert "117916386985" in texto, (
        "o job VERDADEIRO do epomeno-epipedo-s066 saiu da serie")


def test_nenhuma_marca_de_job_fica_sem_PACOTE_na_mesma_linha():
    """Marca de job solta e o sintoma do `replace` por prefixo (18/10 11:2x),
    e tambem o que esconderia um id sem dono."""
    soltas = [l.strip() for l in SR._texto(SR.ARQ_SERIE).splitlines()
              if re.search(r"#\s*job\s*\d+", l) and not PONTO.search(l)
              and not l.strip().startswith("#")]
    assert not soltas, f"marca de job sem ponto na mesma linha: {soltas[:3]}"


def test_a_CRASE_do_heredoc_continua_avisada_onde_dói():
    """O aviso existe no `CLAUDE.md` desde 11/10 e me pegou duas vezes hoje.
    Ele tem de continuar escrito, porque e o que explica a nota garbled."""
    with open(os.path.join(RAIZ, "CLAUDE.md"), encoding="utf-8") as f:
        texto = " ".join(f.read().split())
    assert "crase no heredoc come texto" in texto or \
           "crase em heredoc come texto" in texto, (
        "o aviso da crase saiu do CLAUDE.md")


def test_o_MOTIVO_deste_arquivo_continua_escrito():
    with open(os.path.abspath(__file__), encoding="utf-8") as f:
        texto = " ".join(f.read().split())
    for frase in ("117928061886", "117916386985", "pior que procedencia ausente"):
        assert frase in texto, f"o motivo perdeu {frase!r}"
