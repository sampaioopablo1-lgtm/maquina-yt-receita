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
