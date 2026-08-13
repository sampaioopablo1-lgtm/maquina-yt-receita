"""O medidor de prontidao nao pode aprovar o que o publicar.py reprova.

Ele existe para responder uma pergunta com numero — quantos pacotes a frota
dispara agora — e essa resposta so vale se os portoes dele forem os MESMOS que
a esteira aplica depois. Um medidor mais frouxo que a esteira e pior que nenhum:
ele promete pacotes que vao abortar depois do render.

Estes testes trancam a equivalencia nos dois pontos onde ela pode escorregar.
"""

from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "fabrica"))

import prontidao  # noqa: E402


def _spec_minima(**extra):
    base = {
        "slug": "nivel-do-jogo",
        "pacote": "nivel-do-jogo-002",
        "idioma": "pt-BR",
        "voz": "pt-BR-AntonioNeural",
        "paleta": {"ink": "#000", "c1": "#111", "c2": "#222", "bg": "#FFF"},
        "thumb": {"l1": "A", "l2": "B"},
        "longo": [{"layout": "titulo", "kicker": "k", "sub": "s", "nar": "Oi.",
                   "cap": "Um"}],
        "short": [],
    }
    base.update(extra)
    return base


def test_bilhete_reprova_no_portao_copy():
    """As specs com `copy` de bilhete abortam o publicar.py DEPOIS do render.

    O medidor tem que enxergar isso antes, senao ele conta como pronto um
    pacote que vai queimar dezessete minutos de runner e uma vaga de
    publicacao para morrer no fim.
    """
    faltas = prontidao._gate_copy(
        _spec_minima(copy="gerado a partir dos capitulos reais apos o render")
    )
    assert faltas and "bilhete" in faltas[0]


def test_descricao_curta_reprova():
    """A rotina pede descricao com 200+ palavras. Sete specs v1 tinham entre
    115 e 145 — passavam no publicar.py e mesmo assim nao servem."""
    copy = (
        "# t\n\n## TITULO\nUm titulo\n\n## DESCRICAO\n"
        + "palavra " * 50
        + "\n\n## TAGS\numa, duas, tres, quatro\n\n## HASHTAGS\n#a #b #c\n"
        "\n## COMENTARIO\nUma pergunta para o publico?\n"
    )
    faltas = prontidao._gate_copy(_spec_minima(copy=copy))
    assert any("200" in f for f in faltas), faltas


def test_tags_fora_do_orcamento_reprovam():
    """O limite de 500 do YouTube conta tag com espaco como len+2.

    orcamento_tags corta silenciosamente o que nao cabe; aqui o corte precisa
    virar reprovacao, porque tag cortada e busca perdida sem ninguem avisar.
    """
    tags = ", ".join(f"tag longa numero {i:02d} de teste" for i in range(30))
    copy = (
        "# t\n\n## TITULO\nUm titulo\n\n## DESCRICAO\n"
        + "palavra " * 250
        + f"\n\n## TAGS\n{tags}\n\n## HASHTAGS\n#a #b #c\n"
        "\n## COMENTARIO\nUma pergunta para o publico?\n"
    )
    faltas = prontidao._gate_copy(_spec_minima(copy=copy))
    assert any("orcamento" in f for f in faltas), faltas


def test_identidade_pega_pacote_divergente(tmp_path):
    caminho = tmp_path / "nivel-do-jogo-002.json"
    caminho.write_text(json.dumps(_spec_minima(pacote="outro-nome")), encoding="utf-8")
    faltas = prontidao._gate_identidade(str(caminho), json.loads(caminho.read_text()))
    assert any("pacote" in f for f in faltas)


def test_identidade_pega_idioma_divergente_do_canal(tmp_path):
    """A spec vence o config em publicar.py, entao spec errada nao e corrigida
    por ninguem: um video pt-BR subiria marcado como grego."""
    caminho = tmp_path / "nivel-do-jogo-002.json"
    caminho.write_text(json.dumps(_spec_minima(idioma="el")), encoding="utf-8")
    faltas = prontidao._gate_identidade(str(caminho), json.loads(caminho.read_text()))
    assert any("idioma" in f for f in faltas)


