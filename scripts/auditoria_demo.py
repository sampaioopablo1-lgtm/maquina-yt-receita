#!/usr/bin/env python3
"""Demonstracao do fluxo OAuth, para gravar o video da auditoria da YouTube API.

Existe porque a auditoria exige um video mostrando a tela de consentimento DO
NOSSO app e o que ele faz com o acesso — e a maquina publica hoje pela
Upload-Post, sem OAuth proprio. Nao havia o que gravar.

E um arquivo so, de proposito: quem vai gravar nao precisa instalar o projeto
inteiro, so o Python e duas bibliotecas. Toda a saida sai em INGLES porque o
terminal aparece no video e quem le e o revisor do Google.

Uso:
    python auditoria_demo.py <client_secret.json> [video.mp4]

Sem o segundo argumento ele so autentica e mostra o canal — util para ensaiar
antes de gravar. Com o video, faz o upload de verdade, que e o trecho final
que o revisor precisa ver.
"""
import json
import os
import sys

ESCOPOS = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/yt-analytics.readonly",
]


def linha(t=""):
    print(t, flush=True)


def autenticar(segredo):
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow

    token = os.path.join(os.path.dirname(os.path.abspath(segredo)), "token.json")
    cred = None
    if os.path.exists(token):
        cred = Credentials.from_authorized_user_file(token, ESCOPOS)
    if cred and cred.expired and cred.refresh_token:
        cred.refresh(Request())
    if not cred or not cred.valid:
        linha("No stored credentials. Starting OAuth consent flow...")
        linha("A browser window will open. Review the requested permissions.")
        linha()
        cred = InstalledAppFlow.from_client_secrets_file(
            segredo, ESCOPOS).run_local_server(port=0)
        # O token fica ao lado do segredo, nao no diretorio corrente: quem grava
        # o video roda de qualquer pasta, e um token perdido faz o ensaio
        # seguinte reabrir o consentimento sem aviso.
        with open(token, "w", encoding="utf-8") as f:
            f.write(cred.to_json())
        linha(f"Consent granted. Credentials stored in {token}")
    else:
        linha("Using stored credentials.")
    return cred


def mostrar_canal(api):
    r = api.channels().list(part="snippet,statistics", mine=True).execute()
    itens = r.get("items") or []
    if not itens:
        sys.exit("ERROR: these credentials do not control any YouTube channel.")
    c = itens[0]
    linha()
    linha("AUTHENTICATED CHANNEL (owned by the person granting consent)")
    linha(f"  title       {c['snippet']['title']}")
    linha(f"  channel id  {c['id']}")
    linha(f"  subscribers {c['statistics'].get('subscriberCount', 'hidden')}")
    linha(f"  videos      {c['statistics'].get('videoCount', '0')}")
    linha()


def enviar(api, caminho):
    from googleapiclient.http import MediaFileUpload

    corpo = {
        "snippet": {
            "title": "OAuth demonstration upload",
            "description": ("Test upload recorded for the YouTube API Services "
                            "audit submission. Uploaded by the channel owner to "
                            "the channel owner's own channel."),
            "categoryId": "27",
        },
        # Privado de proposito. Nao contraria a regra de publicar sempre em
        # publico: isto nao e publicacao, e a demonstracao — e enquanto o
        # projeto nao esta auditado o proprio YouTube forca privado de todo
        # jeito. O video mostra exatamente a limitacao que a auditoria remove.
        "status": {
            "privacyStatus": "private",
            "selfDeclaredMadeForKids": False,
            "containsSyntheticMedia": True,
        },
    }
    linha(f"Uploading {caminho} via youtube.videos.insert ...")
    req = api.videos().insert(part="snippet,status", body=corpo,
                              media_body=MediaFileUpload(caminho,
                                                         chunksize=-1,
                                                         resumable=True))
    resp = req.execute()
    vid = resp["id"]
    linha()
    linha("UPLOAD COMPLETE")
    linha(f"  video id  {vid}")
    linha(f"  url       https://www.youtube.com/watch?v={vid}")
    linha(f"  privacy   {resp['status']['privacyStatus']}")
    linha()
    linha("Open YouTube Studio to confirm the video is listed on the channel.")


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    segredo = sys.argv[1]
    if not os.path.exists(segredo):
        sys.exit(f"ERROR: client secret not found at {segredo}")
    # Confere que e mesmo um cliente de app instalado. Cliente "Web" tambem
    # baixa um JSON parecido e so falha depois, no meio do consentimento —
    # tarde demais para quem ja apertou o gravador.
    dados = json.load(open(segredo, encoding="utf-8"))
    if "installed" not in dados:
        sys.exit("ERROR: this client secret is not a Desktop app client.\n"
                 "In Google Cloud, create the OAuth client with application "
                 "type 'Desktop app' and download that JSON instead.")

    from googleapiclient.discovery import build

    linha("=" * 62)
    linha("Receita Video Pipeline - YouTube API access demonstration")
    linha("=" * 62)
    linha()
    cred = autenticar(segredo)
    api = build("youtube", "v3", credentials=cred)
    mostrar_canal(api)
    if len(sys.argv) > 2:
        enviar(api, sys.argv[2])
    else:
        linha("No video file given - authentication only.")
        linha("Run again with a video path to demonstrate videos.insert.")


if __name__ == "__main__":
    main()
