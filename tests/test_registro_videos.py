"""A linha em `videos` era o segundo passo manual, e automatizar o primeiro
fez o segundo desaparecer.

Medido em 13/10/2026 as 14:1x: `grava_metricas_janela` levantou

    violates foreign key constraint "metricas_youtube_id_fkey"
    Key (youtube_id)=(CdUiplaeP5g) is not present in table "videos"

As DOZE pecas publicadas hoje nao tinham linha em `videos`. As linhas existem no
banco ate o `labtreinamento-s025` (12/10 23:12) e param ali -- exatamente onde eu
passei a usar o `corpus_atrasado.py` para o outro passo do registro.

Estes testes ancoram nos DOZE notices reais de hoje e nas duas armadilhas que
quase me fizeram reportar errado: o titulo pela forma errada (o `## TITULO`
longo, que custou um fator de dezessete em 00:2x) e a lista de pacotes escrita a
mao, que inventou `kolejny-poziom-s020` e `-s021` -- pacotes que NAO EXISTEM.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "fabrica"))

import registro_videos as RV  # noqa: E402

SPECS = os.path.join(os.path.dirname(__file__), "..", "fabrica", "specs")

# Os doze notices REAIS de 13/10, copiados dos runs do retomar.yml.
NOTICES = """
notice PUBLICADO labtreinamento-s026 shorts youtube_id=CdUiplaeP5g titulo=Mude uma coisa só no seu preço em=2026-10-13T00:15:47Z
notice PUBLICADO labtreinamento-s027 shorts youtube_id=uhhg3nZ1ZEY titulo=Cliente sem retrabalho vale mais em=2026-10-13T01:12:24Z
notice PUBLICADO labtreinamento-s028 shorts youtube_id=UOLpIvPCl58 titulo=Compare com algo que você conhece em=2026-10-13T02:11:09Z
notice PUBLICADO labtreinamento-s029 shorts youtube_id=rWDgoEwwEWY titulo=O trabalho pequeno dói mais em=2026-10-13T03:10:23Z
notice PUBLICADO labtreinamento-s030 shorts youtube_id=UEz0xdb3CL0 titulo=Responda sem decidir nada em=2026-10-13T04:13:15Z
notice PUBLICADO labtreinamento-s031 shorts youtube_id=xwqCqRlE3jg titulo=Não é erro ainda: descarte os casos em=2026-10-13T05:13:14Z
notice PUBLICADO labtreinamento-s032 shorts youtube_id=vHknlJnkUNA titulo=Decida pela possibilidade, não pela escala em=2026-10-13T06:16:47Z
notice PUBLICADO epomeno-epipedo-s020 shorts youtube_id=Q_1v7ZoBgiI titulo=Το ενοίκιο δεν είναι το κόστος στέγης em=2026-10-13T07:19:05Z
notice PUBLICADO epomeno-epipedo-s021 shorts youtube_id=6AZoMTvq6wc titulo=Το ποσοστό δεν είναι το ποσό σου em=2026-10-13T08:15:31Z
notice PUBLICADO kolejny-poziom-s022 shorts youtube_id=PNWT8JndFWc titulo=Podwyżka przed wnioskiem nic nie dała em=2026-10-13T09:17:59Z
notice PUBLICADO epomeno-epipedo-s022 shorts youtube_id=AW6pabY2Dw4 titulo=Πάρε τις κιλοβατώρες, όχι τα ευρώ em=2026-10-13T11:13:11Z
notice PUBLICADO epomeno-epipedo-s023 shorts youtube_id=8xBNUQ3qTmk titulo=Το όριο δεν μετράει αν ζεις em=2026-10-13T13:13:22Z
"""


def test_le_as_DOZE_publicacoes_reais_de_hoje():
    assert len(RV.linhas_dos_notices(NOTICES)) == 12


def test_TODAS_saem_com_origem_id_porque_e_isso_que_o_670_pede():
    for l in RV.linhas_dos_notices(NOTICES):
        assert l["origem_id"], l["slug"]


def test_o_slug_e_pacote_mais_short_como_as_linhas_que_ja_existem():
    l = RV.linhas_dos_notices(NOTICES)[0]
    assert l["slug"] == "labtreinamento-s026-short"
    assert l["pacote"] == "labtreinamento-s026"


def test_o_canal_vem_da_SPEC_e_nao_do_prefixo_do_pacote():
    # `epomeno-epipedo-s020` tem canal `epomeno-epipedo`; cortar o pacote por
    # "-" daria `epomeno`, e a linha entraria no canal errado.
    por_pac = {l["pacote"]: l for l in RV.linhas_dos_notices(NOTICES)}
    assert por_pac["epomeno-epipedo-s020"]["canal"] == "epomeno-epipedo"
    assert por_pac["kolejny-poziom-s022"]["canal"] == "kolejny-poziom"


def test_o_titulo_e_o_TITULO_SHORT_e_nao_o_titulo_longo_da_copy():
    # O erro de 00:2x, que custou um fator de dezessete pecas: o corpus e a
    # linha de `videos` guardam o titulo que o YouTube recebe.
    import json
    p = os.path.join(SPECS, "epomeno-epipedo-s023.json")
    spec = json.load(open(p, encoding="utf-8"))
    curto = RV.titulo_short(spec)
    longo = spec["copy"].split("## TITULO")[1].split("##")[0].strip()
    assert curto and curto != longo
    assert len(curto) <= 45


def test_notice_de_run_abortado_NAO_entra():
    ruim = ("notice PUBLICADO labtreinamento-s026 shorts youtube_id=? "
            "titulo=Mude uma coisa só no seu preço em=2026-10-13T00:15:47Z")
    assert RV.linhas_dos_notices(ruim) == []


def test_pacote_sem_spec_NAO_entra_em_vez_de_inventar_linha():
    # `kolejny-poziom-s020` nao existe -- foi a minha lista a mao que o
    # inventou as 14:1x, e o efeito (C) da rotina outra vez.
    ruim = ("notice PUBLICADO kolejny-poziom-s020 shorts youtube_id=XXXXXXXXXXX "
            "titulo=Inventado em=2026-10-12T20:00:00Z")
    assert RV.linhas_dos_notices(ruim) == []
    assert not os.path.exists(os.path.join(SPECS, "kolejny-poziom-s020.json"))


def test_o_sql_tem_on_conflict_para_reexecutar_sem_estrago():
    sql = RV.sql_insert(RV.linhas_dos_notices(NOTICES))
    assert "on conflict (slug) do nothing" in sql
    assert sql.count("(") >= 13      # 12 tuplas + a lista de colunas


def test_o_sql_escapa_apostrofo_em_vez_de_quebrar_o_statement():
    linhas = [{"slug": "x-short", "status": "publicado", "formato": "shorts",
               "titulo": "O que n'ao vai", "youtube_id": "y", "canal": "c",
               "pacote": "x", "origem_id": "o", "cenas": 9,
               "publicado_em": "2026-10-13T00:00:00Z", "trilha": "t"}]
    assert "n''ao" in RV.sql_insert(linhas)


def test_sem_linhas_o_relato_AVISA_em_vez_de_calar():
    r = RV.relato([])
    assert "NAO existe" in r and "chave estrangeira" in r


def test_o_modulo_NAO_executa_sql_sozinho():
    fonte = open(os.path.join(os.path.dirname(__file__), "..", "fabrica",
                              "registro_videos.py"), encoding="utf-8").read()
    for proibido in ("execute_sql", "psycopg", "requests.post", "http_post"):
        assert proibido not in fonte.split('"""')[2], proibido
