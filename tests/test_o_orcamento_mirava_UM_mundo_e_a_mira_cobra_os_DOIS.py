# -*- coding: utf-8 -*-
"""O orcamento mirava UM mundo de provedor e a mira cobra os DOIS.

MEDIDO em 19/10 as 17:2x, escrevendo o `labtreinamento-s086`. O
`mira.orcamento` deu **25** caracteres por cena para nove cenas no MEIO da mira
medida daquele canal (23,0 de 20,0 a 26,0) — e com 25 a peca sai em edge 22,6 e
**piper 18,6, abaixo do piso de 20,0**. Isto e: a propria `mira.confere`
REPROVA a resposta que o `mira.orcamento` acabou de dar, porque ela cobra os
DOIS mundos desde 13/10 as 02:1x e o orcamento invertia so o `edge`.

O TAMANHO VAI MEDIDO e separado em duas coisas, porque elas nao sao a mesma:

  1. no canal cuja mira o `confere` DE FATO cobra nos dois mundos
     (`labtreinamento`), o orcamento do MEIO e reprovado em **98 de 99** specs.
     Esse e o defeito acionavel, e a janela que serve mora no TOPO da faixa:
     28 a 30 caracteres para nove cenas, nao o meio;
  2. nos outros dois canais da frota a mira e o `ALVO_SHORT` (41,5 a 43,0), e
     ali a pinca esta fechada por ARITMETICA: a razao piper/edge medida e 0,82 a
     0,89, logo o vao entre os mundos vale 4,6 a 7,5 s em 42 s — mais de TRES
     vezes a largura de 1,5 s da faixa. Nenhuma contagem de cenas poe os dois
     dentro, em nenhuma das tres vozes.

**O que isto NAO afirma:** que alguma peca foi publicada errada por isso. O
`confere` devolve `tem_mira: False` nesses dois canais e o portao `duracao`
cobra 18 a 45, que os dois mundos satisfazem. O que estava errado era o
CONSELHO do instrumento — e conselho que a conferencia reprova e pior que
conselho ausente, porque convida a escrever a peca errada.

**E a saida nao e nossa:** alargar o `ALVO_SHORT` ou mirar um mundo so e
parametro de producao (§10). O instrumento NOMEIA, como o `origens_sem_uso`
nomeia origem inutilizavel em vez de a esconder.
"""
import ast
import glob
import json
import os
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import ensaio  # noqa: E402
import mira  # noqa: E402

VOZES_DA_FROTA = ("el-GR-NestorasNeural", "pl-PL-MarekNeural",
                  "pt-BR-ThalitaMultilingualNeural")


def _specs_com_orcamento():
    """Toda spec do DISCO que recebe orcamento, com o orcamento dela."""
    out = []
    for p in sorted(glob.glob(os.path.join(RAIZ, "fabrica", "specs", "*.json"))):
        try:
            sp = json.load(open(p, encoding="utf-8"))
        except Exception:
            continue
        o = mira.orcamento(sp)
        if o and o.get("cabe"):
            out.append((os.path.basename(p), sp, o))
    return out


def test_a_varredura_sai_do_DISCO_e_nao_pode_ficar_vazia():
    """Vacuidade e o defeito do 743 em forma de glob."""
    todas = _specs_com_orcamento()
    assert len(todas) >= 50, (
        "menos de 50 specs com orcamento: a varredura deixou de medir o parque, "
        f"e todo teste deste arquivo passaria por vacuidade (achei {len(todas)})")


def test_o_canal_com_mira_COBRADA_nos_dois_mundos_reprova_o_orcamento_do_MEIO():
    """O defeito acionavel, e ele e de MAIORIA e nao de uma peca."""
    assert "labtreinamento" in ensaio.ALVO_POR_CANAL, (
        "nenhum canal tem ALVO_POR_CANAL: sem mira cobrada nos dois mundos "
        "este arquivo nao mede o defeito que o produziu")
    tot = rej = 0
    for _, sp, o in _specs_com_orcamento():
        if mira.canal_da_spec(sp) != "labtreinamento":
            continue
        tot += 1
        if not o.get("cabe_nos_dois"):
            rej += 1
    assert tot >= 20, f"specs demais de fora da conta: {tot}"
    assert rej > tot / 2, (
        "o orcamento do MEIO deixou de ser reprovado pela maioria das specs "
        f"deste canal ({rej} de {tot}) — releia a nota em vez de apagar: ou a "
        "mira mudou, ou o orcamento passou a mirar os dois mundos sozinho")


