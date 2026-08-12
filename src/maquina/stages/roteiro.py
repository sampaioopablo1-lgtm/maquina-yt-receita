"""Ideacao e roteirizacao.

Os prompts aqui carregam as regras do playbook: titulo sobre palavra-chave
validada, gancho nos primeiros segundos e densidade de informacao suficiente
para sustentar retencao de 30%.
"""

from __future__ import annotations

import json
import re

from ..config import Config
from ..models import Cena, Formato, Ideia, Roteiro
from ..providers.base import LLM

SISTEMA = """Voce e roteirista de um canal do YouTube subnichado e sem rosto.
Escreve em {idioma}. Tema do canal: {tema}. Tom: {tom}.

Regras inegociaveis:
- Conteudo com valor proprio: informacao concreta, dados, exemplos, uma tese.
  Nunca texto generico ou de preenchimento.
- Nada de "historinha" ficcional rasa (milionario encontra X). Isso e o padrao
  que o YouTube trata como conteudo de baixo valor produzido em massa.
- Perspectiva propria e explicita, nao um apanhado neutro.
- Gancho nos primeiros 15 segundos: promessa concreta do que a pessoa leva.
- Sem promessa de ganho financeiro garantido.

Responda SEMPRE com JSON valido, sem cercas de codigo, sem comentarios."""

PROMPT_IDEIAS = """Gere {n} ideias de video para o canal.
Formato alvo: {formato} ({aspect}, ~{dur_min} min).

Titulos ja publicados neste canal (NAO repita tema nem estrutura):
{publicados}

Palavras-chave que performam no subnicho:
{chaves}

EIXO OBRIGATORIO desta rodada: {eixo}
Todas as ideias devem seguir este eixo estrutural. Ele existe para forcar
variacao real entre videos publicados em sequencia — nao o ignore.

Cada titulo deve usar palavra-chave validada, ser especifico e prometer algo
concreto. Semelhante ao que funciona no nicho, porem melhorado — nunca copia.

JSON: {{"ideias":[{{"titulo":"...","angulo":"...","palavras_chave":["..."]}}]}}"""

PROMPT_ROTEIRO = """Escreva o roteiro completo deste video.

Titulo: {titulo}
Angulo: {angulo}
Formato: {formato} ({aspect})
Duracao alvo: {dur_min} minutos -> aproximadamente {palavras} palavras de narracao.

Estrutura obrigatoria:
1. Gancho (0-15s): promessa concreta.
2. Desenvolvimento: {n_cenas} cenas. Cada cena e um bloco de narracao
   auto-contido de 2 a 4 frases, com UMA ideia clara.
3. Fechamento: sintese + convite a comentar (sem prometer retorno financeiro).

Para cada cena escreva tambem um prompt de imagem em INGLES, seguindo a
identidade visual do canal: "simple doodle illustration, white background,
irregular hand-drawn black lines, minimal color palette (2-3 accent colors),
16:9, no text". Descreva a COMPOSICAO concreta da cena dentro desse estilo.
Varie enquadramento e elementos entre as cenas — sequencia visualmente identica
derruba retencao e caracteriza conteudo de template.

Thumbnail: proponha o prompt de imagem (ingles) e o texto de no maximo 3
palavras que vai no topo, coerente com o titulo.

JSON:
{{"titulo":"...","gancho":"...",
  "cenas":[{{"narracao":"...","prompt_visual":"..."}}],
  "descricao":"...","tags":["..."],
  "prompt_thumbnail":"...","texto_thumbnail":"..."}}"""


def _json_do_llm(bruto: str) -> dict:
    """LLM as vezes devolve cercado por ```json. Extrai o objeto de forma tolerante."""
    texto = bruto.strip()
    texto = re.sub(r"^```(?:json)?\s*|\s*```$", "", texto, flags=re.MULTILINE).strip()
    try:
        return json.loads(texto)
    except json.JSONDecodeError:
        ini, fim = texto.find("{"), texto.rfind("}")
        if ini == -1 or fim <= ini:
            raise ValueError(f"resposta do LLM nao contem JSON:\n{bruto[:500]}")
        return json.loads(texto[ini : fim + 1])


def _sistema(cfg: Config) -> str:
    return SISTEMA.format(
        idioma=cfg.canal.idioma,
        tema=cfg.canal.tema,
        tom=cfg.canal.estilo_narracao,
    )


def proximo_eixo(cfg: Config, ja_publicados: int) -> str:
    """Rotaciona o eixo tematico pela contagem de videos ja publicados.

    Deterministico de proposito: em ritmo diario, sorteio aleatorio repete eixo
    por acaso com frequencia alta. A rotacao garante que N videos seguidos
    percorram N eixos distintos.
    """
    eixos = cfg.canal.eixos_tematicos
    return eixos[ja_publicados % len(eixos)] if eixos else "(livre)"


