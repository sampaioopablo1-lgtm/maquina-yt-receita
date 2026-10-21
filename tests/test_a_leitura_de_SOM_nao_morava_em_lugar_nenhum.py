# -*- coding: utf-8 -*-
"""A leitura de SOM da peca publicada nao era parqueada por ninguem.

Toda rodada eu lia o `::notice:: SOM` da anotacao, escrevia os numeros no relato
e eles acabavam ali — e a medida de "NOVE dos 38 renders acima do teto", escrita
no docstring do `som.py`, foi contada A MAO na API, com o proprio comentario
dizendo que nenhum teste a reconfere. Este arquivo existe para que ela passe a
ser reconferivel, e para travar as tres decisoes do modulo: o VEREDITO nao e
parqueado, a CHAVE e (pacote, arquivo), e o teto tem UM dono.
"""
import ast
import io
import json
import os
import subprocess
import sys

import pytest

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "fabrica"))

import som                       # noqa: E402
import som_parqueado as SPQ      # noqa: E402

FONTE = io.open(os.path.join(RAIZ, "fabrica", "som_parqueado.py"),
                encoding="utf-8").read()


def _parque():
    regs = SPQ.carrega()
    assert len(regs) >= SPQ.MINIMO_PARA_AFIRMAR, (
        "o parque do disco tem %d linha(s) e o minimo para afirmar e %d —"
        " contar os tres estados com menos que isso e vacuidade, que e o"
        " defeito do 743 em forma de glob" % (len(regs), SPQ.MINIMO_PARA_AFIRMAR))
    return regs


def test_o_parque_existe_no_disco_e_nao_e_vacuo():
    regs = _parque()
    assert all(r.get("pacote") and r.get("arquivo") and r.get("job")
               for r in regs), (
        "toda linha carrega pacote, arquivo e job — os dois ultimos sao a"
        " PROCEDENCIA, e foi a falta dela que deixou passar o job inventado de"
        " 20/10 as 14:3x")


def test_os_TRES_estados_existem_no_parque():
    """Se um deles desaparecer, esta nota se rele em vez de o numero ser movido.

    Sem `clipa` o relato nunca exercita o ramo do DEFEITO; sem `acima_do_teto` o
    modulo perde o objeto, porque foi essa faixa que o produziu; e sem `dentro`
    a leitura estaria toda fora e o problema seria outro.
    """
    d = SPQ.distribuicao(_parque())
    c = d["contagem"]
    for estado in ("dentro", "acima_do_teto", "clipa"):
        assert c.get(estado, 0) > 0, (
            "o parque nao tem nenhuma linha em %r (%r) — com um dos tres"
            " estados ausente a contagem deixa de medir o que este arquivo"
            " afirma, e a nota tem de ser RELIDA" % (estado, c))
    assert d["afirma"] is True


def test_o_VEREDITO_nao_e_parqueado_e_o_teto_tem_UM_dono():
    """O parque guarda a MEDIDA; quem julga e o `som.pico_acima_do_teto`.

    Gravar o `pico_vs_teto` que a anotacao traz pronto seria congelar um
    veredito feito com um teto que pode mudar — o segundo dono da mesma regra,
    a assinatura que congelou a legenda.
    """
    regs = _parque()
    assert not any("pico_vs_teto" in r for r in regs), (
        "alguma linha gravou o veredito: ele e DERIVADO, nunca parqueado")
    arvore = ast.parse(FONTE)
    for no in ast.walk(arvore):
        if isinstance(no, ast.Assign):
            for alvo in no.targets:
                assert not (isinstance(alvo, ast.Name)
                            and alvo.id == "TP_MAX_DBTP"), (
                    "o teto foi redefinido aqui — ele mora no `som.py` e copia-lo"
                    " cria o SEGUNDO dono")
        if isinstance(no, ast.Constant) and isinstance(no.value, float):
            assert no.value != som.TP_MAX_DBTP, (
                "o valor do teto aparece cravado no modulo em vez de ser lido"
                " do dono (753)")
    chamadas = {ast.unparse(n.func) for n in ast.walk(arvore)
                if isinstance(n, ast.Call)}
    assert "som.pico_acima_do_teto" in chamadas, (
        "o veredito tem de ser DELEGADO ao dono do teto")
    assert "canal.do_pacote" in chamadas, (
        "a derivacao do canal e do `canal.do_pacote` desde 19/10 as 05:2x —"
        " refaze-la aqui seria a quarta forma de slug outra vez")
    assert "rsplit" not in FONTE, (
        "o modulo derivou canal por conta propria em vez de delegar")


