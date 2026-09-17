"""O `copy` das specs e markdown; `publicar.py` so aceitava dict.

`cp["titulo"]` num str e TypeError, entao o passo "Publicar no YouTube" do
frota.yml nunca completou com nenhuma das 22 specs versionadas — o render de 13
minutos terminava e a publicacao morria na primeira linha.

Estes testes rodam contra as specs REAIS do repositorio, em sete idiomas, porque
o parse nao pode depender de cabecalho traduzido: as secoes se chamam TITULO,
TITLE, TÍTULO, ΤΙΤΛΟΣ, TYTUŁ e BAŞLIK, e as specs antigas tem 5 secoes em ordem
diferente das novas, que tem 9.
"""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parents[1]
SPECS = sorted((RAIZ / "fabrica" / "specs").glob("*.json"))


def _publicar():
    spec = importlib.util.spec_from_file_location(
        "fab_publicar", RAIZ / "fabrica" / "publicar.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


pub = _publicar()


def _fabrica():
    """copy_md.py: capitulos e copy.md, sem a stack de render.

    Este helper injetava cairosvg e edge_tts falsos em sys.modules para
    conseguir importar fabrica.py. Contornar em teste o que trava em producao
    esconde o defeito: o mesmo import derrubou o job de reparo de descricao
    (run 31656308340) em 13/08/2026. As funcoes sairam para um modulo proprio.
    """
    spec = importlib.util.spec_from_file_location("copy_md", RAIZ / "fabrica" / "copy_md.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


fab = _fabrica()


@pytest.fixture(autouse=True)
def _trilhas_presentes(tmp_path_factory, monkeypatch):
    """As tres faixas do portfolio, presentes como na esteira.

    Desde 25/08/2026 `escrever_copy` RECUSA gravar o copy.md quando a spec
    declara trilha e o mp3 nao esta em TRILHA_DIR (test_copy_sem_trilha_recusa):
    era assim que o credito CC-BY sumia calado. Na esteira o frota.yml baixa as
    faixas antes; aqui ninguem baixava, e os 221 casos que passam pelo
    `escrever_copy` morriam no runner com "nenhum mp3 valido esta em
    /tmp/trilhas" (run 33815263984). Sem `valida`, a faixa e listada pelo
    nome, entao arquivo vazio basta — o mesmo que test_prontidao ja faz.
    """
    d = tmp_path_factory.mktemp("trilhas")
    for f in fab.TRILHAS_VALIDAS:
        (d / f"{f}.mp3").write_bytes(b"")
    monkeypatch.setattr(fab, "TRILHA_DIR", str(d))


def _copy_renderizado(spec, destino, dur_cena=15.0):
    """Escreve o copy.md como o render escreveria, com capitulos cronometrados."""
    fab.escrever_copy(spec, [dur_cena] * len(spec["longo"]), str(destino))


def _com_copy_markdown():
    """Specs cujo `copy` traz as secoes de fato.

    Cinco specs guardam ali so um bilhete ("gerado a partir dos capitulos reais
    apos o render") — para elas o copy.md do render nao e preferencia, e
    requisito, e o teste disso e o _exige_copy_md abaixo.
    """
    for caminho in SPECS:
        dados = json.loads(caminho.read_text(encoding="utf-8"))
        copy = dados.get("copy")
        if isinstance(copy, str) and copy.count("\n## ") >= 2:
            yield pytest.param(caminho, id=caminho.stem)


def _so_bilhete():
    for caminho in SPECS:
        dados = json.loads(caminho.read_text(encoding="utf-8"))
        copy = dados.get("copy")
        if isinstance(copy, str) and copy.strip() and copy.count("\n## ") < 2:
            yield pytest.param(caminho, id=caminho.stem)


@pytest.mark.parametrize("caminho", list(_so_bilhete()))
def test_spec_sem_secoes_exige_o_copy_md_em_vez_de_publicar_o_bilhete(caminho, tmp_path):
    """"gerado a partir dos capitulos reais apos o render" nao e uma descricao.

    O codigo antigo publicaria essa frase como descricao do video sem reclamar.
    """
    spec = json.loads(caminho.read_text(encoding="utf-8"))

    with pytest.raises(SystemExit, match="copy.md"):
        pub.ler_copy(spec, str(tmp_path))


@pytest.mark.parametrize("caminho", list(_com_copy_markdown()))
def test_toda_spec_do_repo_rende_titulo_e_descricao(caminho, tmp_path):
    spec = json.loads(caminho.read_text(encoding="utf-8"))
    _copy_renderizado(spec, tmp_path)

    cp = pub.ler_copy(spec, str(tmp_path))

    assert cp["titulo"], "titulo vazio publicaria video sem nome"
    assert len(cp["titulo"]) <= 100, "o YouTube corta em 100"
    assert "\n" not in cp["titulo"]
    assert len(cp["descricao"]) > 200, "a rotina pede 200+ palavras de descricao"


@pytest.mark.parametrize("caminho", list(_com_copy_markdown()))
def test_nenhum_placeholder_vaza_para_a_descricao(caminho, tmp_path):
    """`{CAPITULOS}` literal na descricao do YouTube e o defeito visivel.

    Aconteceu de verdade em 13/08/2026 com o seviye-seviye-002, para os
    assinantes do canal.
    """
    spec = json.loads(caminho.read_text(encoding="utf-8"))
    _copy_renderizado(spec, tmp_path)

    cp = pub.ler_copy(spec, str(tmp_path))

    assert "{" not in cp["descricao"] or "PLACEHOLDER" not in cp["descricao"].upper()
    assert "{CAPITULOS}" not in cp["descricao"]
    assert "{TRILHA}" not in cp["descricao"]


def test_o_copy_md_do_render_vence_a_spec(tmp_path):
    """O render substitui {CAPITULOS} pelos tempos medidos nos clipes.

    A spec tem so o placeholder, entao publicar dela poria "{CAPITULOS}" na
    descricao do video. A ordem das fontes e o que evita isso.
    """
    spec = {"copy": "# T\n\n## TITULO\nDa spec\n\n## DESCRICAO\n" + "x" * 250}
    (tmp_path / "copy.md").write_text(
        "# T\n\n## BAŞLIK\nDo render\n\n## AÇIKLAMA\n" + "y" * 250
        + "\n\n## BÖLÜMLER\n0:00 Giris\n1:30 Bolum 1\n",
        encoding="utf-8",
    )

    cp = pub.ler_copy(spec, str(tmp_path))

    assert cp["titulo"] == "Do render"
    assert "0:00 Giris" in cp["descricao"], "capitulos cronometrados entram na descricao"


def test_capitulos_reais_entram_na_descricao(tmp_path):
    (tmp_path / "copy.md").write_text(
        "# T\n\n## TITLE\nT\n\n## DESCRIPTION\n" + "d" * 250
        + "\n\n## CHAPTERS\n0:00 Intro\n2:14 Part 1\n11:40 Close\n"
        "\n## HASHTAGS\n#a #b #c\n\n## TAGS\numa, duas, tres, quatro\n",
        encoding="utf-8",
    )

    cp = pub.ler_copy({}, str(tmp_path))

    assert "11:40 Close" in cp["descricao"]
    assert cp["tags"] == ["uma", "duas", "tres", "quatro"]
    assert cp["hashtags"] == "#a #b #c"


def test_hashtag_nao_e_confundida_com_tag(tmp_path):
    """As duas secoes sao uma linha so; o que separa e o `#`."""
    (tmp_path / "copy.md").write_text(
        "# T\n\n## BAŞLIK\nT\n\n## AÇIKLAMA\n" + "d" * 250
        + "\n\n## ETİKETLER\n#AsgariUcret #Enflasyon #SeviyeSeviye\n"
        "\n## TAGS\nasgari ücret 2026, açlık sınırı, tüik, enflasyon\n",
        encoding="utf-8",
    )

    cp = pub.ler_copy({}, str(tmp_path))

    assert cp["tags"][0] == "asgari ücret 2026"
    assert not any(t.startswith("#") for t in cp["tags"])


def test_dict_continua_funcionando(tmp_path):
    """Specs futuras podem trazer copy ja estruturado — nao quebrar quem migrar."""
    cp = pub.ler_copy({"copy": {"titulo": "T", "descricao": "D", "tags": ["a"]}},
                      str(tmp_path))

    assert cp["titulo"] == "T"


def test_sem_copy_nenhum_e_erro_claro(tmp_path):
    with pytest.raises(SystemExit, match="sem copy"):
        pub.ler_copy({}, str(tmp_path))


def test_orcamento_de_tags_conta_as_aspas():
    """O limite de 500 conta tag com espaco entre aspas (len+2); somar so os
    caracteres aprova lista que o YouTube rejeita."""
    tags = ["com espaco"] * 60

    mantidas, total = pub.orcamento_tags(tags)

    assert total <= 480
    assert all(len(t) + 2 for t in mantidas)


def test_a_spec_do_seviye_002_esta_publicavel(tmp_path):
    """O pacote da vez: seviye-seviye-002, asgari ucret x aclik siniri."""
    spec = json.loads(
        (RAIZ / "fabrica" / "specs" / "seviye-seviye-002.json").read_text(encoding="utf-8")
    )

    assert spec.get("pacote") == "seviye-seviye-002", "frota.yml resolve o workdir por `pacote`"
    assert spec.get("idioma") == "tr"
    _copy_renderizado(spec, tmp_path)

    cp = pub.ler_copy(spec, str(tmp_path))

    assert cp["titulo"].startswith("Asgari ücret")
    assert len(cp["tags"]) == 15
    mantidas, total = pub.orcamento_tags(cp["tags"])
    assert total <= 480, f"orcamento estourado: {total}"


# ---------- reparo de pacote ja publicado ----------

def test_placeholder_nao_publica_mais(tmp_path):
    """O aviso "copy.md ausente" existia e nao impediu nada.

    Em 13/08/2026 o seviye-seviye-002 subiu com "{CAPITULOS}" literal para os
    assinantes. Um run que falha se refaz em treze minutos; descricao quebrada
    no ar so sai se alguem perceber.
    """
    spec = {"copy": "# T\n\n## TITULO\nT\n\n## DESCRICAO\n" + "d" * 250
                    + "\n\n## CAPITULOS\n{CAPITULOS}\n"}

    with pytest.raises(SystemExit, match=r"\{CAPITULOS\}"):
        pub.ler_copy(spec, str(tmp_path))


def test_tempos_saem_do_srt_quando_o_tempos_json_morreu(tmp_path):
    """O runner e efemero e leva o tempos.json junto; o .srt vai para o Storage.

    Os dois carregam a mesma informacao, entao o reparo nao precisa repetir
    treze minutos de render so para recalcular capitulos.
    """
    srt = tmp_path / "legendas.srt"
    srt.write_text(
        "1\n00:00:00,150 --> 00:00:09,850\ncena um\n\n"
        "2\n00:00:10,150 --> 00:00:24,850\ncena dois\n\n"
        "3\n00:00:25,150 --> 00:00:30,850\ncena tres\n\n",
        encoding="utf-8",
    )

    tempos = pub.tempos_do_srt(str(srt))

    assert tempos == pytest.approx([10.0, 15.0, 6.0], abs=0.01)
    assert sum(tempos) == pytest.approx(31.0, abs=0.01)


def test_srt_sem_bloco_de_tempo_e_erro_claro(tmp_path):
    vazio = tmp_path / "legendas.srt"
    vazio.write_text("nao e legenda", encoding="utf-8")

    with pytest.raises(SystemExit, match="bloco de tempo"):
        pub.tempos_do_srt(str(vazio))


def test_capitulos_do_seviye_002_batem_com_a_duracao_real():
    """Capítulo depois do fim do video seria pior que nao ter capitulo."""
    import json as _json

    spec = _json.loads(
        (RAIZ / "fabrica" / "specs" / "seviye-seviye-002.json").read_text(encoding="utf-8")
    )
    tempos = [15.0] * len(spec["longo"])          # ~13 min no total

    caps = fab.capitulos(spec, tempos)

    assert caps[0].startswith("0:00"), "o YouTube exige que o primeiro seja 0:00"
    assert len(caps) >= 6, "6-8 capitulos e o que a rotina pede num longo"
    minutos = [int(c.split(":")[0]) for c in caps]
    assert minutos == sorted(minutos), "capitulos fora de ordem invalidam a lista inteira"
    assert minutos[-1] * 60 < sum(tempos), "capitulo depois do fim do video"


def test_copy_md_nao_arrasta_a_stack_de_render():
    """Formatar markdown nao pode exigir cairosvg.

    O job de reparo de descricao morreu com ModuleNotFoundError importando
    fabrica.py para chamar uma funcao que so conta segundos e junta texto.
    """
    import ast

    arvore = ast.parse((RAIZ / "fabrica" / "copy_md.py").read_text(encoding="utf-8"))
    importados = set()
    for no in ast.walk(arvore):
        if isinstance(no, ast.Import):
            importados.update(a.name.split(".")[0] for a in no.names)
        elif isinstance(no, ast.ImportFrom) and no.module:
            importados.add(no.module.split(".")[0])

    assert importados <= {"glob", "os", "__future__"}, (
        f"copy_md.py so pode usar a biblioteca padrao leve; achei {importados}")


# ---------------------------------------------------------------------------
# Trava contra republicacao.
#
# Em 13/08/2026 eu contei quinze specs como "prontas para disparar" olhando so
# os portoes do prontidao.py — e dez delas ja estavam no ar desde 05/08
# (setiap-level-003/004/005, agla-level-003, epomeno-epipedo-002,
# game-money-lab-002, resep-naik-level-002, kolejny-poziom-007,
# labtreinamento-001, seja-mais-magra-001). Disparar aquela lista teria posto
# duplicata em dez canais.
#
# A spec no repositorio nao carrega youtube_id, entao nenhuma leitura de spec
# resolve isso. So o banco sabe — e a pergunta tem que sair de dentro do
# publicar.py, que e o unico ponto por onde toda publicacao passa.

def test_ja_publicado_devolve_ids_por_formato(monkeypatch):
    import io
    import json as _json

    chamadas = []

    def _falso_req(url, **kw):
        chamadas.append(url)
        return io.BytesIO(_json.dumps([
            {"formato": "longo", "youtube_id": "v-5v7R13BBc"},
            {"formato": "shorts", "youtube_id": "ZYh3bpLP5JE"},
        ]).encode())

    monkeypatch.setattr(pub, "_req", _falso_req)
    vivos = pub.ja_publicado("setiap-level-004", "https://sb", "chave")

    assert vivos == {"longo": "v-5v7R13BBc", "shorts": "ZYh3bpLP5JE"}
    # O filtro tem que excluir linha sem youtube_id: um pacote registrado com
    # erro, sem id, NAO conta como publicado e precisa poder subir.
    assert "youtube_id=not.is.null" in chamadas[0]
    assert "pacote=eq.setiap-level-004" in chamadas[0]


def test_ja_publicado_vazio_quando_nada_foi_ao_ar(monkeypatch):
    import io

    monkeypatch.setattr(pub, "_req", lambda url, **kw: io.BytesIO(b"[]"))
    assert pub.ja_publicado("sx-educacao-001", "https://sb", "chave") == {}


def test_pacote_com_barra_ou_espaco_nao_quebra_a_query(monkeypatch):
    """O nome do pacote entra na URL: sem quote, um caractere estranho viraria
    outro filtro e a consulta responderia sobre o pacote errado — devolvendo
    vazio e liberando a republicacao."""
    import io

    vistos = []
    monkeypatch.setattr(pub, "_req",
                        lambda url, **kw: (vistos.append(url), io.BytesIO(b"[]"))[1])
    pub.ja_publicado("nome com espaco/e-barra", "https://sb", "chave")
    assert " " not in vistos[0] and "espaco%2Fe-barra" in vistos[0]