def gerar_ideias(
    llm: LLM, cfg: Config, formato: Formato, n: int = 5, publicados: list[str] | None = None
) -> list[Ideia]:
    lista_publicados = publicados or []
    prompt = PROMPT_IDEIAS.format(
        n=n,
        formato=formato.value,
        aspect=formato.aspect,
        dur_min=round(formato.duracao_alvo_s / 60, 1),
        publicados="\n".join(f"- {t}" for t in lista_publicados) or "(nenhum ainda)",
        chaves=", ".join(cfg.canal.referencias_titulo) or "(sem referencias cadastradas)",
        eixo=proximo_eixo(cfg, len(lista_publicados)),
    )
    dados = _json_do_llm(llm.completar(prompt, sistema=_sistema(cfg)))
    return [
        Ideia(
            titulo=i["titulo"],
            angulo=i.get("angulo", ""),
            palavras_chave=i.get("palavras_chave", []),
            formato=formato,
        )
        for i in dados["ideias"]
    ]


# Taxa MEDIDA de cada voz, em caracteres por segundo de audio, com numeros por
# extenso e rate -4%. Medir importa: as vozes vao de 9,85 a 20,02 chars/s, e
# dimensionar pela taxa errada e o que ja produziu 9:25 onde se queria 13:00.
# Voz ausente daqui cai no piso conservador — errar para MAIS texto so alonga o
# video, errar para menos o derruba abaixo do piso de 8 min.
CHARS_POR_S = {
    "pt-BR-AntonioNeural": 14.30,
    "pt-BR-ThalitaMultilingualNeural": 16.52,
    "pt-BR-FranciscaNeural": 14.01,
}
CHARS_POR_S_PADRAO = 12.0

# Fracao minima do texto-alvo que o LLM precisa entregar. Abaixo disso o roteiro
# e recusado ANTES de renderizar: render custa ~18 min de runner, e um roteiro
# curto so revela o problema no fim, quando ja gastou tudo.
MIN_FRACAO_TEXTO = 0.75


def _chars_por_s(cfg: Config) -> float:
    return CHARS_POR_S.get(cfg.canal.voz_edge or "", CHARS_POR_S_PADRAO)


def escrever_roteiro(llm: LLM, cfg: Config, ideia: Ideia) -> Roteiro:
    dur_alvo_s = ideia.formato.duracao_alvo_s
    dur_min = dur_alvo_s / 60
    taxa = _chars_por_s(cfg)

    # O alvo e em CARACTERES, nao em palavras: e caractere que o TTS converte em
    # tempo, e a razao palavra/caractere muda com o idioma. O "150 palavras por
    # minuto" que estava aqui era um numero generico de locucao em ingles.
    chars_alvo = int(dur_alvo_s * taxa)
    palavras = int(chars_alvo / 5.5)  # so para orientar o LLM, nao para medir

    # A rotina pede 70-90 cenas no longo. A conta antiga (dur_min * 1.6) dava
    # VINTE cenas para treze minutos — o LLM entregava vinte cenas curtas e o
    # video saia com um terco da duracao.
    n_cenas = 5 if ideia.formato is Formato.SHORTS else max(int(dur_min * 6), 70)

    prompt = PROMPT_ROTEIRO.format(
        titulo=ideia.titulo,
        angulo=ideia.angulo or "(livre)",
        formato=ideia.formato.value,
        aspect=ideia.formato.aspect,
        dur_min=round(dur_min, 1),
        palavras=palavras,
        n_cenas=n_cenas,
    )
    dados = _json_do_llm(
        llm.completar(prompt, sistema=_sistema(cfg), max_tokens=16384)
    )

    cenas = [
        Cena(indice=i, narracao=c["narracao"].strip(), prompt_visual=c["prompt_visual"].strip())
        for i, c in enumerate(dados["cenas"])
    ]
    if not cenas:
        raise ValueError("LLM devolveu roteiro sem cenas")

    # CONFERIR ANTES DE RENDERIZAR. Medido em 2026-08-12 sobre os dez longos que
    # o caminho automatico produziu: mediana de 231 s contra alvo de 780, e nove
    # dos dez abaixo do piso de 8 min. Nenhum foi barrado aqui — todos foram
    # renderizados inteiros e so entao reprovados, ou pior, publicados.
    chars = sum(len(c.narracao) for c in cenas)
    estimado_s = chars / taxa
    if chars < chars_alvo * MIN_FRACAO_TEXTO:
        raise ValueError(
            f"roteiro curto demais: {chars} caracteres para alvo de {chars_alvo} "
            f"({chars / chars_alvo:.0%}), o que da ~{estimado_s / 60:.1f} min contra "
            f"{dur_min:.1f} de alvo, em {len(cenas)} cenas de {n_cenas} pedidas. "
            f"Taxa usada: {taxa} chars/s ({cfg.canal.voz_edge}). "
            "Rejeitado antes de renderizar — render custa ~18 min."
        )

    return Roteiro(
        titulo=dados.get("titulo", ideia.titulo),
        gancho=dados.get("gancho", ""),
        cenas=cenas,
        descricao=dados.get("descricao", ""),
        tags=dados.get("tags", []),
        prompt_thumbnail=dados.get("prompt_thumbnail", ""),
        texto_thumbnail=dados.get("texto_thumbnail", "")[:40],
    )