def _pacote_com_dois_arquivos(regs):
    por = {}
    for r in regs:
        por.setdefault(r["pacote"], set()).add(r["arquivo"])
    for pac, arqs in sorted(por.items()):
        if len(arqs) >= 2:
            return pac, sorted(arqs)
    return None, None


def test_a_CHAVE_e_pacote_mais_ARQUIVO_e_o_caso_vem_do_DISCO():
    """O pacote emite DUAS anotacoes — `longo.mp4` e `short.mp4`.

    Pego na PRIMEIRA execucao da semeadura: chave por pacote sozinho leu as duas
    como leitura discordante da MESMA peca e levantou. A guarda estava certa e a
    chave estava errada, e e a mesma forma do defeito do `registro_videos` de
    19/10 as 13:0x — la o `on conflict do nothing` descartava uma EM SILENCIO.

    O caso e DERIVADO do disco: nomear o `labtreinamento-014` seria identidade
    onde ha propriedade (743/753/761).
    """
    regs = _parque()
    pac, arqs = _pacote_com_dois_arquivos(regs)
    assert pac is not None, (
        "nenhum pacote do parque tem DUAS leituras de som — o arquivo PERDEU A"
        " ANCORA e nao mede mais o defeito que o produziu; semeie um pacote"
        " (longo + short) antes de relaxar isto")
    picos = {r["arquivo"]: r["pico_dbtp"] for r in regs if r["pacote"] == pac}
    assert len(set(picos.values())) >= 2, (
        "as duas leituras de %s tem o MESMO pico (%r), logo elas nao"
        " exercitariam a guarda de divergencia" % (pac, picos))
    assert len({SPQ.chave(r) for r in regs if r["pacote"] == pac}) == 2, (
        "a chave colapsou as duas leituras do mesmo pacote")


def test_divergencia_LEVANTA_e_repeticao_identica_NAO(tmp_path):
    """Contraprova nos DOIS sentidos: sem ela bastaria aceitar tudo."""
    p = str(tmp_path / "som.jsonl")
    base = ('SOM short.mp4 canal-teste-s001 {"lufs": -14.0, "lra": 2.0,'
            ' "pico_dbtp": -3.0, "desvio_do_alvo": 0.0, "silencios": []}')
    r1 = SPQ.do_notice(base, job="111", run="999")
    SPQ.parqueia(r1, caminho=p)
    assert len(SPQ.carrega(p)) == 1
    SPQ.parqueia(SPQ.do_notice(base, job="111", run="999"), caminho=p)
    assert len(SPQ.carrega(p)) == 1, "leitura identica nao duplica a linha"
    outro = base.replace('"pico_dbtp": -3.0', '"pico_dbtp": -1.2')
    with pytest.raises(SPQ.SemProcedencia):
        SPQ.parqueia(SPQ.do_notice(outro, job="111", run="999"), caminho=p)
    # e o MESMO pacote em outro ARQUIVO entra, porque sao duas pecas
    longo = base.replace("short.mp4", "longo.mp4").replace(
        '"pico_dbtp": -3.0', '"pico_dbtp": -1.2')
    SPQ.parqueia(SPQ.do_notice(longo, job="111", run="999"), caminho=p)
    assert len(SPQ.carrega(p)) == 2, (
        "longo e short do mesmo pacote sao DUAS leituras e as duas entram")


def test_sem_procedencia_LEVANTA_em_vez_de_parquear_calado():
    base = ('SOM short.mp4 canal-teste-s002 {"lufs": -14.0,'
            ' "pico_dbtp": -3.0}')
    with pytest.raises(SPQ.SemProcedencia):
        SPQ.do_notice(base, job="")
    with pytest.raises(SPQ.SemProcedencia):
        SPQ.do_notice("isto nao e um notice de SOM", job="111")
    with pytest.raises(SPQ.SemProcedencia):
        SPQ.do_notice('SOM short.mp4 canal-teste-s002 {"lufs": -14.0}',
                      job="111")
    assert SPQ.OBRIGATORIOS == ("pacote", "arquivo", "job", "pico_dbtp")


