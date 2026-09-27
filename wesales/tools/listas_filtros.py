"""Filtros das listas inteligentes no formato que a TELA do GHL usa (registrado em 27/09
aplicando cada filtro pela tela e lendo o corpo de POST /contacts/search/2). O formato da
API pública (/contacts/search) é outro, e a tela descarta o que não reconhece."""
PIPE, CONECTAR = "0Fo2xbeayE4EP6yuSUtq", "deb60542-a5cd-43ae-b875-b467b120a72c"


def etapa(stage):
    # Sem `status` dentro do grupo: a tela desmonta o grupo se ele tiver `status` (vira um
    # filtro solto inválido e a lista mostra 0). Aberto/perdido sai pela tag `status-perdido`
    # (aplicada pelo Espelho de Etapa), que a tela entende.
    return {"field": "opportunities", "operator": "nested", "value": [{"group": "AND", "filters": [
        {"field": "pipeline_id", "operator": "eq", "value": PIPE, "uiMeta": {"fieldAlias": "pipeline_stage"}},
        {"group": "AND", "filters": [{"field": "pipeline_stage_id", "operator": "eq", "value": stage,
                                     "uiMeta": {"fieldAlias": "stage_id"}}]}]}],
        "uiMeta": {"isDependantFilterGroup": True}}


def sem_tag(tag):
    return {"field": "tags", "operator": "not_eq", "value": [tag], "options": {"minimumMatch": "all"}}


def com_tag(tag):
    return {"field": "tags", "operator": "eq", "value": [tag], "options": {"minimumMatch": "all"}}


def cf_min(cid, n):
    """Campo >= n para inteiros, como lista de filtros. A tela recusa o `range` que a busca
    aceita (422 "Invalid value for 'range'"), então vira: preenchido e != 0..n-1."""
    f = "custom_fields." + cid
    return [{"field": f, "operator": "exists"}] + [
        {"field": f, "operator": "not_eq", "value": v} for v in range(n)]


def cf_vazio_ou_zero(cid):
    return {"group": "OR", "filters": [{"field": "custom_fields." + cid, "operator": "not_exists"},
                                       {"field": "custom_fields." + cid, "operator": "eq", "value": 0}]}


def envelope(filtros):
    return [{"group": "AND", "filters": [{"group": "AND", "filters": filtros}]}]
