"""Capitulos cronometrados e copy.md — texto puro, sem stack de render.

Estas tres funcoes viviam em fabrica.py, que abre com `import cairosvg,
edge_tts`. Elas nao usam nenhum dos dois: contam segundos e formatam markdown.
Mas quem precisasse delas herdava a stack inteira de render.

O custo apareceu duas vezes no mesmo dia (13/08/2026):

* o job de reparo de descricao morreu com ModuleNotFoundError em cairosvg —
  para uma operacao que so mexe em texto;
* o teste teve que injetar modulos falsos em sys.modules para conseguir
  importar. Contornar em teste o que trava em producao e o sinal de que o
  acoplamento e o defeito, nao o ambiente.

`trilha_do_canal` vem junto porque o credito CC-BY faz parte do copy, e ela so
lista arquivo — quem decodifica audio para validar a faixa e a fabrica.
"""

from __future__ import annotations

import glob
import os

TRILHA_DIR = "/tmp/trilhas"

# As UNICAS faixas do portfolio. E a mesma lista que o frota.yml baixa.
#
# Sem isto, `trilha_do_canal` fazia glob de *.mp3 e sorteava por hash sobre
# QUALQUER arquivo presente. Medido em 14/08/2026 no container da sessao: um
# `bench.mp3` de benchmark esquecido em /tmp/trilhas entrava no sorteio e era
# escolhido como trilha do nivel-do-jogo e do kolejny-poziom — um arquivo que
# nunca foi trilha de nada, com o credito CC-BY do copy nomeando outra coisa.
#
# O modo de falha certo e "faixa faltando", que e barulhento, e nunca "faixa
# trocada", que sai no ar sem ninguem perceber.
#
# O Cipher2 saiu da lista em 14/08/2026. Baixado do bucket direto: HTTP 404,
# NoSuchKey, 88 bytes de JSON de erro. E nenhum dos treze canais esta
# registrado nele em canais.trilha — era fantasma puro, e um fantasma na lista
# fazia o hash dividir por quatro quando so tres chegam.
TRILHAS_VALIDAS = ("Deliberate_Thought", "Inspired", "Wholesome")

# O YouTube exige capitulo >= 10s e descarta a LISTA INTEIRA se um so violar.
# Cena tem ~11s e algumas ficam abaixo, entao agrupa.
MIN_CAP, MAX_CAP = 60, 150


def trilha_do_canal(slug, valida=None, registrada=None):
    """Faixa fixa por canal = assinatura sonora. CC-BY, credito no copy.md.

    `registrada` e o nome gravado em canais.trilha e VENCE o hash. O hash foi
    como as faixas se distribuiram na primeira vez; o banco e o registro do que
    cada canal REALMENTE usa desde entao.

    Isso importa porque o hash divide pelos arquivos PRESENTES, e o conjunto
    varia. Medido em 13/08/2026: Cipher2.mp3 nao existe no bucket (404
    NoSuchKey), entao quem baixa as quatro fica com tres — e o nivel-do-jogo,
    registrado em Inspired, passaria a receber Wholesome. Faixa trocada sem
    erro nenhum, com o credito CC-BY do copy apontando para a outra.

    O frota.yml tolera isso hoje: baixa as quatro com `|| true` e so aborta se
    ZERO chegarem.

    `valida` e opcional para quem puder decodificar (a fabrica passa a checagem
    que pega mp3 com HTML dentro). Sem ela, lista pelo nome — que e o suficiente
    para descobrir QUAL faixa creditar.
    """
    fs = sorted(f for f in glob.glob(f"{TRILHA_DIR}/*.mp3")
                if os.path.basename(f)[:-4] in TRILHAS_VALIDAS)
    if valida:
        fs = [f for f in fs if valida(f)]
    if not fs:
        return None
    if registrada:
        alvo = os.path.join(TRILHA_DIR, f"{registrada}.mp3")
        if alvo in fs:
            return alvo
        # Registrada e ausente e defeito de entrega, nao motivo para escolher
        # outra calada: quem chamou decide o que fazer com o None.
        raise FileNotFoundError(
            f"trilha registrada '{registrada}' do canal {slug} nao esta em "
            f"{TRILHA_DIR} (tem: {[os.path.basename(f)[:-4] for f in fs]}). "
            f"Renderizar com outra faixa troca a assinatura sonora do canal e "
            f"deixa o credito CC-BY do copy apontando para a errada."
        )
    return fs[sum(map(ord, slug)) % len(fs)]


