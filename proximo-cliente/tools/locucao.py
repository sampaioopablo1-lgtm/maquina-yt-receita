"""Gera a locucao dos criativos da O Proximo Cliente pelo ElevenLabs.

Roda no GitHub Actions (locucao-elevenlabs.yml), porque a sessao de nuvem onde
os criativos sao montados nao alcanca api.elevenlabs.io. A interface e o
repositorio: um roteiro .json entra em `proximo-cliente/locucao/roteiros/`, o
workflow gera o audio e commita em `proximo-cliente/locucao/audio/`.

Cada roteiro tem:

    {
      "id": "01-lead-esfria-v2",
      "texto": "...",
      "modelo": "eleven_multilingual_v2",          # opcional
      "vozes": ["<voice_id>", ...],                # vazio = voz clonada da conta
      "ajustes": {"stability": 0.45, ...}          # opcional
    }

Para cada voz sai um `.mp3` e um `.tempos.json` com o inicio e o fim de cada
palavra, que o criativo usa para sincronizar as animacoes com a fala.

Tambem escreve `proximo-cliente/locucao/VOZES.md`: as vozes da conta e as vozes
em portugues da biblioteca publica, com link de previa, para escolher de ouvido.

Sem ELEVENLABS_API_KEY o script avisa e encerra com sucesso: um workflow que so
falha treina quem olha o Actions a ignorar vermelho.
"""

from __future__ import annotations

import base64
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://api.elevenlabs.io"
RAIZ = Path(__file__).resolve().parents[1] / "locucao"
ROTEIROS = RAIZ / "roteiros"
AUDIO = RAIZ / "audio"
CATALOGO = RAIZ / "VOZES.md"

MODELO_PADRAO = "eleven_multilingual_v2"
# Conversacional e natural: estabilidade media deixa a entonacao variar sem
# virar teatro; style baixo evita o tom de locutor de radio.
AJUSTES_PADRAO = {"stability": 0.45, "similarity_boost": 0.8, "style": 0.15, "use_speaker_boost": True}
VOZES_AUTOMATICAS = 3


def chamar(metodo: str, caminho: str, chave: str, corpo: dict | None = None) -> dict:
    dados = json.dumps(corpo).encode() if corpo is not None else None
    req = urllib.request.Request(API + caminho, data=dados, method=metodo)
    req.add_header("xi-api-key", chave)
    req.add_header("accept", "application/json")
    if dados is not None:
        req.add_header("content-type", "application/json")
    for tentativa in range(3):
        try:
            with urllib.request.urlopen(req, timeout=120) as resp:
                return json.loads(resp.read() or b"{}")
        except urllib.error.HTTPError as erro:
            detalhe = erro.read().decode(errors="replace")[:400]
            if erro.code in (429, 500, 502, 503) and tentativa < 2:
                time.sleep(5 * (tentativa + 1))
                continue
            raise SystemExit(f"ElevenLabs {metodo} {caminho} -> HTTP {erro.code}: {detalhe}")
    raise SystemExit(f"ElevenLabs {metodo} {caminho}: sem resposta")


