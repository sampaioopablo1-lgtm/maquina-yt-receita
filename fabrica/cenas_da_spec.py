"""O guarda do argumento `cenas` — ele RECUSA a spec em vez de a aceitar.

**POR QUE ELE EXISTE (22/10, 09:3x): eu passei a SPEC onde a funcao quer a lista
de CENAS, e o erro saiu em `ensaio.py:234` dizendo
`'str' object has no attribute 'get'`.** Erro de TIPO, apontando uma linha de um
modulo que o chamador nunca tocou — exatamente o que a nota de 22/10 as 04:4x
nomeia: *"LEVANTA com motivo de DADO em vez de deixar o `open(None)` dar erro de
TIPO — erro de tipo manda conferir no lugar errado"*.

**A DIVERGENCIA ESTA MEDIDA, e e ela que torna o engano facil:** varridas as
funcoes PUBLICAS da fabrica por AST, **55 recebem `spec` na primeira posicao e
14 recebem `cenas`** — e entre as 14 estao as tres de duracao
(`duracao_estimada`, `duracao_estimada_short`, `duracao_real_prevista`) que a
mira, o portao e todo instrumento de redacao leem. Logo a forma COMUM da fabrica
e passar a spec, e as funcoes de duracao sao a minoria.

**A FALHA E RUIDOSA e isso vai dito em vez de inflado: as 14 LEVANTAM hoje**,
nenhuma e permissiva — medido uma a uma. O que este modulo conserta nao e o
veredito, e o ENDERECO: quem le `ensaio.py:234` vai conferir o `ensaio`, quando
o engano esta na propria chamada.

**E O RAMO PERMISSIVO EXISTE E QUASE ME ENGANOU:** funcao que so fizesse
`len(cenas)` devolveria o numero de CHAVES da spec, e na peca desta rodada
`len(spec)` e `len(spec["short"])` valem **os dois 11** — concordancia por
ACIDENTE, do tipo que a nota de 22/10 as 01:1x descreve. Nenhuma das 14 faz isso
hoje; o guarda fecha a porta antes de alguma fazer.

**ELE NAO ACEITA AS DUAS FORMAS, de proposito.** Extrair `spec["short"]` aqui
daria ao argumento `cenas` um SEGUNDO significado, que e a assinatura do
`exceto` de 20/10 as 11:3x — o mesmo nome com duas convencoes em modulos irmaos,
que falhava em silencio nos dois sentidos. Ele RECUSA com o motivo e diz qual
campo passar, do jeito que o `porta1` recusa janela curta.
"""

CAMPOS = ("short", "longo")


class CenasTrocadas(ValueError):
    """A spec foi passada onde a funcao quer a LISTA de cenas."""


def parece_spec(cenas) -> bool:
    """A spec e um dicionario; a lista de cenas e uma lista.

    O discriminador e o TIPO e nao a presenca de um campo: dicionario que nao
    tenha `short` nem `longo` tambem nao e lista de cenas, e dizer 'nao e spec'
    sobre ele mandaria o chamador procurar outro defeito.
    """
    return isinstance(cenas, dict)


def exige(cenas, quem: str = ""):
    """Devolve `cenas` ou LEVANTA com motivo de DADO, nomeando o campo.

    `quem` e o nome da funcao que chama, para o motivo apontar o lugar certo —
    sem ele a mensagem diria onde o erro foi DETECTADO, que e o defeito que este
    modulo conserta.
    """
    if not parece_spec(cenas):
        return cenas
    tem = [c for c in CAMPOS if isinstance(cenas.get(c), list)]
    onde = (" em %s" % quem) if quem else ""
    if tem:
        return _recusa(
            "a SPEC foi passada onde%s se espera a lista de CENAS. Passe"
            " `spec[%r]`%s — e nao a spec, porque aceitar as duas formas daria"
            " ao argumento `cenas` um SEGUNDO significado (20/10 as 11:3x)."
            % (onde, tem[0],
               " ou `spec[%r]`" % tem[1] if len(tem) > 1 else ""))
    return _recusa(
        "um dicionario foi passado onde%s se espera a lista de CENAS, e ele nao"
        " tem nenhum dos campos %s. Se e uma spec, passe o campo de cenas; se"
        " nao e, o defeito esta antes desta chamada." % (onde, list(CAMPOS)))


def _recusa(motivo: str):
    raise CenasTrocadas(motivo)
