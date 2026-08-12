"""Clonagem da voz do Pablo em GPU gratuita do Kaggle.

Existe por um numero medido, nao por preferencia. O aprendizado #152 mediu o
Chatterbox Multilingual na CPU do runner do Actions: 319 s de CPU para 13,58 s
de audio, ou 23,5x o tempo real. Nesse fator um longo de 12:44 custa 5 h e a
frota de treze canais custaria 116.619 min/mes, contra os 2.000 do teto gratuito
de repositorio privado — 58x acima. A licenca (MIT) nunca foi o obstaculo; o
obstaculo e computacional.

Em GPU o mesmo modelo roda perto de 1x o tempo real. O Kaggle da 30 h/semana de
T4 de graca, e a frota inteira precisa de ~13,7 h/semana de audio. Cabe com
folga de duas vezes — e esta e a unica rota gratuita que fecha a conta.

DOIS MODOS:
  bench (padrao) — repete o experimento do voz-clone.yml, uma frase por idioma,
    e mede o fator em GPU. Serve para comparar com os 23,5x da CPU no MESMO
    material. Rode este primeiro: sem o numero, o resto e aposta.
  fila — le voz/fila.json do Storage e narra as cenas de verdade.

O que este script NAO faz: decidir por voce se o uso cabe nos termos do Kaggle.
Ver docs/21-kaggle-voz.md, secao "O risco que voce assume".
"""

import json
import os
import time
import urllib.request

# ---------------------------------------------------------------- configuracao

SB = "https://vevocauwtarctfwngrch.supabase.co"
BUCKET = "videos-maquina"
MODO = os.environ.get("MODO", "bench")
EXAG = float(os.environ.get("EXAG", "0.5"))
CFG = float(os.environ.get("CFG", "0.5"))

# A referencia ja vem densificada e normalizada (17,9 s, 87% de fala, -19,6 dBFS,
# zero clipping). Nao regenere: o corte foi escolhido a mao.
REF_URL = f"{SB}/storage/v1/object/public/{BUCKET}/voz/referencia-corte.wav"

# Mesmas frases do voz-clone.yml. Comparar hardware exige material identico —
# trocar as frases junto com a maquina mede duas coisas ao mesmo tempo e nao
# permite atribuir a diferenca a nenhuma delas.
FRASES = {
    "pt": "Existe mesmo um Ozempic natural? A Anvisa acabou de proibir tres produtos vendidos com essa promessa.",
    "en": "Your paycheck did not get smaller. The tax bracket moved, and almost nobody noticed it happening.",
    "es": "Con cien pesos de despensa se cocina toda la semana. Te muestro exactamente como se reparte.",
    "hi": "आपकी सैलरी कम नहीं हुई है। टैक्स का नियम बदला है, और किसी ने ध्यान नहीं दिया।",
    "pl": "Twoja rata wlasnie spadla, i to jest najniebezpieczniejszy moment calego kredytu.",
    "tr": "Asgari ucret zamlandi ama market fisi daha hizli buyudu. Farki birlikte hesaplayalim.",
    "el": "Ο μισθός σου δεν μειώθηκε. Άλλαξε η φορολογική κλίμακα, και σχεδόν κανείς δεν το πρόσεξε.",
    "id": "Gaji kamu tidak berkurang. Aturan pajaknya yang berubah, dan hampir tidak ada yang sadar.",
}

SAIDA = "/kaggle/working"


def anon():
    """Chave anon vem do cofre do Kaggle, nunca do codigo.

    O script fica num kernel privado, mas kernel privado pode ser tornado
    publico com dois cliques e o historico do commit continua la. Chave em
    Add-ons -> Secrets, nome SUPABASE_ANON.
    """
    from kaggle_secrets import UserSecretsClient

    return UserSecretsClient().get_secret("SUPABASE_ANON")


def baixar(url, destino):
    urllib.request.urlretrieve(url, destino)
    tam = os.path.getsize(destino)
    if tam == 0:
        raise RuntimeError(f"download vazio: {url}")
    print(f"  baixado {destino} ({tam/1024:.0f} kB)")
    return destino


