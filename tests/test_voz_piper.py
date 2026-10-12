"""O plano B de narracao tem tres propriedades que, se cairem, matam calado.

`fabrica/voz_piper.py` nasceu em 12/10, quando o edge-tts passou a devolver 403
no handshake DO RUNNER e a maquina ficou sem conseguir produzir peca em lugar
nenhum. A rotina proibe costura vazia, entao o plano B e um provedor de
verdade — mas provedor de verdade tambem regride em silencio:

  1. ele e FALLBACK, nao substituto. Se alguem o promover a primeiro, a frota
     troca de voz para sempre sem ninguem decidir isso;
  2. a calibracao R/P do `MODELO_VOZ` e do edge-tts e NAO vale para o Piper.
     Peca narrada por aqui sem aviso vira estimativa de duracao errada
     alimentando o portao `duracao` e a mira — o erro do 679/698, usar a
     constante de uma voz para outra;
  3. as tres vozes da frota precisam estar mapeadas. Faltar uma significa um
     canal que nao produz, e o sintoma seria so um `raise` generico.
"""

import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(RAIZ / "fabrica"))

import voz_piper as VP  # noqa: E402

FROTA = ("pt-BR-ThalitaMultilingualNeural",
         "el-GR-NestorasNeural",
         "pl-PL-MarekNeural")


def test_as_TRES_vozes_da_frota_estao_mapeadas():
    """Conferidas por HEAD no run 38202568056: as quatro existem publicadas."""
    assert set(VP.VOZES) == set(FROTA)
    for v, (caminho, nome) in VP.VOZES.items():
        assert caminho.endswith(("/low", "/medium", "/high")), v
        assert nome and "/" not in nome, v


def test_o_mapa_e_chaveado_pela_voz_do_EDGE():
    """Assim nenhuma spec muda para o fallback funcionar."""
    assert all(v.count("-") >= 2 and "Neural" in v for v in VP.VOZES)


def test_o_piper_entra_SO_depois_das_tres_tentativas_do_edge():
    """Promove-lo a primeiro trocaria a voz da frota sem ninguem decidir."""
    fonte = _vozes_fonte()
    # O fallback vive DENTRO do ramo da terceira tentativa.
    assert "if tentativa == 2:" in fonte
    i_edge = fonte.index("edge_tts.Communicate")
    i_pip = fonte.index("voz_piper")
    assert i_edge < i_pip, "o Piper nao pode ser tentado antes do edge-tts"


def _vozes_fonte() -> str:
    """O TEXTO da funcao `vozes`, sem importar fabrica.py (que puxa cairosvg)."""
    texto = (RAIZ / "fabrica/fabrica.py").read_text()
    i = texto.index("async def vozes(")
    j = texto.index("\nfrom caminhos import", i)
    return texto[i:j]


def test__vozes_fonte_pega_mesmo_a_funcao():
    """Se o recorte errar, os testes acima passam por VACUIDADE."""
    fonte = _vozes_fonte()
    assert "async def vozes(" in fonte and "edge_tts.Communicate" in fonte


def test_toda_peca_do_piper_sai_com_AVISO_de_calibracao():
    """Sem isso, a estimativa de duracao mente e o portao nao sabe."""
    msg = VP.aviso_de_calibracao("pt-BR-ThalitaMultilingualNeural")
    assert msg.startswith("::warning::")
    for pedaco in ("PIPER", "MODELO_VOZ", "NAO valem", "duracao"):
        assert pedaco in msg, pedaco
    fonte = _vozes_fonte()
    assert "aviso_de_calibracao" in fonte, (
        "o aviso existe mas ninguem o imprime — pior que nao existir")


def test_voz_desconhecida_devolve_None_em_vez_de_adivinhar():
    assert VP.modelo("xx-XX-InexistenteNeural") is None


def test_o_length_scale_reproduz_o_rate_do_edge():
    """O edge e chamado com rate=-4%; aqui isso vira duracao 1/0,96."""
    assert abs(VP.LENGTH_SCALE - 1 / 0.96) < 1e-9
    fonte = (RAIZ / "fabrica/fabrica.py").read_text()
    assert 'rate="-4%"' in fonte, (
        "se o rate do edge mudar, o LENGTH_SCALE tem de mudar junto")


def test_sintetiza_devolve_False_quando_o_modelo_nao_baixa(monkeypatch):
    """Falha de rede nao pode virar mp3 vazio passando por bom."""
    monkeypatch.setattr(VP, "modelo", lambda v: None)
    assert VP.sintetiza("oi", "pt-BR-ThalitaMultilingualNeural", "/tmp/x.mp3") is False


def test_o_FROTA_instala_o_piper():
    """Plano B que a producao nao instala e plano B decorativo.

    Run 38211497370: o edge-tts deu 403 na frota, `VP.disponivel()` devolveu
    False porque o `frota.yml` instalava so edge-tts/cairosvg/pydantic/pillow,
    e o erro subiu cru — exatamente a falha que o fallback existe para evitar.
    O codigo estava certo; o ambiente que o usa nao tinha o pacote.
    """
    yml = (RAIZ / ".github/workflows/frota.yml").read_text()
    linha = next(l for l in yml.splitlines() if "pip install" in l and "edge-tts" in l)
    assert "piper-tts" in linha, linha


def test_o_TESTE_de_ponta_a_ponta_tambem_instala():
    """Senao o teste exercita um caminho que a producao nao tem."""
    yml = (RAIZ / ".github/workflows/teste-ponta.yml").read_text()
    assert "piper-tts" in yml
