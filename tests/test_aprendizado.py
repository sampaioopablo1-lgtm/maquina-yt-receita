"""O laco que fecha: o que o acervo provou volta para a producao.

Ate 20/08/2026 a maquina tinha memoria da PESQUISA e nao tinha memoria do
RESULTADO. `v_maquina_formatos` guarda o que os concorrentes fazem e decide
pauta desde o primeiro disparo. O espelho disso sobre o proprio acervo nao
existia: 152 videos no ar, 1.932 linhas em `metricas`, e nenhuma linha do
caminho de decisao lendo qualquer uma delas.

Estes testes cercam o que falha em silencio num laco de aprendizado:
indisponibilidade lida como "nada a relatar", veredito que nao chega ao prompt,
e decisao tomada sobre coluna que ninguem mediu.
"""
from __future__ import annotations

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "fabrica"))

import aprendizado as A  # noqa: E402
import autor  # noqa: E402


def _licao(**kw):
    base = {"canal": "teste", "shorts_medidos": 6, "longos_medidos": 6,
            "short_vd_mediana": 81.5, "longo_vd_mediana": 4.6,
            "short_vd_topo": 224.0, "veredito_longo": "liberado",
            "views_total": 2320}
    base.update(kw)
    return base


# ------------------------------------------------------------- o veredito

def test_todo_veredito_tem_acao_escrita():
    """Veredito sem acao e relatorio, nao decisao. Se um veredito novo entrar
    na view sem entrar aqui, o prompt recebe o rotulo e nenhuma instrucao."""
    for v in ("suspenso", "canal frio", "liberado", "sem dado"):
        assert v in A.ACAO and len(A.ACAO[v]) > 40, v


def test_suspenso_manda_o_melhor_material_para_o_short():
    assert "SHORT" in A.ACAO["suspenso"]
    assert "8 min" in A.ACAO["suspenso"]


def test_canal_frio_nao_manda_trocar_de_formato():
    """Canal frio e o caso em que NENHUM formato pegou. Mandar produzir so
    short ali responde a pergunta errada."""
    assert "gancho" in A.ACAO["canal frio"]
    assert "eixo novo" in A.ACAO["canal frio"]


# ------------------------------------------------------------- a memoria

def test_a_memoria_carrega_o_veredito_em_maiuscula(monkeypatch):
    monkeypatch.setattr(A, "licoes", lambda u, k, s="": [_licao(veredito_longo="suspenso")])
    monkeypatch.setattr(A, "melhores", lambda u, k, s, n=5: [])
    monkeypatch.setattr(A, "desempenho", lambda u, k, s="": [])
    txt = A.memoria("u", "k", "teste")
    assert "VEREDITO: SUSPENSO" in txt
    assert A.ACAO["suspenso"][:30] in txt


def test_a_memoria_traz_os_titulos_que_performaram(monkeypatch):
    """Titulo real do proprio canal e o unico exemplo que ja passou por ESTE
    publico — vale mais que qualquer descricao de formato."""
    monkeypatch.setattr(A, "licoes", lambda u, k, s="": [_licao()])
    monkeypatch.setattr(A, "melhores", lambda u, k, s, n=5: [
        {"titulo": "Asgari ucret", "formato": "shorts", "vd": 224.0},
        {"titulo": "Maas hesabi", "formato": "longo", "vd": 4.6}])
    monkeypatch.setattr(A, "desempenho", lambda u, k, s="": [])
    txt = A.memoria("u", "k", "teste")
    assert "Asgari ucret" in txt and "224.0" in txt


def test_canal_sem_licao_devolve_vazio_e_nao_texto_falso(monkeypatch):
    monkeypatch.setattr(A, "licoes", lambda u, k, s="": [])
    assert A.memoria("u", "k", "teste") == ""


# --------------------------------------------- indisponivel != nada a relatar

def test_memoria_indisponivel_avisa_o_gerador(monkeypatch):
    """A diferenca entre "nao ha licao" e "nao consegui ler a licao" e enorme.
    Se a falha passar calada, o gerador decide como se o canal nada tivesse
    provado — e escreve exatamente o que ja falhou.

    `titulos_publicados` e stubado porque ele NAO tem essa protecao, e de
    proposito: ele alimenta a checagem de similaridade, e escrever sem saber o
    que ja foi publicado arrisca um titulo duplicado. Ali falhar duro e o
    comportamento certo.
    """
    def explode(*a, **k):
        raise RuntimeError("banco fora")

    monkeypatch.setattr(autor, "titulos_publicados", lambda *a, **k: [])
    monkeypatch.setattr(A, "memoria", explode)
    ctx = autor.contexto("labtreinamento", "http://x", "chave")
    assert "INDISPONIVEL" in ctx["memoria_propria"]
    assert "conservador" in ctx["memoria_propria"]