def test_falta_de_fonte_e_ambiente_e_nao_defeito_da_spec():
    """`usar_fonte` aborta sem a Noto Devanagari, que o agla-level pede.

    Se isso reprovasse a spec, a agla-level-003 apareceria como travada em toda
    maquina sem a fonte — e o frota.yml instala fonts-noto-core, que a traz.
    """
    faltas = prontidao._gate_layout(
        _spec_minima(fonte="Fonte Que Nao Existe Em Lugar Nenhum")
    )
    assert faltas and faltas[0].startswith("AMBIENTE")


SPECS_REAIS = sorted((RAIZ / "fabrica" / "specs").glob("*.json"))


@pytest.mark.parametrize(
    "spec",
    [p for p in SPECS_REAIS if json.loads(p.read_text(encoding="utf-8")).get("copy")
     and len(json.loads(p.read_text(encoding="utf-8"))["copy"]) > 200],
    ids=lambda p: p.stem,
)
def test_toda_spec_com_copy_real_passa_no_portao_copy(spec):
    """Regressao: uma spec que ja tem copy de verdade nao pode regredir.

    Cobre o caso que aconteceu de fato — parser de copy mudou e specs que
    publicavam pararam de publicar, sem teste nenhum reclamar.
    """
    sp = json.loads(spec.read_text(encoding="utf-8"))
    if not sp.get("longo"):
        pytest.skip("nao e spec de video")
    # As specs v1 sao as SEM sufixo -00N: sete pilotos com descricao entre 115 e
    # 145 palavras e sem hashtags. Elas nao vao a producao. O criterio e o nome,
    # nao a contagem de cenas — a epomeno-epipedo v1 tem 65 cenas e mesmo assim
    # e piloto, entao "poucas cenas" classificaria errado.
    if not re.search(r"-\d{3}$", spec.stem):
        pytest.skip("spec v1 sem sufixo de pacote, fora da producao")
    assert not prontidao._gate_copy(sp), f"{spec.stem}: {prontidao._gate_copy(sp)}"


def test_portao_de_glifos_morde_quando_nenhuma_fonte_cobre(monkeypatch):
    """A logica do portao, provada sem depender das fontes desta maquina.

    Nao da para exercitar isto com um caractere de verdade aqui: o container da
    sessao cobre TODO codepoint alfabetico testado (medido em 13/08/2026, nem
    Osage nem Cuneiforme ficam em zero). Um teste que dependesse disso passaria
    por acidente e nao provaria nada — entao a contagem de fontes e substituida.
    """
    monkeypatch.setattr(prontidao, "_fontes_que_cobrem", lambda cp: 0)
    faltas = prontidao._gate_glifos(
        {"longo": [{"kicker": "abc"}], "short": [], "thumb": {}}
    )
    assert faltas and "tofu" in faltas[0]


def test_portao_de_glifos_ignora_o_nar_do_longo(monkeypatch):
    """O `nar` do longo vai para o .srt, que o YouTube renderiza com as fontes
    do espectador — nao passa pela fabrica e nao pode reprovar a spec."""
    monkeypatch.setattr(prontidao, "_fontes_que_cobrem", lambda cp: 0)
    assert not prontidao._gate_glifos(
        {"longo": [{"nar": "texto so na narracao"}], "short": [], "thumb": {}}
    )


def test_portao_de_glifos_cobre_a_legenda_queimada_do_short(monkeypatch):
    """O `nar` do SHORT vira legenda queimada no pixel — esse entra."""
    monkeypatch.setattr(prontidao, "_fontes_que_cobrem", lambda cp: 0)
    assert prontidao._gate_glifos(
        {"longo": [], "short": [{"nar": "legenda queimada"}], "thumb": {}}
    )


# --------------------------------------------------------------------------
# Thumbnail. A unica imagem que decide o clique, e ate 13/08/2026 nao passava
# por portao nenhum: o layout.py media as CENAS, o visual.py amostrava o VIDEO.

def _spec_thumb(l1, l2):
    return {"paleta": {"ink": "#102618", "c1": "#217346", "c2": "#F2B134",
                       "bg": "#F1F7F4"},
            "thumb": {"l1": l1, "l2": l2}, "longo": [], "short": []}


def test_thumbnail_com_titulo_de_duas_linhas_nao_colide():
    """O defeito real: com posicao fixa (l1 em y=300 corpo 150, l2 em y=480),
    a segunda linha do titulo caia em 487 — sete pixels DEPOIS do topo do
    subtitulo. Estava assim em todo pacote de titulo longo."""
    import layout as L

    assert not L.analisa_thumb(_spec_thumb("LICENCAS DORMINDO", "a planilha que acha"))