def slug(texto: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", texto.lower()).strip("-") or "voz"


def vozes_da_conta(chave: str) -> list[dict]:
    return chamar("GET", "/v1/voices", chave).get("voices", [])


def vozes_em_portugues(chave: str) -> list[dict]:
    qs = urllib.parse.urlencode({"language": "pt", "page_size": 100, "sort": "usage_character_count_1y"})
    vozes = chamar("GET", f"/v1/shared-voices?{qs}", chave).get("voices", [])
    # Sotaque brasileiro primeiro; portugues europeu soa estranho num anuncio
    # para dono de empresa no Brasil.
    return sorted(vozes, key=lambda v: "brazil" not in (v.get("accent") or "").lower())


def escrever_catalogo(conta: list[dict], publicas: list[dict]) -> None:
    linhas = [
        "# Vozes disponiveis",
        "",
        "Gerado por `proximo-cliente/tools/locucao.py`. Para usar uma voz, copie o `voice_id` para a lista `vozes` do roteiro.",
        "",
        "## Na conta",
        "",
        "| Nome | Categoria | voice_id | Previa |",
        "| --- | --- | --- | --- |",
    ]
    for v in conta:
        linhas.append(f"| {v.get('name')} | {v.get('category')} | `{v.get('voice_id')}` | [ouvir]({v.get('preview_url')}) |")
    linhas += [
        "",
        "## Biblioteca publica em portugues (mais usadas primeiro, sotaque brasileiro no topo)",
        "",
        "| Nome | Genero | Idade | Sotaque | Descricao | voice_id | Previa |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for v in publicas[:60]:
        desc = (v.get("description") or "").replace("|", "/").replace("\n", " ")[:90]
        linhas.append(
            f"| {v.get('name')} | {v.get('gender')} | {v.get('age')} | {v.get('accent')} | {desc} "
            f"| `{v.get('voice_id')}` | [ouvir]({v.get('preview_url')}) |"
        )
    CATALOGO.write_text("\n".join(linhas) + "\n", encoding="utf-8")


def vozes_proprias(conta: list[dict]) -> list[dict]:
    """A voz do fundador, clonada na conta, vem antes de qualquer voz de biblioteca.

    `premade` sao as vozes padrao do ElevenLabs e `professional` inclui as
    adicionadas da biblioteca publica; so `cloned` e a voz gravada pelo dono.
    """
    return [v for v in conta if v.get("category") == "cloned"]


def escolher_automatico(publicas: list[dict]) -> list[dict]:
    """Duas vozes brasileiras masculinas e uma feminina, as mais usadas."""
    brasileiras = [v for v in publicas if "brazil" in (v.get("accent") or "").lower()] or publicas
    masc = [v for v in brasileiras if v.get("gender") == "male"][:2]
    fem = [v for v in brasileiras if v.get("gender") == "female"][:1]
    return (masc + fem)[:VOZES_AUTOMATICAS]


def garantir_na_conta(chave: str, voz_publica: dict, conta_ids: set[str]) -> str:
    voice_id = voz_publica["voice_id"]
    if voice_id in conta_ids:
        return voice_id
    dono = voz_publica.get("public_owner_id")
    nome = f"OPC {voz_publica.get('name')}"[:60]
    resp = chamar("POST", f"/v1/voices/add/{dono}/{voice_id}", chave, {"new_name": nome})
    novo = resp.get("voice_id", voice_id)
    conta_ids.add(novo)
    print(f"  voz adicionada a conta: {nome} ({novo})")
    return novo


def tempos_por_palavra(alinhamento: dict) -> list[dict]:
    chars = alinhamento.get("characters", [])
    ini = alinhamento.get("character_start_times_seconds", [])
    fim = alinhamento.get("character_end_times_seconds", [])
    palavras, atual, t0, t1 = [], "", None, None
    for c, a, b in zip(chars, ini, fim):
        if c.isspace():
            if atual:
                palavras.append({"palavra": atual, "inicio": round(t0, 3), "fim": round(t1, 3)})
            atual, t0 = "", None
            continue
        if t0 is None:
            t0 = a
        atual += c
        t1 = b
    if atual:
        palavras.append({"palavra": atual, "inicio": round(t0, 3), "fim": round(t1, 3)})
    return palavras


def gerar(chave: str, roteiro: dict, voice_id: str, nome_voz: str) -> None:
    modelo = roteiro.get("modelo", MODELO_PADRAO)
    ajustes = {**AJUSTES_PADRAO, **roteiro.get("ajustes", {})}
    assinatura = hashlib.sha256(
        json.dumps([roteiro["texto"], modelo, ajustes, voice_id], sort_keys=True).encode()
    ).hexdigest()[:16]
    base = AUDIO / f"{roteiro['id']}--{slug(nome_voz)}"
    marca = base.with_suffix(".sha")
    if marca.exists() and marca.read_text().strip() == assinatura and base.with_suffix(".mp3").exists():
        print(f"  {base.name}: sem mudanca, pulado")
        return
    corpo = {"text": roteiro["texto"], "model_id": modelo, "voice_settings": ajustes}
    resp = chamar("POST", f"/v1/text-to-speech/{voice_id}/with-timestamps?output_format=mp3_44100_128", chave, corpo)
    base.with_suffix(".mp3").write_bytes(base64.b64decode(resp["audio_base64"]))
    palavras = tempos_por_palavra(resp.get("alignment") or {})
    duracao = palavras[-1]["fim"] if palavras else None
    base.with_suffix(".tempos.json").write_text(
        json.dumps({"voz": nome_voz, "voice_id": voice_id, "modelo": modelo, "duracao": duracao, "palavras": palavras},
                   ensure_ascii=False, indent=1),
        encoding="utf-8",
    )
    marca.write_text(assinatura + "\n")
    print(f"  {base.name}.mp3 gerado ({duracao}s, {len(roteiro['texto'])} caracteres)")


def main() -> int:
    chave = os.environ.get("ELEVENLABS_API_KEY", "").strip()
    if not chave:
        print("::warning::ELEVENLABS_API_KEY nao cadastrada em Settings > Secrets > Actions. Nada foi gerado.")
        return 0
    AUDIO.mkdir(parents=True, exist_ok=True)

    conta = vozes_da_conta(chave)
    publicas = vozes_em_portugues(chave)
    escrever_catalogo(conta, publicas)
    print(f"catalogo: {len(conta)} vozes na conta, {len(publicas)} publicas em portugues")

    conta_ids = {v["voice_id"] for v in conta}
    nomes = {v["voice_id"]: v.get("name", v["voice_id"]) for v in conta + publicas}
    por_id = {v["voice_id"]: v for v in publicas}

    for arquivo in sorted(ROTEIROS.glob("*.json")):
        roteiro = json.loads(arquivo.read_text(encoding="utf-8"))
        print(f"roteiro {roteiro['id']}")
        escolhidas = (
            roteiro.get("vozes")
            or [v["voice_id"] for v in vozes_proprias(conta)]
            or [v["voice_id"] for v in escolher_automatico(publicas)]
        )
        for voice_id in escolhidas:
            if voice_id in por_id:
                voice_id_conta = garantir_na_conta(chave, por_id[voice_id], conta_ids)
            else:
                voice_id_conta = voice_id
            gerar(chave, roteiro, voice_id_conta, nomes.get(voice_id, voice_id))
    return 0


if __name__ == "__main__":
    sys.exit(main())
