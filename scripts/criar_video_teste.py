"""Cria um Video de teste no SQLite local para validar o pipeline de publicacao.

Uso:
    python scripts/criar_video_teste.py [--slug SLUG] [--video-path CAMINHO]

O arquivo de video precisa ja existir antes de rodar `maquina publicar`.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Garante que o pacote eh encontrado mesmo sem pip install
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from maquina.config import Config
from maquina.models import Cena, Formato, Roteiro, Status, Video
from maquina.storage import Store


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--slug", default="teste-pipeline-shorts")
    parser.add_argument("--video-path", default="")
    args = parser.parse_args()

    cfg = Config.load()
    store = Store(cfg.data_dir / "maquina.db")

    slug = args.slug
    video_path = args.video_path or str(cfg.out_dir / slug / "final.mp4")

    if not Path(video_path).exists():
        print(f"ERRO: arquivo nao encontrado em {video_path}")
        sys.exit(1)

    roteiro = Roteiro(
        titulo="Setiap Level - Uji Coba Pipeline Otomatis",
        gancho="Pipeline publikasi berjalan dengan benar.",
        cenas=[
            Cena(
                indice=0,
                narracao="Ini adalah video uji coba pipeline publikasi otomatis Setiap Level.",
                prompt_visual="layar hitam dengan teks putih",
            )
        ],
        descricao=(
            "Video uji coba untuk memvalidasi pipeline publikasi otomatis. "
            "Video ini bersifat private dan akan dihapus setelah pengujian."
        ),
        tags=["uji coba", "pipeline", "otomatis", "setiap level"],
    )

    video = Video(
        slug=slug,
        formato=Formato.SHORTS,
        status=Status.AGUARDANDO_REVISAO,
        idioma="id",
        roteiro=roteiro,
        video_path=video_path,
        duracao_s=3.0,
        conteudo_sintetico=True,
    )

    store.salvar(video)
    print(f"OK: video '{slug}' registrado no SQLite")
    print(f"    video_path = {video_path}")
    print(f"    formato    = {video.formato.value}")
    print(f"    status     = {video.status.value}")


if __name__ == "__main__":
    main()
