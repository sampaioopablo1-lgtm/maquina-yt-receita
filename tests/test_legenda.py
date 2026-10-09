"""A legenda queimada em pedaços. Ver `fabrica/legenda.py`.

O defeito que estes testes travam: uma fala só para a cena inteira deixava ~18
palavras paradas na tela por oito segundos, e era a região que o olho lê.
"""
import legenda


def _falas(srt: str) -> list[str]:
    return [b.strip().splitlines()[-1] for b in srt.split("\n\n") if b.strip()]


def test_quebra_em_grupos_de_quatro_palavras():
    assert legenda.pedacos("uma duas tres quatro cinco seis") == [
        "uma duas tres quatro", "cinco seis"]


def test_nunca_quebra_palavra_ao_meio():
    nar = "antecedencia incompreensibilidade caracteristicamente"
    for g in legenda.pedacos(nar):
        for p in g.split():
            assert p in nar.split(), f"{p!r} nao e palavra inteira"


def test_uma_cena_de_nove_segundos_vira_varias_falas():
    nar = ("Voce multiplicou as duas notas e achou o nivel. Agora precisa "
           "dizer onde comeca o alto, e e ai que a planilha trava.")
    falas = _falas(legenda.srt(nar, 9.1))
    assert len(falas) >= 5, f"so {len(falas)} falas — continua quase congelado"


def test_o_texto_inteiro_sobrevive_a_quebra():
    nar = "Chegou a norma eletrica nova e voce pediu o estudo no mesmo dia."
    assert " ".join(_falas(legenda.srt(nar, 8.0))) == nar


def test_as_falas_nao_se_sobrepoem_e_ficam_dentro_da_cena():
    nar = " ".join(f"palavra{i}" for i in range(24))
    dur = 9.0
    blocos = [b for b in legenda.srt(nar, dur).split("\n\n") if b.strip()]
    fim_ant = 0.0
    for b in blocos:
        marca = b.splitlines()[1]
        ini, fim = (x.strip().replace(",", ".") for x in marca.split("-->"))

        def seg(t):
            h, m, s = t.split(":")
            return int(h) * 3600 + int(m) * 60 + float(s)

        assert seg(ini) >= fim_ant - 1e-6, "fala comecou antes da anterior acabar"
        assert seg(fim) <= dur + 1e-6, "fala passou do fim da cena"
        fim_ant = seg(fim)


def test_cena_curta_junta_grupos_em_vez_de_piscar():
    """Frase longa em cena curta nao pode virar pisca-pisca ilegivel."""
    nar = " ".join(f"palavra{i}" for i in range(30))
    blocos = [b for b in legenda.srt(nar, 2.5).split("\n\n") if b.strip()]
    for b in blocos:
        ini, fim = (x.strip().replace(",", ".")
                    for x in b.splitlines()[1].split("-->"))

        def seg(t):
            h, m, s = t.split(":")
            return int(h) * 3600 + int(m) * 60 + float(s)

        assert seg(fim) - seg(ini) >= legenda.MIN_S - 1e-6, "fala abaixo do minimo"


def test_narracao_vazia_devolve_vazio():
    assert legenda.srt("", 5.0) == ""
    assert legenda.srt("   ", 5.0) == ""


def test_grupo_longo_fica_mais_tempo_que_grupo_curto():
    """O tempo e proporcional aos CARACTERES: 'e' e 'antecedencia' nao se leem
    no mesmo tempo, e repartir igual fazia o grupo longo sumir antes de ser
    lido."""
    nar = "a b c d antecedencia incompreensibilidade caracteristicamente xyzw"
    blocos = [b for b in legenda.srt(nar, 8.0).split("\n\n") if b.strip()]

    def dur(b):
        ini, fim = (x.strip().replace(",", ".")
                    for x in b.splitlines()[1].split("-->"))

        def seg(t):
            h, m, s = t.split(":")
            return int(h) * 3600 + int(m) * 60 + float(s)

        return seg(fim) - seg(ini)

    assert dur(blocos[1]) > dur(blocos[0]), "o grupo de palavras longas ficou menos tempo"