def test_falha_da_memoria_nao_derruba_a_geracao(monkeypatch):
    def explode(*a, **k):
        raise RuntimeError("banco fora")

    monkeypatch.setattr(autor, "titulos_publicados", lambda *a, **k: [])
    monkeypatch.setattr(A, "memoria", explode)
    ctx = autor.contexto("labtreinamento", "http://x", "chave")
    assert ctx["voz"] and ctx["paleta"]      # o resto do contexto sobreviveu


# ------------------------------------------------------ o laco chega ao prompt

def test_a_memoria_propria_entra_no_pedido():
    ctx = autor.contexto("labtreinamento")
    ctx["memoria_propria"] = "VEREDITO: SUSPENSO. marcador-unico-do-teste"
    assert "marcador-unico-do-teste" in autor._pedido(ctx, "pauta", 80, 9000)


def test_o_prompt_diz_qual_memoria_vence():
    """Duas memorias que discordam sem regra de desempate produzem escolha
    arbitraria — e a arbitraria costuma ser a do nicho, que e maior."""
    assert "PROPRIA vence" in autor.SISTEMA
    assert "VEREDITO" in autor.SISTEMA


# ------------------------------------------------- so o que foi medido decide

def test_o_modulo_nao_decide_por_coluna_nao_medida():
    """ctr, impressoes, retencao, inscritos e receita estao em `metricas` e sao
    default: nenhum dos treze tokens tem escopo yt-analytics.readonly. Decidir
    com elas repetiria o defeito que models.py registrou em 13/08 — "o painel
    inteiro parecia dado e era default"."""
    fonte = (RAIZ / "fabrica" / "aprendizado.py").read_text(encoding="utf-8")
    corpo = "\n".join(l for l in fonte.splitlines()
                      if not l.strip().startswith("#"))
    corpo = corpo.split('"""', 2)[-1]          # fora o docstring do modulo
    for coluna in ("ctr", "impressoes", "retencao_media_pct",
                   "inscritos_ganhos", "receita_estimada_usd"):
        assert coluna not in corpo, f"{coluna} nao foi medida e nao pode decidir"


def test_idade_minima_e_a_mesma_regra_da_rotina():
    """48h — a regra existe porque o contador do YouTube atualiza em lote
    (aprendizado 360)."""
    assert A.IDADE_MINIMA_H == 48


# ----------------------------------------------------------- a retencao

def _desemp(**kw):
    base = {"canal": "teste", "formato": "shorts", "n": 9, "vd_mediana": 46.88,
            "ret_n": 2, "ret_mediana_pct": 35.5, "ret_dur_mediana_s": 13}
    base.update(kw)
    return base


def test_retencao_entra_na_memoria_com_o_n_ao_lado(monkeypatch):
    """Numero sem n vira certeza falsa no prompt: uma mediana calculada sobre
    UM video le-se igual a uma calculada sobre trinta. Doze dos 629 videos
    coletados tem retencao — e indicio, e tem de chegar ao gerador como tal."""
    monkeypatch.setattr(A, "licoes", lambda u, k, s="": [_licao()])
    monkeypatch.setattr(A, "melhores", lambda u, k, s, n=5: [])
    monkeypatch.setattr(A, "desempenho", lambda u, k, s="": [_desemp()])
    txt = A.memoria("u", "k", "teste")
    assert "35.5%" in txt
    assert "2 medido(s)" in txt
    assert "indicio" in txt


def test_sem_retencao_medida_a_memoria_nao_inventa_secao(monkeypatch):
    monkeypatch.setattr(A, "licoes", lambda u, k, s="": [_licao()])
    monkeypatch.setattr(A, "melhores", lambda u, k, s, n=5: [])
    monkeypatch.setattr(A, "desempenho", lambda u, k, s="": [_desemp(ret_n=0)])
    txt = A.memoria("u", "k", "teste")
    assert "COMO LER A RETENCAO" not in txt
    assert "VEREDITO" in txt


def test_desempenho_fora_do_ar_nao_derruba_a_memoria(monkeypatch):
    """O veredito e o que muda o roteiro; a retencao e ornamento. Perder o
    bloco inteiro porque a consulta secundaria caiu seria trocar um pelo
    outro."""
    def explode(*a, **k):
        raise RuntimeError("banco fora")

    monkeypatch.setattr(A, "licoes", lambda u, k, s="": [_licao()])
    monkeypatch.setattr(A, "melhores", lambda u, k, s, n=5: [])
    monkeypatch.setattr(A, "desempenho", explode)
    assert "VEREDITO: LIBERADO" in A.memoria("u", "k", "teste")


def test_a_memoria_explica_como_ler_a_retencao(monkeypatch):
    """Retencao alta com views baixo e distribuicao; retencao baixa com views
    baixo e roteiro. O gerador nao deduz isso sozinho — e escrito."""
    monkeypatch.setattr(A, "licoes", lambda u, k, s="": [_licao()])
    monkeypatch.setattr(A, "melhores", lambda u, k, s, n=5: [])
    monkeypatch.setattr(A, "desempenho", lambda u, k, s="": [_desemp()])
    txt = A.memoria("u", "k", "teste")
    assert "distribuicao" in txt and "roteiro" in txt
    assert "100%" in txt