def test_geometria_do_thumb_mantem_as_faixas_separadas():
    """A conta e a fonte da verdade, e o portao le a MESMA conta que o desenho.

    Medir a imagem pronta nao serve: renderizar uma linha de cada vez para
    comparar faixas muda a geometria, porque ela depende das duas. Tentei
    assim primeiro e o portao reprovou as dezenove specs, inclusive as boas.
    """
    import fabrica as F

    for l1, l2 in [("R$ 333 MILHÕES", "a caixinha acabou"),
                   ("YOU ARE THE PRODUCT", "credit, explained"),
                   ("4 PILAR", "urutannya"),
                   ("UM TITULO BEM MAIS COMPRIDO QUE O NORMAL", "e um subtitulo longo tambem")]:
        g = F.geometria_thumb({"l1": l1, "l2": l2})
        assert g["base1"] <= g["topo2"], f"{l1!r} colide com {l2!r}"
        assert g["topo1"] >= 40 and g["base2"] <= 680, f"{l1!r} sai da caixa"


@pytest.mark.parametrize(
    "spec", [p for p in SPECS_REAIS
             if json.loads(p.read_text(encoding="utf-8")).get("longo")],
    ids=lambda p: p.stem,
)
def test_toda_spec_tem_thumbnail_legivel(spec):
    import layout as L

    assert not L.analisa_thumb(json.loads(spec.read_text(encoding="utf-8")))


# --------------------------------------------------------------------------
# Trilha. A assinatura sonora do canal, e o credito CC-BY que o copy declara.

def test_trilha_registrada_vence_o_hash(tmp_path, monkeypatch):
    """O hash divide pelos arquivos PRESENTES, e o conjunto varia.

    Medido em 13/08/2026: Cipher2.mp3 nao existe no bucket (404 NoSuchKey),
    entao quem baixa as quatro fica com tres — e o nivel-do-jogo, registrado
    em Inspired, passava a receber Wholesome. Faixa trocada sem erro nenhum,
    com o credito do copy apontando para a outra.
    """
    import copy_md as C

    for f in ("Deliberate_Thought", "Inspired", "Wholesome"):
        (tmp_path / f"{f}.mp3").write_bytes(b"")
    monkeypatch.setattr(C, "TRILHA_DIR", str(tmp_path))

    assert C.trilha_do_canal("nivel-do-jogo").endswith("Wholesome.mp3")
    assert C.trilha_do_canal("nivel-do-jogo", registrada="Inspired").endswith("Inspired.mp3")


def test_trilha_registrada_ausente_levanta_em_vez_de_trocar(tmp_path, monkeypatch):
    """Escolher outra faixa calada troca a assinatura do canal E mente no
    credito CC-BY. Quem chamou tem que decidir, nao a funcao."""
    import copy_md as C

    (tmp_path / "Wholesome.mp3").write_bytes(b"")
    monkeypatch.setattr(C, "TRILHA_DIR", str(tmp_path))

    with pytest.raises(FileNotFoundError, match="Cipher2"):
        C.trilha_do_canal("resep-naik-level", registrada="Cipher2")


def test_sem_trilha_nenhuma_continua_devolvendo_none(tmp_path, monkeypatch):
    import copy_md as C

    monkeypatch.setattr(C, "TRILHA_DIR", str(tmp_path))
    assert C.trilha_do_canal("qualquer") is None


# --------------------------------------------------------------------------
# Duracao. O portao dividia por uma taxa unica de chars/s e somava 0,5 s por
# CENA. Os dois pedacos estavam errados, e o erro so aparece em roteiro de
# frase curta — que e exatamente o que a chave de estilo manda escrever.

def _cenas(*nars):
    return [{"layout": "item", "kicker": "k", "preco": "p", "nar": n} for n in nars]


def test_a_mesma_quantidade_de_texto_dura_mais_em_frases_curtas():
    """O defeito de fundo, provado com o modelo e nao com uma opiniao.

    Medido em 14/08/2026 na id-ID-Gadis: dois textos da MESMA voz devolveram
    15,19 e 8,19 chars/s de taxa aparente. O que muda nao e a voz, e o numero
    de pontos finais — e cada um custa 1,376 s de silencio nessa voz.

    Uma taxa unica nao consegue exprimir isto: ela da o MESMO numero para os
    dois. Este teste falha em qualquer volta para o modelo de um termo.
    """
    from ensaio import duracao_estimada

    corrido = _cenas("a" * 200)
    picado = _cenas(". ".join("a" * 18 for _ in range(10)) + ".")
    assert abs(len(corrido[0]["nar"]) - len(picado[0]["nar"])) <= 12
    assert duracao_estimada(picado, "id-ID-GadisNeural") > \
        duracao_estimada(corrido, "id-ID-GadisNeural") + 8