def test_quando_o_orcamento_e_reprovado_o_relato_DIZ_em_vez_de_calar():
    """Silenciar a conferencia e o sentido PERMISSIVO — custou seis pecas."""
    vistos = 0
    for nome, sp, o in _specs_com_orcamento():
        if o.get("cabe_nos_dois"):
            continue
        linhas = mira._linha_do_orcamento(sp)
        texto = "\n".join(linhas)
        assert "ATENCAO" in texto, (
            f"{nome}: o orcamento e reprovado pela mira e o relato nao diz nada")
        vistos += 1
        if vistos >= 25:
            break
    assert vistos > 0, "nenhuma spec reprovada: nada foi medido aqui"


def test_a_janela_dos_dois_mundos_e_cobrada_na_FRONTEIRA():
    """O que o instrumento devolve cabe; um caractere fora dela, nao."""
    voz = "pt-BR-ThalitaMultilingualNeural"
    faixa = ensaio.ALVO_POR_CANAL["labtreinamento"]
    jan = mira.janela_dos_dois_mundos(voz, 9, faixa)
    assert jan, ("a janela dos dois mundos FECHOU para nove cenas no "
                 "labtreinamento — era ela que tornava a peca `s086` "
                 "escrevivel; releia a nota em vez de mover o numero")
    lo, hi = jan

    def dentro(c):
        cen = [{"nar": "x" * c} for _ in range(9)]
        e = ensaio.duracao_real_prevista(cen, voz, "edge")
        p = ensaio.duracao_real_prevista(cen, voz, "piper")
        return faixa[0] <= e <= faixa[1] and faixa[0] <= p <= faixa[1]

    assert dentro(lo) and dentro(hi), "a janela devolvida nao cabe nos dois"
    assert not dentro(lo - 1), f"{lo - 1} tambem cabe: o piso esta frouxo"
    assert not dentro(hi + 1), f"{hi + 1} tambem cabe: o teto esta frouxo"


def test_CONTRAPROVA_a_janela_existe_num_caso_e_NAO_existe_noutro():
    """Funcao que devolve sempre None, ou sempre uma janela, nao mede nada."""
    aberta = mira.janela_dos_dois_mundos(
        "pt-BR-ThalitaMultilingualNeural", 9,
        ensaio.ALVO_POR_CANAL["labtreinamento"])
    fechada = mira.janela_dos_dois_mundos(
        "pt-BR-ThalitaMultilingualNeural", 10, ensaio.ALVO_SHORT)
    assert aberta is not None, "o caso ABERTO fechou"
    assert fechada is None, (
        "o `ALVO_SHORT` da frota passou a conter os dois mundos: isso derruba "
        "o item 2 da nota deste arquivo e ela tem de ser relida")


def test_a_faixa_da_FROTA_nao_contem_os_dois_mundos_em_contagem_NENHUMA():
    """Aritmetica, nao amostra: o vao entre os mundos e maior que a faixa."""
    for voz in VOZES_DA_FROTA:
        for n in range(1, 41):
            jan = mira.janela_dos_dois_mundos(voz, n, ensaio.ALVO_SHORT)
            assert jan is None, (
                f"{voz} com {n} cenas poe os dois mundos dentro de "
                f"{ensaio.ALVO_SHORT} ({jan}) — a pinca da frota ABRIU e a nota "
                "deste arquivo tem de ser relida, nao reaproveitada")


def test_a_razao_entre_os_mundos_e_MAIOR_que_a_largura_da_faixa_da_frota():
    """O motivo do teste anterior, medido em vez de deduzido."""
    largura = ensaio.ALVO_SHORT[1] - ensaio.ALVO_SHORT[0]
    meio = (ensaio.ALVO_SHORT[0] + ensaio.ALVO_SHORT[1]) / 2.0
    for voz in VOZES_DA_FROTA:
        cen = [{"nar": "x" * 50} for _ in range(10)]
        e = ensaio.duracao_real_prevista(cen, voz, "edge")
        p = ensaio.duracao_real_prevista(cen, voz, "piper")
        razao = p / e
        vao = (1.0 - razao) * meio
        assert vao > largura, (
            f"{voz}: o vao entre os mundos ({vao:.2f} s) deixou de ser maior "
            f"que a largura da faixa ({largura:.2f} s) — releia a nota")


def test_a_conta_e_DELEGADA_e_nao_nasce_um_segundo_dono_da_sobrecarga():
    """Refazer `P + 0,300` aqui e o defeito que congelou a legenda.

    Por AST, porque o docstring do modulo CITA a formula em prosa para se
    explicar, e casar prosa pegaria a explicacao em vez do codigo.
    """
    fonte = open(os.path.join(RAIZ, "fabrica", "mira.py"), encoding="utf-8").read()
    arv = ast.parse(fonte)
    alvo = None
    for n in ast.walk(arv):
        if isinstance(n, ast.FunctionDef) and n.name == "janela_dos_dois_mundos":
            alvo = n
    assert alvo is not None, "`janela_dos_dois_mundos` desapareceu do modulo"
    chamadas = [ast.unparse(c.func) for c in ast.walk(alvo)
                if isinstance(c, ast.Call)]
    assert any("duracao_real_prevista" in c for c in chamadas), (
        "a janela deixou de delegar ao `ensaio.duracao_real_prevista`: ela "
        f"chama {chamadas}")
    corpo = ast.unparse(alvo)
    for proibido in ("0.300", "0.3 +", "+ 0.3"):
        assert proibido not in corpo, (
            f"{proibido!r} dentro da funcao: segundo dono da sobrecarga por voz")


