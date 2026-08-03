"""Providers offline deterministicos.

Nao sao mocks de teste: eles produzem assets reais (audio com duracao correta,
imagem PNG de verdade) para que a pipeline inteira — inclusive o render do
ffmpeg — possa ser executada e validada sem nenhuma chave de API. E o que
permite `maquina run --dry-run` funcionar no CI.
"""

from __future__ import annotations

import hashlib
import json
import textwrap
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from .. import media

# Ritmo medio de narracao usado para estimar duracao sem TTS real.
PALAVRAS_POR_MINUTO = 150


class LLMStub:
    """Devolve JSON com a forma que a etapa espera, derivado do prompt."""

    custo_usd = 0.0

    def completar(self, prompt: str, *, sistema: str = "", max_tokens: int = 4096) -> str:
        semente = hashlib.sha1(prompt.encode()).hexdigest()

        if '"ideias"' in prompt or "ideias" in prompt.lower()[:200]:
            return json.dumps(
                {
                    "ideias": [
                        {
                            "titulo": f"Pauta de exemplo {semente[:4]} — {i}",
                            "angulo": "angulo gerado offline para validar a pipeline",
                            "palavras_chave": ["exemplo", "offline", "stub"],
                        }
                        for i in range(1, 6)
                    ]
                },
                ensure_ascii=False,
            )

        # Roteiro: numero de cenas suficiente para exercitar concat e legendas.
        cenas = [
            {
                "narracao": (
                    f"Bloco {i} do roteiro de validacao offline. "
                    "Este texto existe para exercitar a sintese de audio, o "
                    "calculo de duracao e a sincronizacao das legendas."
                ),
                "prompt_visual": f"cena {i}: composicao abstrata, tom sobrio, sem texto",
            }
            for i in range(1, 7)
        ]
        return json.dumps(
            {
                "titulo": f"Titulo de validacao {semente[:6]}",
                "gancho": "Gancho de abertura gerado offline.",
                "cenas": cenas,
                "descricao": "Descricao gerada pelo provider offline.",
                "tags": ["stub", "offline"],
                "prompt_thumbnail": "fundo sobrio, figura central, espaco para texto no topo",
                "texto_thumbnail": "EXEMPLO",
            },
            ensure_ascii=False,
        )


class TTSStub:
    """Gera silencio com a duracao que a narracao teria."""

    custo_usd = 0.0

    def sintetizar(self, texto: str, saida: Path, *, voice_id: str = "") -> Path:
        palavras = max(len(texto.split()), 1)
        segundos = max(palavras / PALAVRAS_POR_MINUTO * 60, 1.5)
        return media.silencio(saida, segundos)


class ImagemStub:
    """PNG real com gradiente deterministico + o prompt escrito, para conferencia visual."""

    custo_usd = 0.0

    def gerar(self, prompt: str, saida: Path, *, largura: int, altura: int) -> Path:
        h = hashlib.sha1(prompt.encode()).digest()
        topo = (h[0] // 2 + 20, h[1] // 2 + 20, h[2] // 2 + 20)
        base = (h[3] // 3, h[4] // 3, h[5] // 3)

        img = Image.new("RGB", (largura, altura), topo)
        d = ImageDraw.Draw(img)
        for y in range(altura):
            t = y / max(altura - 1, 1)
            d.line(
                [(0, y), (largura, y)],
                fill=tuple(int(topo[i] * (1 - t) + base[i] * t) for i in range(3)),
            )

        try:
            fonte = ImageFont.truetype(
                "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", max(largura // 34, 14)
            )
        except OSError:
            fonte = ImageFont.load_default()

        texto = "\n".join(textwrap.wrap(prompt, width=34)[:6])
        d.multiline_text(
            (largura // 2, altura // 2),
            texto,
            fill=(245, 245, 245),
            font=fonte,
            anchor="mm",
            align="center",
            spacing=10,
        )
        saida.parent.mkdir(parents=True, exist_ok=True)
        img.save(saida, "PNG")
        return saida
