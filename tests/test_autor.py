"""A escrita automatica de roteiro — a parte que decide TAMANHO.

O gerador existe porque o teto subiu para 5 pacotes por canal por dia e a
escrita a mao entrega, no melhor dia, 24 para treze canais. O que estes testes
cercam nao e o texto (isso quem julga sao os portoes e o `fatos.py`), e sim o
dimensionamento — a parte que falha em silencio e so aparece depois do render.

O defeito que motivou metade deles: em 20/08/2026 o labtreinamento-003 foi ao
ar com short de 47,6 s, fora do teto de 45. A causa foi dimensionar so o longo.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "fabrica"))

import autor  # noqa: E402
import ensaio  # noqa: E402
import prontidao  # noqa: E402

SPECS = RAIZ / "fabrica" / "specs"


def _reais():
    for c in sorted(SPECS.glob("*.json")):
        try:
            sp = json.loads(c.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        if sp.get("longo") and sp.get("voz") in ensaio.MODELO_VOZ:
            yield c.stem, sp


# ------------------------------------------------------------- o orcamento

def _sinteticas(voz: str, alvo_s: float, n: int, fc: int = 2) -> list[dict]:
    """Cenas de teste com EXATAMENTE `fc` frases cada e o texto do orcamento.

    O `fc` inteiro entra nos dois lados da conta de proposito: o que este teste
    mede e se o orcamento e o inverso da medicao, nao se o palpite de densidade
    esta certo — isso quem mede e o teste contra o corpus real.
    """
    orc = autor.orcamento_de_texto(voz, alvo_s, n, fc)
    por_frase = max(1, orc // (n * fc))
    return [{"nar": " ".join(["a" * por_frase + "."] * fc)} for _ in range(n)]


def test_o_orcamento_e_o_inverso_da_medicao():
    """Pedir N caracteres e medir o resultado tem de fechar no mesmo tempo.

    Se as duas contas divergirem, o laco de correcao persegue um alvo que nao
    existe e nunca converge — e cada volta do laco e uma chamada de modelo.
    """
    voz = "pt-BR-ThalitaMultilingualNeural"
    alvo = 810.0
    cenas = _sinteticas(voz, alvo, 80)
    assert abs(autor.medir(cenas, voz) - alvo) < 5.0


def test_o_inverso_fecha_em_toda_voz_da_frota():
    """Treze canais, oito linguas, taxas que vao de 8 a 21 chars/s."""
    for voz in ensaio.MODELO_VOZ:
        for alvo, n in ((810.0, 80), (38.0, 6)):
            d = autor.medir(_sinteticas(voz, alvo, n), voz)
            assert abs(d - alvo) < max(3.0, alvo * 0.02), f"{voz} em {alvo}s: {d:.1f}"


def _desvios(por_canal: bool) -> list[float]:
    """Erro do orcamento contra cada spec que ja foi ao ar, FORA da amostra.

    O `excluir` e o que torna a afericao honesta, e ele faltava ate 25/08/2026.
    `autor.densidade` le as specs do canal em disco; sem excluir a spec que
    esta sendo prevista, ela entra na propria populacao que gera a previsao. O
    numero que saia dai era ajuste dentro da amostra, e nao previsao — e o
    docstring do teste ja dizia "aferido contra o corpus real, nao contra si
    mesmo", que era exatamente o que nao estava acontecendo.

    Em producao esse vazamento nao existe: quando o `autor` dimensiona uma
    spec nova, ela ainda nao esta em disco. Entao a leitura de fora da amostra
    e a unica que descreve o que a esteira vive.
    """
    saida = []
    for nome, sp in _reais():
        c = autor.chars(sp["longo"])
        if c < 2000:
            continue
        fc = (autor.densidade(sp["slug"], "longo", excluir=nome + ".json")
              if por_canal else autor.FRASES_POR_CENA)
        prev = autor.orcamento_de_texto(
            sp["voz"], autor.medir(sp["longo"], sp["voz"]), len(sp["longo"]), fc)
        saida.append(abs(prev - c) / c)
    return sorted(saida)


def test_o_primeiro_rascunho_ja_cai_dentro_da_tolerancia():
    """Aferido contra o corpus real, nao contra si mesmo — agora de verdade.

    A tolerancia do laco e de 1 min em 13,5 — 7,4%. O que este teste garante e
    que a spec MEDIANA nasce dentro dela, ou seja, sem gastar uma segunda
    chamada de modelo so para ajustar tamanho.

    OS NUMEROS SAO OUTROS DESDE 25/08/2026, e a spec nao mudou: o que mudou foi
    a afericao passar a excluir a spec prevista da populacao que gera a
    previsao. Medido sobre as 74 specs com mais de 2.000 caracteres:

        por canal, DENTRO da amostra (o que este teste media)  3,46%   77,0%
        por canal, FORA da amostra (a condicao de producao)    5,23%   58,1%
        constante global do corpus                             4,55%   71,6%

    As barras abaixo sao a segunda linha, que e a verdadeira, com folga curta.
    Elas nao devem ser afrouxadas: se o orcamento piorar, o teste tem de cair.

    E a terceira linha e um achado que este teste nao fecha sozinho: FORA da
    amostra, a densidade por canal perde para a constante global do corpus —
    13,5 pontos a menos de specs nascendo dentro da tolerancia. O motivo e
    tamanho de amostra: um canal tem de 3 a 16 specs, e a mediana de tao pouco
    e instavel. A troca nao foi feita aqui de proposito, porque mexe em como
    TODA spec e dimensionada e merece rodada propria; esta registrada como
    aprendizado com a tabela inteira.
    """
    d = _desvios(por_canal=True)
    assert d, "nenhuma spec real para aferir"
    mediana = d[len(d) // 2]
    assert mediana < 0.06, f"mediana do desvio: {mediana:.1%}"
    dentro = sum(1 for x in d if x < autor.TOLERANCIA_S / autor.ALVO_S)
    assert dentro / len(d) > 0.55, f"so {dentro}/{len(d)} nasceriam dentro"


def _desvios_do_bloco(bloco: str, usar_canal: bool) -> list[float]:
    """Como `_desvios`, mas de qualquer bloco e sempre fora da amostra."""
    minimo = 2000 if bloco == "longo" else 200
    saida = []
    for nome, sp in _reais():
        cenas = sp.get(bloco) or []
        c = autor.chars(cenas)
        if c < minimo:
            continue
        fc = (_mediana_do_canal(sp["slug"], bloco, nome + ".json") if usar_canal
              else autor.FRASES_POR_CENA)
        prev = autor.orcamento_de_texto(
            sp["voz"], autor.medir(cenas, sp["voz"]), len(cenas), fc)
        saida.append(abs(prev - c) / c)
    return sorted(saida)


def _mediana_do_canal(slug: str, bloco: str, excluir: str) -> float:
    """A mediana crua do canal, sem o desvio por bloco que `densidade` aplica.

    Reimplementada aqui de proposito: o teste abaixo compara as DUAS fontes, e
    chamar `densidade` daria a resposta que ela ja escolheu, nunca a rejeitada.
    """
    import statistics

    import narracao as N

    vistos = []
    for caminho in sorted((RAIZ / "fabrica" / "specs").glob(f"{slug}-*.json")):
        if caminho.name == excluir:
            continue
        try:
            sp = json.loads(caminho.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            continue
        cenas = sp.get(bloco) or []
        if len(cenas) < 4:
            continue
        idi = N.idioma_de(sp, None)
        vistos.append(sum(len(N.frases((c or {}).get("nar") or "", idi))
                          for c in cenas) / len(cenas))
    return statistics.median(vistos) if vistos else autor.FRASES_POR_CENA


def test_a_fonte_da_densidade_e_a_que_mede_melhor_em_cada_bloco():
    """A escolha de `densidade`, medida bloco a bloco e fora da amostra.

    Este teste substitui um que afirmava a mesma coisa para os dois blocos e
    media DENTRO da amostra. Fora dela a resposta se parte em duas, e e por
    isso que `densidade` hoje devolve fontes diferentes:

        longo   canal  5,23% / 58,1%   contra   corpus  4,55% / 71,6%
        short   canal  4,20% / 71,2%   contra   corpus 14,26% / 32,5%

    No longo o canal perde por tamanho de amostra. No short o corpus perde
    porque a constante de 2,26 foi calibrada em bloco longo, e short e outro
    regime de escrita.

    Se um dia qualquer das duas viradas se inverter, este teste cai e a decisao
    se revisa com dado — em vez de a funcao seguir existindo por inercia.
    """
    tol = autor.TOLERANCIA_S / autor.ALVO_S

    def dentro(d):
        return sum(1 for x in d if x < tol) / len(d)

    longo_canal = _desvios_do_bloco("longo", usar_canal=True)
    longo_corpus = _desvios_do_bloco("longo", usar_canal=False)
    assert dentro(longo_corpus) > dentro(longo_canal), (
        "no longo a constante do corpus deixou de ser melhor — "
        f"corpus {dentro(longo_corpus):.1%} contra canal {dentro(longo_canal):.1%}")

    short_canal = _desvios_do_bloco("short", usar_canal=True)
    short_corpus = _desvios_do_bloco("short", usar_canal=False)
    assert dentro(short_canal) > dentro(short_corpus), (
        "no short a mediana do canal deixou de ser melhor — "
        f"canal {dentro(short_canal):.1%} contra corpus {dentro(short_corpus):.1%}")


def test_densidade_devolve_a_fonte_escolhida_em_cada_bloco():
    """A trava contra reverter a escolha sem reverter a medicao junto."""
    assert autor.densidade("nivel-do-jogo", "longo") == autor.FRASES_POR_CENA
    do_short = autor.densidade("nivel-do-jogo", "short")
    assert do_short != autor.FRASES_POR_CENA
    assert do_short == _mediana_do_canal("nivel-do-jogo", "short", "")


def test_voz_sem_modelo_medido_nao_dimensiona():
    """Nao ha como escrever para uma voz cuja taxa ninguem mediu — e chutar
    aqui produz um video fora da faixa que so aparece depois do render."""
    with pytest.raises(SystemExit):
        autor.orcamento_de_texto("xx-XX-NinguemNeural", 810, 80)


# ------------------------------------------------------------- a faixa

def test_o_short_entra_no_laco_de_correcao():
    """O defeito de 20/08: o dimensionamento so olhava o longo, e o short de
    47,6 s passou por baixo dele."""
    sp = {"voz": "pt-BR-ThalitaMultilingualNeural",
          "longo": [{"nar": "x" * 200} for _ in range(80)],
          "short": [{"nar": "x" * 400} for _ in range(6)]}
    pedidos = autor._fora_da_faixa(sp, sp["voz"])
    assert any("short" in p for p in pedidos)


def test_short_dentro_da_faixa_nao_pede_correcao():
    voz = "el-GR-NestorasNeural"
    sp = json.loads((SPECS / "epomeno-epipedo-007.json").read_text(encoding="utf-8"))
    assert sp["voz"] == voz
    assert not [p for p in autor._fora_da_faixa(sp, voz) if "short" in p]


def test_a_faixa_do_short_mira_no_meio_e_nao_no_teto():
    """Mirar no teto e ficar sem folga para o erro conhecido do modelo em
    short (ate 7% para baixo, sempre subestimando)."""
    voz = "pt-BR-ThalitaMultilingualNeural"
    quase_no_teto = prontidao.SHORT_MAX_S * (1 - prontidao.MARGEM_SHORT) - 0.5
    sp = {"voz": voz, "longo": _sinteticas(voz, autor.ALVO_S, 80),
          "short": _sinteticas(voz, quase_no_teto, 6)}
    do_short = [p for p in autor._fora_da_faixa(sp, voz) if "short" in p]
    assert do_short and "ENCURTE" in do_short[0]


def test_correcao_vai_em_caracteres_nao_em_cenas():
    """Pedir "mais cinco cenas" devolve cinco cenas de tamanho arbitrario, e a
    medida seguinte erra de novo. Caractere e a unidade do modelo de voz."""
    sp = {"voz": "pt-BR-ThalitaMultilingualNeural",
          "longo": [{"nar": "x" * 50} for _ in range(80)], "short": []}
    p = autor._fora_da_faixa(sp, sp["voz"])[0]
    assert "caracteres" in p and "ALONGUE" in p
    assert "cenas" not in p.replace("numero de cenas", "")


def test_longo_no_alvo_nao_pede_nada():
    voz = "pt-BR-ThalitaMultilingualNeural"
    sp = {"voz": voz, "longo": _sinteticas(voz, autor.ALVO_S, 80), "short": []}
    assert not [p for p in autor._fora_da_faixa(sp, voz) if "longo" in p]


def test_a_densidade_do_short_e_medida_separada_da_do_longo():
    """Short escreve mais curto: 1,60 frases por cena no setiap-level contra
    1,98 no longo do mesmo canal. Usar a densidade do longo no short erra o
    termo que mais pesa num video de 6 cenas."""
    for slug in ("setiap-level", "epomeno-epipedo", "labtreinamento"):
        assert autor.densidade(slug, "short") < autor.densidade(slug, "longo"), slug


def test_canal_sem_spec_anterior_cai_na_mediana_do_corpus():
    assert autor.densidade("canal-que-nao-existe") == autor.FRASES_POR_CENA


# ------------------------------------------------------------- similaridade

def test_pauta_parecida_com_o_acervo_e_recusada():
    pub = ["Planilha de Riscos Psicossociais da NR-1 em Excel"]
    passa, valor, _ = autor.inedita(
        "Planilha de Riscos Psicossociais da NR 1 no Excel", pub)
    assert not passa and valor > autor.SIMILARIDADE_MAX


def test_pauta_de_outro_eixo_passa():
    pub = ["Planilha de Riscos Psicossociais da NR-1 em Excel"]
    passa, valor, _ = autor.inedita("ISO 9001:2026 — planilha de transicao", pub)
    assert passa and valor <= autor.SIMILARIDADE_MAX


def test_canal_sem_acervo_nao_trava():
    passa, valor, contra = autor.inedita("qualquer coisa", [])
    assert passa and valor == 0.0 and contra == ""


def test_o_limite_e_o_mesmo_da_publicacao():
    """Dois numeros para a mesma regra viram dois numeros diferentes."""
    sys.path.insert(0, str(RAIZ / "src"))
    from maquina.config import Config

    assert autor.SIMILARIDADE_MAX == Config().publicacao.similaridade_max


# ------------------------------------------------------------- a identidade

def test_o_que_e_do_canal_nao_vem_do_modelo():
    """Voz, trilha, idioma e paleta nao entram no pedido: sao identidade, ja
    estao decididas, e deixar o modelo repeti-las cria uma segunda copia que
    uma hora diverge calada — foi assim que o kolejny-poziom-005 foi ao ar com
    a trilha de outro canal."""
    ctx = autor.contexto("labtreinamento")
    sp = autor._monta(ctx, {"longo": [], "short": [], "thumb": {}, "copy": "",
                            "voz": "INVENTADA", "trilha": "INVENTADA",
                            "paleta": {"ink": "#FFFFFF"}}, 9)
    assert sp["voz"] == ctx["voz"]
    assert sp["trilha"] == ctx["trilha"]
    assert sp["paleta"] == ctx["paleta"]


def test_spec_gerada_se_declara_de_maquina():
    """Sem o carimbo o portao de fatos nao se aplica, e o gerador publicaria
    numero que ninguem conferiu."""
    ctx = autor.contexto("labtreinamento")
    sp = autor._monta(ctx, {"longo": [], "short": [], "thumb": {}, "copy": ""}, 9)
    assert sp["autoria"] == "maquina"
    assert prontidao._gate_fatos(sp)


def test_o_contexto_sai_do_yaml_do_canal():
    ctx = autor.contexto("labtreinamento")
    assert ctx["idioma"] == "pt-BR"
    assert ctx["voz"] == "pt-BR-ThalitaMultilingualNeural"
    assert ctx["trilha"] == "Inspired"
    assert ctx["categoria_id"] == "27"
    assert "planilha" in ctx["memoria"].lower()


def test_todo_canal_da_frota_tem_contexto_legivel():
    """Um canal cujo yaml nao responde e um canal que o gerador pula em
    silencio — e ninguem descobre ate a fila secar."""
    for yaml in sorted((RAIZ / "config" / "canais").glob("*.yaml")):
        slug = yaml.stem
        if not list(SPECS.glob(f"{slug}-*.json")):
            continue          # canal sem spec anterior escreve a primeira a mao
        ctx = autor.contexto(slug)
        assert ctx["idioma"], slug
        assert ctx["voz"] in ensaio.MODELO_VOZ, f"{slug}: voz sem taxa medida"
        assert ctx["trilha"], slug
        assert ctx["paleta"], slug


def test_o_numero_do_pacote_nao_colide_com_o_que_ja_existe():
    for yaml in sorted((RAIZ / "config" / "canais").glob("*.yaml")):
        slug = yaml.stem
        n = autor.proximo_numero(slug)
        assert not (SPECS / f"{slug}-{n:03d}.json").exists(), slug


def test_o_gerador_sabe_que_a_pauta_nao_e_o_titulo():
    """A pauta do banco diz sobre O QUE falar, nunca como montar o titulo.

    Medido em 20/08/2026 no resep-naik-level: todo outlier do nicho tinha cifra
    mais periodo no titulo (278 a 6.057 v/d) e as doze pautas em banco eram
    todas "por que X esta errado", sem cifra e sem periodo — pesquisadas por
    assunto. Escrever o titulo na forma da pauta e escrever na forma que o
    nicho mede como morta (aprendizado 372).
    """
    assert "ASSINATURA" in autor.SISTEMA
    assert "pesquisada por" in autor.SISTEMA


def test_a_memoria_do_nicho_chega_inteira_ao_pedido():
    """Os comentarios do yaml sao a medicao do nicho — views/dia por formato, o
    que ja morreu. Valem mais para escrever do que qualquer campo estruturado,
    e sem eles o gerador nao tem como achar a assinatura."""
    ctx = autor.contexto("resep-naik-level")
    pedido = autor._pedido(ctx, "uma pauta qualquer", 80, 8000)
    assert ctx["memoria"] in pedido
    assert "views/dia" in pedido or "v/d" in pedido.lower() or "MEMORIA" in pedido


def test_o_gerador_desconfia_de_cifra_que_vem_na_pauta():
    """Duas pautas do canal de saude traziam "R$ 27.000 em 5 Anos" e "R$ 18.000
    em Shakes", e nenhuma tem fonte — a pauta foi escrita por geracao de
    ideias, nao por medicao. Quem tratasse isso como dado publicaria numero
    inventado num canal de saude (aprendizado 376)."""
    assert "NAO VERIFICADA" in autor.SISTEMA
    assert "METODO" in autor.SISTEMA


def test_o_gerador_procura_o_fato_regulatorio_em_saude():
    """"Suplementos inuteis" e alegacao de eficacia, insustentavel em doze
    minutos. "189 alegacoes permitidas e emagrecer nao e uma delas" e o texto
    da norma — gancho mais forte e exposicao menor (aprendizado 377)."""
    assert "REGULATORIO" in autor.SISTEMA
    assert "189" in autor.SISTEMA
