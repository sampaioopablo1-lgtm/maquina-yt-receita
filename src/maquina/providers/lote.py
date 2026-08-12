"""Provider de narracao em lote — voz clonada gratuita via Colab.

O caminho gratuito e sem conector: o Chatterbox-TTS-Indonesian (Apache 2.0,
clonagem zero-shot por audio prompt) roda no Colab com GPU T4 gratuita e gera
as narracoes de cada cena com a voz de referencia do operador. Este provider
NAO sintetiza nada: ele consome os MP3 gerados la.

Fluxo:
  1. `maquina exportar-narracao <slug>`  -> out/<slug>/narracao.json
  2. Abrir notebooks/narracao_chatterbox.ipynb no Colab (GPU T4)
  3. Enviar narracao.json + assets/voice/referencia.wav ao notebook
  4. Baixar o narracao.zip gerado e extrair em out/<slug>/audio/
  5. `maquina retomar <slug>` continua a producao do ponto certo

Se um arquivo de cena faltar, o erro diz exatamente o que fazer.
"""

from __future__ import annotations

from pathlib import Path

from .base import ErroProvider


class TTSLote:
    """Consome narracoes pre-geradas (Colab/Chatterbox) em vez de sintetizar."""

    custo_usd = 0.0

    def sintetizar(self, texto: str, saida: Path, *, voice_id: str = "") -> Path:
        if saida.exists() and saida.stat().st_size > 0:
            return saida
        raise ErroProvider(
            f"narracao em lote: falta {saida}.\n"
            "Gere as narracoes no Colab:\n"
            "  1. maquina exportar-narracao <slug>\n"
            "  2. abra notebooks/narracao_chatterbox.ipynb no Colab (GPU T4)\n"
            "  3. envie narracao.json + assets/voice/referencia.wav\n"
            "  4. extraia o narracao.zip em out/<slug>/audio/\n"
            "  5. maquina retomar <slug>"
        )
