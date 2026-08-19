# -*- coding: utf-8 -*-
"""A trava por nome de pacote precisa rodar ANTES do render.

Em 19/08/2026 o kolejny-poziom-007 renderizou 89 cenas e so entao descobriu
que o nome ja pertencia a um video publicado em 11/08. A trava existia e
funcionou — no lugar errado da fila.
"""
import json
import os
import subprocess
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLICAR = os.path.join(RAIZ, "fabrica", "publicar.py")


def _spec(tmp_path, pacote="canal-teste-001"):
    p = tmp_path / "spec.json"
    p.write_text(json.dumps({
        "slug": "canal-teste", "pacote": pacote, "idioma": "pl",
        "voz": "pl-PL-MarekNeural", "longo": [], "short": [], "copy": "",
    }), encoding="utf-8")
    return str(p)


def _roda(spec, respostas, extra=()):
    """Roda o publicar.py com a rede fingida por um sitecustomize."""
    dir_falso = os.path.dirname(spec)
    with open(os.path.join(dir_falso, "sitecustomize.py"), "w") as f:
        f.write(
            "import io, json, sys\n"
            "sys.path.insert(0, %r)\n" % os.path.join(RAIZ, "fabrica") +
            "RESP = %r\n" % json.dumps(respostas) +
            "import urllib.request\n"
            "def _fake(req, *a, **k):\n"
            "    return io.BytesIO(RESP.encode())\n"
            "urllib.request.urlopen = _fake\n"
        )
    env = dict(os.environ)
    env["PYTHONPATH"] = dir_falso
    env["SUPABASE_URL"] = "https://exemplo.supabase.co"
    env["SUPABASE_SERVICE_ROLE_KEY"] = "chave-de-teste"
    return subprocess.run(
        [sys.executable, PUBLICAR, spec, "--canal", "canal-teste",
         "--so-conferir-nome", *extra],
        capture_output=True, text=True, env=env, cwd=RAIZ,
    )


def test_nome_livre_passa(tmp_path):
    r = _roda(_spec(tmp_path), [])
    assert r.returncode == 0, r.stderr
    assert "livre" in r.stdout


def test_nome_ja_usado_reprova(tmp_path):
    r = _roda(_spec(tmp_path), [{"formato": "longo", "youtube_id": "MjI4ZGJAhIo"}])
    assert r.returncode != 0
    assert "JA ESTA no ar" in r.stderr


def test_a_mensagem_diz_para_nao_contar_videos(tmp_path):
    """A causa raiz foi contar longos distintos em vez de olhar os nomes."""
    r = _roda(_spec(tmp_path), [{"formato": "longo", "youtube_id": "MjI4ZGJAhIo"}])
    assert "nao e sequencial" in r.stderr
    assert "ANTES de renderizar" in r.stderr


def test_repetir_libera_a_trava_antecipada(tmp_path):
    """--repetir e republicacao deliberada; a trava antecipada respeita isso."""
    r = _roda(_spec(tmp_path), [{"formato": "longo", "youtube_id": "MjI4ZGJAhIo"}],
              extra=("--repetir",))
    assert r.returncode == 0, r.stderr


def test_sai_antes_de_precisar_do_copy(tmp_path):
    """O ponto todo e rodar sem artefato de render no disco."""
    r = _roda(_spec(tmp_path), [])
    assert r.returncode == 0
    assert "copy" not in r.stderr.lower()


def test_o_passo_roda_antes_do_render_no_workflow():
    """Portao depois do render nao economiza render nenhum."""
    import yaml
    with open(os.path.join(RAIZ, ".github", "workflows", "frota.yml")) as f:
        d = yaml.safe_load(f)
    nomes = [s.get("name") for s in d["jobs"]["produzir"]["steps"]]
    assert "Conferir nome do pacote" in nomes
    assert nomes.index("Conferir nome do pacote") < nomes.index("Renderizar")
