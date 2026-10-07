"""O motion e OPT-IN, e este arquivo e o que garante o "opt".

POR QUE ELE EXISTE. Em 07/10/2026 Pablo pediu video com "animacoes, barulhos,
efeitos sonoros". O `fabrica/motion.py` foi escrito naquele dia e ficou SEM
NINGUEM O IMPORTAR — codigo morto, que nao muda nada e nao se mede. Agora ele
esta ligado ao renderizador, e isso cria um risco novo: o experimento 32 (foco
de tres canais, teto 7) precisa de sete a dez dias com o pipeline INTACTO, e foi
exatamente uma troca de renderizador no meio que matou o experimento 31.

Entao a garantia que estes testes dao nao e "o motion e bonito" — isso o olho
julga no YouTube. E: COM `motion` AUSENTE OU FALSO, A STRING DE FILTRO SAI
IDENTICA A DE ANTES, caractere por caractere. Enquanto este arquivo passar, a
spec sem a chave renderiza exatamente como renderizava.

Como em test_tremor.py, aqui se olha a FORMA do filtro, nao pixel de video:
roda em milissegundos e vale para spec que ainda nao existe.
"""

import os
import sys
import types

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.modules.setdefault("edge_tts", types.ModuleType("edge_tts"))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import fabrica as F  # noqa: E402
import motion as M  # noqa: E402


# ----------------------------------------------------------------- a trava
def test_motion_desligado_nao_muda_nada():
    """O contrato do experimento 32, em forma de assert.

    Se este teste cair, o caminho padrao mudou e a comparacao do experimento
    perdeu o controle — e isso vale para QUALQUER numero de camadas, porque a
    cena de 0 camadas passa por um `return` proprio no filtro.
    """
    for n in (0, 1, 2, 3, 4, 7):
        padrao = F.filtro_camadas(n, 10.0, 0, 300, 1280, 720)
        explicito = F.filtro_camadas(n, 10.0, 0, 300, 1280, 720, motion=False)
        assert padrao == explicito, f"n={n}: o default deixou de ser desligado"
        assert "fade=t=in:st=0" not in padrao, f"n={n}: borda vazou com motion off"
        assert "pow(" not in padrao, f"n={n}: easing vazou com motion off"
        if n:
            assert f"d={F.ENTRADA}:alpha=1" in padrao, (
                f"n={n}: a entrada deixou de ser os 0,40 s de sempre")


def test_motion_ligado_so_com_a_chave():
    assert M.motion_ligado({}) is False
    assert M.motion_ligado({"motion": False}) is False
    assert M.motion_ligado({"motion": True}) is True


# -------------------------------------------------------- o que ele muda
def test_easing_entra_e_e_recortado():
    """Com motion, o deslize deixa de ser linear — e nao se move fora da janela."""
    f = F.filtro_camadas(2, 10.0, 0, 300, 1280, 720, motion=True, layout="titulo")
    assert "pow(1-" in f, "o ease-out cubico nao chegou ao filtro"
    assert "max(0" in f and "min(1" in f, "o progresso saiu sem recorte"
    assert "*max(0\\,1-(t-" not in f, "o deslize linear antigo continua ali"


def test_entrada_escalona_por_papel():
    """Titulo entra mais lento que item de lista. Numeros do motion, nao daqui."""
    tit = F.filtro_camadas(3, 10.0, 0, 300, 1280, 720, motion=True, layout="titulo")
    lis = F.filtro_camadas(3, 10.0, 0, 300, 1280, 720, motion=True, layout="lista")
    assert f"d={M.ENTRADA_POR_PAPEL['titulo']}:alpha=1" in tit
    assert f"d={M.ENTRADA_POR_PAPEL['item']}:alpha=1" in lis
    assert M.ENTRADA_POR_PAPEL["item"] < M.ENTRADA_POR_PAPEL["titulo"]