def capitulos(sp, tempos):
    """Capitulos cronometrados a partir dos clipes RENDERIZADOS.

    Os tempos saem do clipe renderizado, nunca do mp3: o mp3 nao inclui a
    respiracao entre cenas, e o erro acumula ao longo de 50 cenas jogando os
    capitulos do fim para depois do trecho que nomeiam.

    Prefere abrir no `titulo` ou no `broll` — as cenas que abrem secao nos
    dois formatos — para o capitulo levar nome de secao e nao um slide
    qualquer do meio.
    """
    caps, t, ultimo = [], 0.0, -1e9
    for i, c in enumerate(sp["longo"]):
        dt = t - ultimo
        # `sem_cap` marca cenas de passagem (ponte de fim de capitulo): sao
        # layout `titulo` mas o texto delas nao nomeia secao nenhuma, e virava
        # capitulo chamado "Bridge — ...", que nao ajuda ninguem a navegar.
        pode = not c.get("sem_cap")
        # `broll` entra ao lado de `titulo` porque no formato com footage a
        # cena que ABRE capitulo e uma cena broll — o epomeno-epipedo-004
        # desenhou 7 capitulos e publicou 4, porque as 7 aberturas eram broll
        # e so `titulo` contava como abertura de secao (aprendizado 311).
        # A regra continua sendo "abertura de secao", nao "tem cap": `cap`
        # aparece em 785 cenas de todos os layouts e viraria capitulo a cada
        # minuto.
        if i == 0 or (pode and dt >= MIN_CAP and
                      c.get("layout") in ("titulo", "broll")) \
                or (pode and dt >= MAX_CAP):
            caps.append(f"{int(t//60)}:{int(t%60):02d} {c.get('cap', c.get('kicker','...'))}")
            ultimo = t
        t += tempos[i]
    return caps


def credito_trilha(slug, valida=None, registrada=None):
    """Credito CC-BY obrigatorio: sem ele o uso da faixa deixa de ser licenciado.

    `registrada` PRECISA chegar ate aqui. O parametro existia em
    `trilha_do_canal` desde 13/08/2026 e nao era repassado por ninguem, entao o
    credito continuava saindo do hash — medido em 14/08/2026 no ensaio do
    resep-naik-level-003: canais.trilha diz Deliberate_Thought e o copy.md
    renderizado creditava Cipher2.

    Credito errado nao e detalhe de estilo: e o que torna o uso da faixa
    licenciado. Nomear a faixa errada e o mesmo que nao creditar.
    """
    faixa = trilha_do_canal(slug, valida, registrada)
    if not faixa:
        return "—"
    nome = os.path.basename(faixa)[:-4].replace("_", " ")
    return (f"Music: {nome} by Kevin MacLeod (incompetech.com) — Licensed under "
            "Creative Commons: By Attribution 4.0\n"
            "http://creativecommons.org/licenses/by/4.0/")


def escrever_copy(sp, tempos, d, valida_trilha=None):
    """Preenche {CAPITULOS} e {TRILHA} e grava copy.md no workdir.

    Vivia dentro do `render()` da fabrica, que o `etapas.py` nao chama — e por
    isso todo pacote feito pela esteira sequencial ficava SEM copy.md. Medido em
    13/08/2026: o seviye-seviye-002 subiu para o YouTube com "{CAPITULOS}"
    literal na descricao, porque o publicar.py caiu no texto da spec.
    """
    copy = (sp.get("copy") or "") \
        .replace("{CAPITULOS}", "\n".join(capitulos(sp, tempos))) \
        .replace("{TRILHA}", credito_trilha(sp["slug"], valida_trilha,
                                            sp.get("trilha")))
    with open(f"{d}/copy.md", "w", encoding="utf-8") as f:
        f.write(copy)
    return copy