def test_o_fato_de_a_anotacao_trazer_o_veredito_tem_os_DOIS_valores():
    """Sem os dois lados a frase das "51 de 60" nao tem objeto.

    E o numero e RECONFERIDO contra o parque em vez de confiado ao texto (753):
    a primeira versao do `distribuicao` procurava `pico_vs_teto` DENTRO do
    registro — que nunca esta la, porque o veredito nao e parqueado — e por isso
    o relato dizia "60 de 60" onde a medida e 51. Era o relato medindo outra
    coisa, pego na semeadura.
    """
    regs = _parque()
    valores = {bool(r.get("tinha_veredito")) for r in regs}
    assert valores == {True, False}, (
        "o parque tem so %r em `tinha_veredito` — com um lado ausente a frase"
        " do campo que nasceu em 21/10 deixa de medir nada" % valores)
    d = SPQ.distribuicao(regs)
    a_mao = sum(1 for r in regs if not r.get("tinha_veredito"))
    assert d["sem_o_campo_na_anotacao"] == a_mao, (
        "a contagem do relato divergiu de uma recontagem do parque")
    assert ("%d das %d" % (a_mao, len(regs))) in SPQ.relato(regs), (
        "o numero impresso nao e o que o parque diz")


def test_os_denominadores_por_canal_e_a_ressalva_que_o_parque_DESMENTIU():
    """A ressalva saiu antes da medida, e a medida a derrubou.

    Eu escrevi "os denominadores diferem" por habito; medidos, eles saem IGUAIS.
    Este teste cobra a propriedade que de fato existe, e **falha se eles
    deixarem de ser iguais** — porque ai a frase do relato tem de ser relida em
    vez de ficar.
    """
    d = SPQ.distribuicao(_parque())
    pc = d["por_canal"]
    assert len(pc) >= 3, "o parque cobre menos de tres canais: %r" % list(pc)
    ns = {c: v["n"] for c, v in pc.items()}
    assert len(set(ns.values())) == 1, (
        "os denominadores por canal deixaram de ser iguais (%r) — a frase do"
        " relato foi escrita sobre a igualdade e tem de ser RELIDA" % ns)
    assert "DENOMINADORES saem IGUAIS" in SPQ.relato(), (
        "a medida saiu do relato")
    assert "NAO afirma" in SPQ.relato(), (
        "a ressalva de que voz e conteudo andam juntos saiu do relato")


def test_a_RECUSA_tem_UM_dono_e_sai_so_no_parque_curto():
    curto = [{"pacote": "a-s1", "arquivo": "short.mp4", "job": "1",
              "pico_dbtp": -3.0}]
    r = SPQ.relato(curto)
    assert "NAO AFIRMA" in r, "parque curto tem de RECUSAR, nao contar"
    assert "dentro do teto:" not in r, (
        "ele contou os tres estados num parque de uma linha")
    assert "NAO AFIRMA" not in SPQ.relato(_parque()), (
        "a recusa apareceu com o parque cheio — recusa que sai sempre deixa de"
        " avisar, que e o argumento pelo qual o `mira.py` nao e portao")
    arvore = ast.parse(FONTE)
    donos = [n for n in ast.walk(arvore)
             if isinstance(n, ast.FunctionDef) and "NAO AFIRMA" in
             ast.unparse(n)]
    assert [n.name for n in donos] == ["_linha_da_recusa"], (
        "a frase da recusa tem mais de um dono: %r" % [n.name for n in donos])


def test_NAO_e_portao_e_o_codigo_de_saida_e_ZERO():
    r = subprocess.run([sys.executable,
                        os.path.join(RAIZ, "fabrica", "som_parqueado.py")],
                       capture_output=True, text=True, cwd=RAIZ)
    assert r.returncode == 0, (
        "ele reprovou: `acima_do_teto` e LEITURA e nao defeito, e um portao"
        " aqui reprovaria dez pecas que ja estao no ar.\n%s" % r.stderr[-800:])
    assert "SOM PARQUEADO" in r.stdout
    arvore = ast.parse(FONTE)
    for no in ast.walk(arvore):
        if isinstance(no, ast.Call) and ast.unparse(no.func) == "sys.exit":
            arg = ast.unparse(no.args[0]) if no.args else ""
            assert "main" in arg, (
                "o modulo sai com algo que nao e o `main`, que devolve zero")


def test_a_semente_tem_PROCEDENCIA_de_run_e_job():
    """Semente sem run e job seria memoria minha com cara de dado."""
    regs = _parque()
    com = [r for r in regs if r.get("run")]
    assert len(com) >= SPQ.MINIMO_PARA_AFIRMAR, (
        "menos de %d linhas trazem o `run` que as emitiu — a semente perde a"
        " procedencia" % SPQ.MINIMO_PARA_AFIRMAR)
    assert all(str(r["job"]).isdigit() for r in com), (
        "algum `job` nao e numero de job do GitHub")
    bruto = io.open(os.path.join(RAIZ, "docs", "pendente", "som-medido.jsonl"),
                    encoding="utf-8").read().strip().splitlines()
    assert len(bruto) == len(regs), "o parque no disco nao bate com o carregado"
    for linha in bruto[:5]:
        json.loads(linha)