def test_borda_entra_e_desaparece_em_cena_curta():
    """O fade da emenda nao cabe em cena curtissima, e ali ele nao deve existir."""
    longa = F.filtro_camadas(1, 10.0, 0, 300, 1280, 720, motion=True)
    assert f"fade=t=in:st=0:d={M.FADE_BORDA}" in longa
    assert "fade=t=out:st=9.880" in longa, "a saida nao fechou na borda certa"
    curta = F.filtro_camadas(1, 0.3, 0, 9, 1280, 720, motion=True)
    assert "fade=t=in" not in curta, "fade em cena de 0,3 s engoliria a cena"


# --------------------------------------------------------------- os sons
def test_som_abre_com_whoosh_e_segue_em_tick():
    plano = M.plano_de_sons("item", [0.45, 1.2, 2.0], tem_cap=False)
    assert [n for n, _ in plano] == ["whoosh", "tick", "tick"]
    assert [round(t, 2) for _, t in plano] == [0.45, 1.2, 2.0]


def test_cena_de_capitulo_leva_marco_no_zero():
    plano = M.plano_de_sons("item", [0.45], tem_cap=True)
    assert plano[0] == ("marco", 0.0)
    assert ("whoosh", 0.45) in plano


def test_broll_so_leva_marco():
    assert M.plano_de_sons("broll", [], tem_cap=False) == []
    assert M.plano_de_sons("broll", [], tem_cap=True) == [("marco", 0.0)]


def test_mix_poe_a_voz_antes_dos_sons_e_apara_a_duracao():
    """A voz e a ultima entrada ANTES dos sons; o mix nao estica a cena.

    O `apad`+`atrim` nao e enfeite: sem ele uma cena cujo ultimo efeito cai
    perto do fim ganha alguns centesimos, e o concat de 56 cenas acumula o
    desvio ate os capitulos sairem do lugar.
    """
    plano = [("marco", 0.0), ("whoosh", 0.45), ("tick", 1.2)]
    f = M.filtro_mixar_sons(plano, 5, 9.5)
    assert f.startswith("[5:a]adelay=0|0"), "o primeiro som nao entrou em 5"
    assert "[6:a]adelay=450|450" in f
    assert "[7:a]adelay=1200|1200" in f
    assert "[4:a]" in f, "a voz nao e a entrada imediatamente anterior"
    assert "amix=inputs=4:" in f, "a voz nao foi contada no mix"
    assert "normalize=0" in f, "sem normalize=0 o amix abaixa a voz"
    assert "atrim=0:9.500[a]" in f
    assert M.filtro_mixar_sons([], 5, 9.5) == ""


def test_ganho_dos_sons_fica_abaixo_da_trilha():
    """Efeito mais alto que a trilha vira irritante na segunda das 56 cenas."""
    trilha_db = float(F.VOL_TRILHA.replace("dB", ""))
    for nome, db in M.GANHO_SOM.items():
        assert db < trilha_db, f"{nome} a {db} dB nao esta abaixo de {trilha_db}"


def test_comando_de_sintese_nao_baixa_nada():
    cmd = M.comando_sintetizar("whoosh", "/tmp/x.wav", "ffmpeg")
    assert "-f" in cmd and "lavfi" in cmd, "o som deixou de ser sintetizado"
    assert not any(str(a).startswith("http") for a in cmd)
    try:
        M.comando_sintetizar("inexistente", "/tmp/x.wav")
    except KeyError:
        pass
    else:
        raise AssertionError("som desconhecido deveria estourar, nao sair calado")


def test_padrao_ligado_no_short_desligado_no_longo():
    """A decisao de 07/10: motion entra pelo SHORT, que e onde mora o portao
    dos tres segundos. O longo segue sem, para a atribuicao ficar limpa."""
    import motion as M
    sp = {}
    assert M.motion_ligado(sp, "s") is True
    assert M.motion_ligado(sp, "l") is False
    assert M.motion_ligado(sp) is False  # chamada antiga nao muda de sentido


def test_spec_manda_nos_dois_sentidos():
    import motion as M
    assert M.motion_ligado({"motion": True}, "l") is True
    assert M.motion_ligado({"motion": False}, "s") is False