def test_o_portao_de_duracao_conta_frase_de_hindi_pelo_danda():
    """Em devanagari o fim de frase e o danda, nao o ponto.

    Contando ponto, um roteiro em hindi vira UMA frase e o portao subestima a
    duracao em toda a pausa — no agla-level-003 sao 110 frases a 1,165 s, dois
    minutos inteiros que sumiriam da conta.
    """
    from ensaio import duracao_estimada

    d = duracao_estimada(_cenas("क ख ग। घ ङ च। छ ज झ।"), "hi-IN-MadhurNeural")
    assert d > 3 * 1.165


def test_voz_sem_modelo_reprova_em_vez_de_supor():
    faltas = prontidao._gate_duracao(
        {"voz": "xx-XX-NinguemMediuNeural", "longo": _cenas("oi"), "short": []}
    )
    assert faltas and "sem modelo medido" in faltas[0]


@pytest.mark.parametrize(
    "spec", [p for p in SPECS_REAIS
             if re.search(r"-\d{3}$", p.stem)
             and json.loads(p.read_text(encoding="utf-8")).get("short")],
    ids=lambda p: p.stem,
)
def test_short_de_producao_cabe_na_faixa_de_shorts(spec):
    """O short e o formato que ENTREGA: mede-se 25 a 96x o longo do mesmo
    pacote. Um short de 29 s nao e curtinho, e fora do formato — e essa conta
    mudou quando o modelo passou a contar pausa por frase."""
    from ensaio import MODELO_VOZ, duracao_estimada

    sp = json.loads(spec.read_text(encoding="utf-8"))
    if sp.get("voz") not in MODELO_VOZ:
        pytest.skip("voz sem modelo medido")
    d = duracao_estimada(sp["short"], sp["voz"])
    assert prontidao.SHORT_MIN_S <= d <= prontidao.SHORT_MAX_S, f"{d:.0f} s"


# --------------------------------------------------------------------------
# Canal de destino. Medido em 14/08/2026: o pacote resep-naik-level-002 inteiro
# foi publicado no canal do setiap-level. Nenhuma trava pegava, porque quem
# escolhe o destino e o perfil da Upload-Post e nao a spec.

def test_auditoria_de_canal_separa_certo_de_errado(monkeypatch):
    """A logica do audit, sem depender de rede.

    O caso real tinha 41 videos certos e 2 errados; aqui o que se prova e que
    ele nao confunde os dois, e que video que a API nao devolve vira AUSENTE em
    vez de virar 'canal errado' — sumido e removido, nao e mal publicado.
    """
    import auditoria_canal as A

    monkeypatch.setattr(A, "canais_registrados",
                        lambda u, k: {"resep-naik-level": "UC_RESEP",
                                      "setiap-level": "UC_SETIAP"})
    monkeypatch.setattr(A, "publicados", lambda u, k, s=None: [
        {"canal": "resep-naik-level", "pacote": "rnl-002", "formato": "longo",
         "youtube_id": "ERRADO"},
        {"canal": "setiap-level", "pacote": "sl-005", "formato": "longo",
         "youtube_id": "CERTO"},
        {"canal": "setiap-level", "pacote": "sl-006", "formato": "longo",
         "youtube_id": "SUMIU"},
    ])
    monkeypatch.setattr(A, "token_do_canal", lambda s, u, k: {})
    monkeypatch.setattr(A, "access_token", lambda t: "x")
    monkeypatch.setattr(A, "canal_real", lambda acc, ids: {
        i: {"ERRADO": ("UC_SETIAP", "Setiap Level"),
            "CERTO": ("UC_SETIAP", "Setiap Level")}[i]
        for i in ids if i in ("ERRADO", "CERTO")})

    ok, erradas, ausentes = A.audita("u", "k")
    assert ok == 1
    assert [e[0]["youtube_id"] for e in erradas] == ["ERRADO"]
    assert [a["youtube_id"] for a in ausentes] == ["SUMIU"]
    assert erradas[0][2] == "setiap-level"


