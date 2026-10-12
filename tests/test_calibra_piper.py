"""A calibracao do Piper tem quatro propriedades que, se cairem, mentem calado.

`fabrica/calibra_piper.py` nasceu em 12/10, um dia depois de a frota passar a
narrar pelo Piper em producao (`byriXB1gSg8`). O risco aqui nao e o script nao
rodar — e ele rodar e produzir numero com cara de medido:

  1. **amostra deterministica.** Medicao que muda de resultado a cada execucao
     nao pode ser comparada com a proxima, e foi comparacao entre medicoes que
     pegou o vies de +6,6% a +18,0% em 17/08;
  2. **nao escreve em `ensaio.py`.** Trocar constante de producao a partir de
     laboratorio e decisao. Script que edita a tabela sozinho transforma "rodei
     para ver" em mudanca de producao;
  3. **silencio nao e leitura de zero** (665/708). Cena que nao sintetizou sai
     da amostra e vai CONTADA, nunca entra como duracao zero — zero puxaria o R
     para cima e o erro apareceria como "o Piper e mais rapido";
  4. **amostra pequena nao calibra.** Com n pequeno o ajuste de minimos
     quadrados devolve numero de qualquer jeito, sem avisar.
"""

import ast
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "fabrica"))

FONTE = (RAIZ / "fabrica/calibra_piper.py").read_text()


def test_a_amostra_e_deterministica_e_nao_aleatoria():
    arvore = ast.parse(FONTE)
    importados = set()
    for no in ast.walk(arvore):
        if isinstance(no, ast.Import):
            importados |= {a.name for a in no.names}
        elif isinstance(no, ast.ImportFrom):
            importados.add(no.module or "")
    assert "random" not in importados, (
        "amostra aleatoria nao se compara com a medicao da proxima rodada")
    assert "passo = len(itens) / max_cenas" in FONTE


def test_nao_escreve_em_ensaio_nem_em_spec_nenhuma():
    """Rodar para ver nao pode virar mudanca de producao.

    Conferido pela ARVORE, nao por substring: um `grep` de `'w'` passa por
    vacuidade no dia em que alguem escrever `mode="w"` ou usar `pathlib`.
    """
    arvore = ast.parse(FONTE)
    for no in ast.walk(arvore):
        if isinstance(no, ast.Call):
            nome = getattr(no.func, "id", None) or getattr(no.func, "attr", None)
            if nome in ("open", "write_text", "write_bytes"):
                modos = [a.value for a in no.args[1:] + [k.value for k in no.keywords]
                         if isinstance(a, ast.Constant) and isinstance(a.value, str)]
                assert not any("w" in m or "a" in m for m in modos), ast.dump(no)
                assert nome == "open", nome
    assert "MODELO_VOZ" in FONTE, "tem de comparar com a tabela de hoje"
    assert "NAO colei em ensaio.MODELO_VOZ" in FONTE


def test_cena_que_nao_sintetizou_sai_da_amostra_e_vai_CONTADA():
    """Zero como duracao puxaria o R para cima e mentiria para o lado bom."""
    assert "falhas += 1" in FONTE
    assert "d <= 0.2" in FONTE, "duracao absurda tambem e falha, nao dado"
    # o retorno de `mede` carrega as falhas, entao o relato nao pode omiti-las
    assert "return C, F, D, falhas" in FONTE
    assert "falhas={falhas}" in FONTE


def test_amostra_pequena_NAO_calibra_e_diz_isso():
    assert "n < 20" in FONTE
    assert "NAO calibre com isto" in FONTE


def test_reusa_o_ajuste_do_calibra_voz_em_vez_de_reimplementar():
    """Dois minimos quadrados divergem com o tempo; um nao."""
    assert "from calibra_voz import ajusta" in FONTE


def test_o_workflow_instala_o_piper_e_o_ffprobe():
    yml = (RAIZ / ".github/workflows/calibra-piper.yml").read_text()
    assert "piper-tts" in yml
    assert "ffmpeg" in yml, "sem ffprobe nao ha duracao"
    assert "calibra_piper.py" in yml


def test_os_confundidores_estao_declarados_no_proprio_modulo():
    """Numero de laboratorio sem ressalva escrita vira numero da frota."""
    for pedaco in ("CONFUNDIDORES", "SINTETIZADOR, nao a esteira",
                   "LENGTH_SCALE", "low"):
        assert pedaco in FONTE, pedaco


def test_a_distincao_com_o_calibra_voz_esta_escrita():
    """Quem ler os dois tem de saber por que existem os dois."""
    assert "nao e `calibra_voz.py`" in FONTE
    assert "17/08" in FONTE
