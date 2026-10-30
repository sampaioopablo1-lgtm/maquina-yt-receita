# O PACOTE DO DONO NÃO ESTÁ NO REPO — e dez citações apontavam para dentro dele

**Medido em 19/10 às 06:1x, varrendo os caminhos citados no código.** Dois
caminhos aparecem em **dez citações** espalhadas por oito arquivos — e **nenhum
dos dois existe**: não no repo, não no histórico (`git log --all` não devolve
commit nenhum para `motor/`), não neste contêiner e não no sandbox do Composio.

| caminho citado | citado em | o que ele sustenta |
|---|---|---|
| `motor/config.py` | `fabrica/temas_do_dono.py`, `fabrica/paleta_referencia.py` e três testes | os **quatro temas** e, por eles, a PALETA DOS TRÊS CANAIS |
| `motor/scenes.html` | `fabrica/fabrica.py`, `fabrica/layouts_longo.py`, um teste, o `CLAUDE.md` e o `ROTINA-NUCLEO.md` | as **coordenadas** dos layouts `comparar` e `numero` |

**É o aprendizado 743 pela SEGUNDA vez, e agora na procedência da identidade
visual da frota inteira.** Lá eu citei `references/shorts-playbook.md` em quatro
documentos por três dias, e o arquivo não existia; a regra que ficou foi **citar
caminho é afirmar que o caminho existe**, e o teste que guarda procedência tem de
ABRIR o arquivo.

**E o teste que eu escrevi para guardar isso NÃO podia pegar estes dois:** o
`test_referencia_citada_existe.py` abre **UM caminho cravado à mão**. É
identidade onde havia propriedade — a mesma classe do 743/753/761 — e por isso
ele passou verde enquanto dez citações apontavam para o vazio.

## De onde os valores vieram, de verdade

O dono entregou um pacote ZIP numa sessão anterior (*"aprenda com o vídeo, tenha
como referência, além da documentação das pastas zip. Javascripts"*, 19/10). O
pacote foi lido naquele momento e **não foi comitado** — logo o que atravessou
para o nosso código é uma **TRANSCRIÇÃO**, e ela não pode ser reconferida aqui.

**Isso não invalida os valores, e a diferença entre os dois casos importa:**

* **as CORES têm um segundo apoio, independente do pacote.** O tema `noite` do
  `labtreinamento` foi **MEDIDO no vídeo publicado dele**: luminância de fundo
  **37** contra 244 do nosso fundo antigo, e o `c2` virou painel pelo **SATAVG
  medido nos 530 quadros** do `FtCtIJPsc_Q`. Essa medição vive em
  `fabrica/video_referencia.py` e não depende de nenhum zip;
* **as COORDENADAS de `comparar` e `numero` têm apoio ÚNICO: a transcrição.**
  Não existe segunda fonte para `x=130`, `top=170`, `800x760`, `valor 300px`. Elas
  produzem cartão que o `layout.py` aprova (zero tinta na borda) e que o olho lê,
  e isso é tudo o que está verificado sobre elas.

## A consequência, e ela é uma trava

**Layout NOVO de longo não se escreve "copiando do `motor/scenes.html`"** —
não há de onde copiar. Quem construir os três que faltam (fórmula anotada,
cartão de erro, divisor de parte) tem duas saídas honestas:

1. **derivar da nossa própria grade**, reusando as frações que os dois layouts
   existentes já fixaram, e **dizer que é derivação nossa** em vez de vestir
   procedência que não existe;
2. **pedir o pacote ao dono outra vez** e comitar o arquivo no mesmo passo, e aí
   a citação volta a ser conferível.

**Enquanto o pacote não voltar, a opção 1 é a única disponível** — e ela não é
pior por isso: ela é honesta sobre o que sustenta cada número.

## O instrumento que fica

`tests/test_todo_caminho_CITADO_existe.py` varre **todos** os caminhos citados
em `fabrica/*.py`, `tests/*.py`, no `CLAUDE.md` e nos dois documentos da rotina,
e **reprova listando os que não existem** — em vez de abrir um caminho cravado.
Os dois casos conhecidos entram numa lista de **exceções DECLARADAS** que aponta
para este documento, e o teste **reprova se a lista crescer** sem que a exceção
seja escrita aqui.

## 30/10 — o pacote VOLTOU (v2.6.0) e a transcricao foi CONFERIDA, mas ele continua FORA do repo

O dono mandou `pipeline_canal_dark_v2.6.0.zip`. Ele traz `motor/config.py` e
`motor/scenes.html`, e as duas transcricoes foram conferidas contra eles:

| o que | resultado |
|---|---|
| cores dos 4 temas (`noite`, `misterio`, `papel`, `neon`), 13 chaves cada | **identicas, 52 de 52** |
| fontes de titulo e texto dos 4 temas | **identicas** |
| `comparar`: x=130/990, top=170, 800x760, borda 8 | **identico** |
| `numero`: valor 300px, top 210/330, legenda 54px top 590, nota 30px top 760 | **identico** |

Logo as coordenadas de `comparar` e `numero` deixaram de ter apoio unico na
transcricao: hoje elas tem a fonte conferida. Os tres layouts derivados
(`formula`, `erro`, `divisor`) seguem declarados como derivacao NOSSA.

**E A OPCAO 2 DESTE DOCUMENTO ("comitar o pacote") NAO ESTA DISPONIVEL**, por
dois fatos medidos no mesmo dia: o repo `sampaioopablo1-lgtm/maquina-yt-receita`
e **PUBLICO**, e a clausula 3 do `LICENCA_DE_USO.md` do produto proibe
*"revender, redistribuir, compartilhar, publicar ou sublicenciar o produto
(codigo, skills, documentos), no todo ou em parte"*. Comitar `motor/` aqui seria
publica-lo. Por isso as duas excecoes do `test_todo_caminho_CITADO_existe.py`
**continuam** — e o que mudou e que a citacao foi conferida, nao que o arquivo
passou a existir.

**Risco que ja existe e e decisao do DONO, nao minha:** o
`fabrica/temas_do_dono.py` carrega os 52 hex e as descricoes dos temas copiados
do produto, num repo publico. Tornar o repo privado resolve isso e as duas
excecoes de uma vez.

### O que a 2.6 trouxe de novo, e por que quase nada atravessa

A novidade e o **molde** (`documentario`, `animacao_2d`, `ia_no_facil`): tema,
regras de roteiro e um pacote de cenas proprio. A regra central dos tres e o
**limite de telas de texto seguidas** (`max_texto_seguido` = 1 no documentario
e na animacao) e, no documentario, **ao menos 70% dos blocos com midia**
(imagem ou clipe). Pela definicao do proprio produto, conta como tela de texto
toda cena que nao e `imagem`, `clipe`, `vinheta`, `inscreva`, `tela_final` ou
`material`.

Medido nas 40 specs de short mais recentes da frota: **279 cenas, 100% tela de
texto** (`item` 92, `titulo` 90, `cta` 38, `lista` 32, `barras` 27), **zero**
imagem ou clipe. Logo a regra do molde **dispararia em toda peca** — e aviso
que dispara sempre deixa de avisar (o argumento do `mira.py`). Ela NAO entrou.

**A distancia real nao e de regra, e de CAPACIDADE:** a resposta da 2.6 a
*"todos parecem iguais"* e MIDIA (foto, clipe, personagem 2D), e o retrato do
nosso short desenha cinco layouts, todos cartao de texto, com b-roll zero por
decisao. Fechar isso e decisao do dono: fonte de imagem (banco com licenca,
Higgsfield com credito) e um layout `imagem` no retrato.