def test_os_DOIS_mundos_sao_exercitados_e_nao_so_o_edge():
    """O defeito era mirar UM mundo; o conserto tem de tocar os dois."""
    fonte = open(os.path.join(RAIZ, "fabrica", "mira.py"), encoding="utf-8").read()
    arv = ast.parse(fonte)
    alvo = [n for n in ast.walk(arv) if isinstance(n, ast.FunctionDef)
            and n.name == "janela_dos_dois_mundos"][0]
    corpo = ast.unparse(alvo)
    assert '"edge"' in corpo or "'edge'" in corpo, "o mundo edge saiu"
    assert '"piper"' in corpo or "'piper'" in corpo, (
        "o mundo piper saiu da janela: ela voltou a medir UM mundo, que e o "
        "defeito inteiro")


def test_o_MOTIVO_continua_escrito_no_modulo():
    """Conserto sem motivo escrito volta calado."""
    fonte = open(os.path.join(RAIZ, "fabrica", "mira.py"), encoding="utf-8").read()
    for marca in ("labtreinamento-s086", "730/733", "740/748"):
        assert marca in fonte, (
            f"{marca!r} saiu do `mira.py`: sem a procedencia, a rodada seguinte "
            "nao sabe por que a janela existe e volta a mirar um mundo so")


def test_o_CODIGO_DE_SAIDA_sai_do_VEREDITO_e_nao_de_um_grep_na_prosa():
    """Ele era `if "FORA" in t` — um grep no texto do proprio modulo.

    MEDIDO na mesma rodada, e por uma REGRESSAO que a suite pegou: quando o
    orcamento passou a dizer *"o OUTRO mundo sai FORA de 20,0 a 26,0"*, o
    `mira.py` comecou a devolver **1** para peca que esta DENTRO da mira. A
    decisao tinha DOIS donos — `confere()["fora"]` e a palavra na frase — e o
    segundo nao e dono de nada. Mesma assinatura do 753 e do grep de 17/10.
    """
    import subprocess
    alvo = os.path.join(RAIZ, "fabrica", "specs", "labtreinamento-s086.json")
    assert os.path.exists(alvo), (
        "a spec `labtreinamento-s086` saiu do disco — e ela e a peca em que a "
        "regressao apareceu; sem ela este teste nao mede nada")
    sp = json.load(open(alvo, encoding="utf-8"))
    r = mira.confere(sp)
    assert r["tem_mira"] and not r["fora"], (
        "o veredito desta peca deixou de ser DENTRO: releia em vez de mover")
    linhas = "\n".join(mira._linha_do_orcamento(sp))
    assert "FORA" in linhas, (
        "a frase do orcamento deixou de carregar a palavra FORA — e era ela "
        "que fazia o grep acusar; sem ela este teste passa por vacuidade")
    proc = subprocess.run([sys.executable, os.path.join(RAIZ, "fabrica", "mira.py"),
                           alvo], capture_output=True, text=True)
    assert proc.returncode == 0, (
        "o `mira.py` devolveu nao-zero para peca DENTRO da mira: o codigo de "
        "saida voltou a sair da prosa em vez do veredito")


def test_CONTRAPROVA_o_codigo_de_saida_continua_acusando_quem_esta_FORA():
    """Sem isto, bastaria devolver sempre zero para o teste acima passar."""
    import subprocess
    foras = []
    for p in sorted(glob.glob(os.path.join(RAIZ, "fabrica", "specs",
                                           "labtreinamento*.json"))):
        sp = json.load(open(p, encoding="utf-8"))
        if mira.canal_da_spec(sp) != "labtreinamento":
            continue
        r = mira.confere(sp)
        if r.get("tem_mira") and r.get("fora"):
            foras.append(p)
    assert foras, ("nenhuma spec deste canal esta FORA da mira: a contraprova "
                   "nao tem caso e este arquivo passa por vacuidade")
    proc = subprocess.run([sys.executable, os.path.join(RAIZ, "fabrica", "mira.py"),
                           foras[0]], capture_output=True, text=True)
    assert proc.returncode != 0, (
        f"{os.path.basename(foras[0])} esta FORA pelo veredito e o `mira.py` "
        "devolveu zero: ele parou de acusar")
