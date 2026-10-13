"""O stdout do `estado_ponte.py` e base64 PURO -- nada mais sai por ele.

POR QUE ESTE ARQUIVO EXISTE, e e um defeito MEDIDO de 13/10 as 15:1x.

O run 38420599010 do `retomar.yml` morreu em `base64: invalid input`, e a causa
era minha: eu montei o estado com

    python3 fabrica/estado_ponte.py > arq 2>&1

O `2>&1` anexou ao arquivo a NOTA que o script escreve em stderr de proposito
("estado: 269 titulos | 29396 chars b64"), e o `tr -d '\n'` seguinte colou a
nota no fim do base64. O runner recebeu base64 corrompido.

O script JA ESTAVA CERTO -- a nota ja ia para stderr. O defeito foi eu
redirecionar stderr para dentro do payload. Entao o que este teste trava NAO e
um conserto: e a propriedade da qual eu dependi sem conferir, para que ninguem
mova a nota para stdout depois e reconstrua a falha calado.

E e a TERCEIRA vez que o `estado_b64` montado por mim mata um run:
  - 12/10, run 38290045583: `titulos_no_ar` como lista de strings;
  - 13/10, run 38420599010: nota de stderr concatenada ao base64.
As duas vezes a licao foi a mesma -- nao improvisar em volta do modulo.
"""
import base64
import json
import subprocess
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
SCRIPT = RAIZ / "fabrica" / "estado_ponte.py"


def _roda():
    return subprocess.run(
        [sys.executable, str(SCRIPT)], cwd=RAIZ,
        capture_output=True, text=True, timeout=120)


def test_o_stdout_decodifica_sozinho_sem_nenhuma_limpeza():
    """Sem tr, sem head, sem strip de nada alem do \\n final do print."""
    r = _roda()
    assert r.returncode == 0, r.stderr
    bruto = r.stdout.strip()
    assert bruto, "stdout vazio"
    est = json.loads(base64.b64decode(bruto, validate=True))
    assert isinstance(est, dict)


def test_o_stdout_tem_UMA_linha_so():
    """Mais de uma linha e o que faz `tr -d` virar necessario, e `tr -d`
    sobre stdout+stderr foi exatamente o que corrompeu o run 38420599010."""
    r = _roda()
    assert len(r.stdout.strip().splitlines()) == 1, r.stdout[:200]


def test_a_NOTA_legivel_vai_para_stderr_e_NAO_para_stdout():
    r = _roda()
    assert "estado:" in r.stderr and "chars b64" in r.stderr, r.stderr
    assert "estado:" not in r.stdout
    assert "chars b64" not in r.stdout


def test_a_nota_de_stderr_NAO_e_base64_valido__era_o_que_matava_o_run():
    """Prova que o defeito era real: colar a nota no fim quebra o decode."""
    r = _roda()
    emendado = (r.stdout.strip() + r.stderr.strip()).replace("\n", "")
    try:
        base64.b64decode(emendado, validate=True)
    except Exception:
        return
    raise AssertionError(
        "a nota emendada decodificou -- este teste perdeu o sentido")


def test_o_estado_traz_titulos_no_ar_n__senao_o_runner_recusa():
    """Aprendizado 718: sem esta chave o `retomar.yml` para em
    'Conferir o estado antes de publicar'."""
    r = _roda()
    est = json.loads(base64.b64decode(r.stdout.strip(), validate=True))
    assert "titulos_no_ar_n" in est
    assert est["titulos_no_ar_n"] == len(est["titulos_no_ar"])


def test_titulos_no_ar_e_lista_de_OBJETOS_com_a_chave_titulo():
    """O outro erro meu, de 12/10 (run 38290045583): lista de strings faz a
    trava por titulo levantar AttributeError dentro do runner."""
    r = _roda()
    est = json.loads(base64.b64decode(r.stdout.strip(), validate=True))
    assert est["titulos_no_ar"], "lista vazia nao prova nada"
    for item in est["titulos_no_ar"]:
        assert isinstance(item, dict), item
        assert isinstance(item.get("titulo"), str) and item["titulo"]