def test_arquivo_estranho_na_pasta_nao_vira_trilha(tmp_path, monkeypatch):
    """O sorteio de trilha divide pelos arquivos PRESENTES.

    Medido em 14/08/2026 no container da sessao: um `bench.mp3` de benchmark
    esquecido em /tmp/trilhas entrava no sorteio e saia escolhido como trilha
    do nivel-do-jogo e do kolejny-poziom. Nunca foi trilha de nada, e o credito
    CC-BY do copy nomearia outra faixa.
    """
    import copy_md as C

    for f in ("Wholesome", "Inspired", "Deliberate_Thought", "bench", "teste_2"):
        (tmp_path / f"{f}.mp3").write_bytes(b"")
    monkeypatch.setattr(C, "TRILHA_DIR", str(tmp_path))

    for slug in ("nivel-do-jogo", "kolejny-poziom", "resep-naik-level",
                 "labtreinamento", "setiap-level", "agla-level"):
        escolhida = C.trilha_do_canal(slug)
        assert os.path.basename(escolhida)[:-4] in C.TRILHAS_VALIDAS, escolhida


def test_so_arquivo_estranho_e_o_mesmo_que_nenhuma_trilha(tmp_path, monkeypatch):
    """Pasta so com lixo tem que devolver None — o frota.yml aborta em zero
    trilhas, e essa e a falha barulhenta que a gente quer."""
    import copy_md as C

    (tmp_path / "bench.mp3").write_bytes(b"")
    monkeypatch.setattr(C, "TRILHA_DIR", str(tmp_path))
    assert C.trilha_do_canal("qualquer") is None


def test_o_credito_segue_a_trilha_registrada_e_nao_o_hash(tmp_path, monkeypatch):
    """O credito CC-BY e o que torna o uso da faixa licenciado.

    Medido em 14/08/2026 no ensaio do resep-naik-level-003: canais.trilha diz
    Deliberate_Thought e o copy.md renderizado creditava Cipher2. O parametro
    `registrada` existia em trilha_do_canal desde 13/08 e ninguem o repassava,
    entao o credito continuava saindo do hash. Nomear a faixa errada e o mesmo
    que nao creditar.
    """
    import copy_md as C

    for f in C.TRILHAS_VALIDAS:
        (tmp_path / f"{f}.mp3").write_bytes(b"")
    monkeypatch.setattr(C, "TRILHA_DIR", str(tmp_path))

    pelo_hash = C.credito_trilha("resep-naik-level")
    registrado = C.credito_trilha("resep-naik-level", None, "Deliberate_Thought")
    assert "Cipher2" in pelo_hash                      # o defeito, reproduzido
    assert "Deliberate Thought" in registrado          # e a correcao


def test_escrever_copy_repassa_a_trilha_da_spec(tmp_path, monkeypatch):
    """A ponta que faltava: quem escreve o copy.md tem que LER sp['trilha'].

    Sem isto a correcao acima fica sendo codigo morto, que foi exatamente o
    estado entre 13 e 14 de agosto.
    """
    import copy_md as C

    trilhas = tmp_path / "t"
    trilhas.mkdir()
    for f in C.TRILHAS_VALIDAS:
        (trilhas / f"{f}.mp3").write_bytes(b"")
    monkeypatch.setattr(C, "TRILHA_DIR", str(trilhas))

    sp = {"slug": "resep-naik-level", "trilha": "Deliberate_Thought",
          "longo": [{"nar": "a", "cap": "um", "kicker": "k"}],
          "copy": "# t\n\n## A\n{TRILHA}\n"}
    d = tmp_path / "wd"
    d.mkdir()
    saida = C.escrever_copy(sp, [10.0], str(d))
    assert "Deliberate Thought" in saida, saida


def test_trilha_declarada_na_spec_tem_que_ser_valida():
    """Nome errado no campo levanta em vez de cair no hash calado."""
    import copy_md as C

    specs = sorted((RAIZ / "fabrica" / "specs").glob("*.json"))
    ruins = []
    for p in specs:
        sp = json.loads(p.read_text(encoding="utf-8"))
        t = sp.get("trilha")
        if t and t not in C.TRILHAS_VALIDAS:
            ruins.append((p.stem, t))
    assert not ruins, ruins