def subir(caminho, alvo, mime, chave):
    """POST cria, PUT atualiza. O Storage separa os dois e nenhum sozinho serve
    para uma rotina que tanto publica arquivo novo quanto regrava — e o modo
    silencioso disso e pior: a copia envelhece sem ninguem notar."""
    url = f"{SB}/storage/v1/object/{BUCKET}/{alvo}"
    corpo = open(caminho, "rb").read()
    cabecalho = {
        "Authorization": f"Bearer {chave}",
        "apikey": chave,
        "Content-Type": mime,
    }
    for metodo in ("POST", "PUT"):
        req = urllib.request.Request(url, data=corpo, method=metodo, headers=cabecalho)
        try:
            with urllib.request.urlopen(req, timeout=300) as r:
                print(f"  {alvo}: {metodo} {r.status}")
                return True
        except Exception as e:
            codigo = getattr(e, "code", "?")
            if metodo == "POST":
                print(f"  {alvo}: POST {codigo} — objeto existe, tentando PUT")
                continue
            print(f"  {alvo}: PUT falhou ({codigo})")
            return False


# ------------------------------------------------------------------- execucao

import torch  # noqa: E402  (depois da config: o import custa segundos)
import torchaudio  # noqa: E402

print("torch", torch.__version__, "| cuda", torch.cuda.is_available())
if not torch.cuda.is_available():
    # Falhar alto aqui e barato. Rodar em CPU sem perceber custa 23,5x e a
    # sessao inteira, e o resultado parece bom porque o audio sai igual.
    raise SystemExit(
        "GPU nao disponivel. No editor: Settings -> Accelerator -> GPU T4 x2. "
        "Se a opcao estiver cinza, falta verificar o telefone da conta."
    )
print("gpu:", torch.cuda.get_device_name(0))

from chatterbox.mtl_tts import ChatterboxMultilingualTTS  # noqa: E402

os.makedirs(SAIDA, exist_ok=True)
ref = baixar(REF_URL, "/kaggle/working/ref.wav")

t0 = time.time()
modelo = ChatterboxMultilingualTTS.from_pretrained(device="cuda")
carga_s = time.time() - t0
print(f"modelo carregado em {carga_s:.0f}s")

chave = anon()
relatorio = {"modo": MODO, "gpu": torch.cuda.get_device_name(0),
             "carga_s": round(carga_s), "exag": EXAG, "cfg": CFG, "itens": []}

if MODO == "bench":
    trabalho = [(cod, texto, f"voz-{cod}") for cod, texto in FRASES.items()]
else:
    fila = json.load(urllib.request.urlopen(
        f"{SB}/storage/v1/object/public/{BUCKET}/voz/fila.json"))
    trabalho = [(c["idioma"], c["texto"], c["id"]) for c in fila["cenas"]]
    relatorio["pacote"] = fila.get("pacote")

for cod, texto, nome in trabalho:
    try:
        t0 = time.time()
        wav = modelo.generate(texto, language_id=cod, audio_prompt_path=ref,
                              exaggeration=EXAG, cfg_weight=CFG)
        gasto = time.time() - t0
        destino = f"{SAIDA}/{nome}.wav"
        torchaudio.save(destino, wav.cpu(), modelo.sr)
        dur = wav.shape[-1] / modelo.sr
        fator = gasto / dur if dur else 0
        print(f"  {cod}/{nome}: {dur:.1f}s de audio em {gasto:.0f}s = {fator:.2f}x tempo real")
        relatorio["itens"].append({"idioma": cod, "nome": nome,
                                   "duracao_s": round(dur, 2),
                                   "gpu_s": round(gasto, 1),
                                   "fator": round(fator, 2)})
        subir(destino, f"voz/{MODO}/{nome}.wav", "audio/wav", chave)
    except Exception as e:
        print(f"  {cod}/{nome}: FALHOU — {type(e).__name__}: {e}")
        relatorio["itens"].append({"idioma": cod, "nome": nome, "erro": str(e)[:200]})

fatores = [i["fator"] for i in relatorio["itens"] if "fator" in i]
if fatores:
    relatorio["fator_mediano"] = round(sorted(fatores)[len(fatores) // 2], 2)
    relatorio["fator_cpu_actions"] = 23.5  # aprendizado #152, mesmo material
    relatorio["ganho"] = round(23.5 / relatorio["fator_mediano"], 1)
    print(f"\nMEDIANA {relatorio['fator_mediano']}x tempo real "
          f"contra 23,5x da CPU do Actions = {relatorio['ganho']}x mais rapido")

with open(f"{SAIDA}/relatorio.json", "w") as f:
    json.dump(relatorio, f, ensure_ascii=False, indent=1)
subir(f"{SAIDA}/relatorio.json", f"voz/{MODO}/relatorio.json", "application/json", chave)
print(json.dumps(relatorio, ensure_ascii=False, indent=1))
