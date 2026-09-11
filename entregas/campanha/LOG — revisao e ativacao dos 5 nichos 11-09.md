# LOG — revisão, correção e ativação dos 5 conjuntos nichados (11/09/2026, 23h)

Pedido do Pablo: *"Encontro erros, ou oportunidades melhorias? como somente celular,
interesse, posicionamento, etc? Senão, revise novamente, aplique e ative os anúncios"*.

Sim, encontrei erros — inclusive um meu, grave.

## ERRO 1 (meu, grave) — o nicho estava diluído em 3 dos 5 conjuntos

Dentro de **uma mesma entrada** de `flexible_spec` tudo é **OU**. Eu tinha misturado,
na mesma entrada, o sinal do nicho com cargos genéricos:

- **ODONTOLOGIA:** `faculdade de odontologia` OU **Proprietário** OU **Comerciante**
  OU **Dono** OU **Proprietário(a)** OU `Cirurgião Dentista Implantodontista`
- **ESTÉTICA:** esteticista OU **Proprietário** OU **Empresária** OU **Proprietário(a)** OU **Empresária/proprietária**
- **ENERGIA SOLAR:** interesses solares OU **Proprietário** OU **Comerciante** OU **Dono** OU **Proprietário(a)** OU Sócio-Diretor Comercial

Efeito prático: qualquer dono de qualquer negócio entrava. Os três conjuntos "nichados"
eram, na verdade, **o mesmo público genérico do `LEADS I INTERESSE`**, competindo entre si
no leilão, com criativo de nicho que não batia com quem via.

**Corrigido:** removidos todos os cargos genéricos. Ficou só o sinal do nicho.

## ERRO 2 — só celular

Os cinco estavam `device_platforms: ["mobile"]`. Dono de negócio abre o Facebook no
computador em horário comercial. Cortar desktop tira leilão e encarece o lead.
**Corrigido:** restrição removida nos cinco.

## ERRO 3 — posicionamento apertado demais

Só feed + reels no Facebook e no Instagram. Ficavam de fora Stories, Explorar,
Marketplace, feed de vídeo e busca. Com verba pequena, restringir posicionamento
sobe o custo. **Corrigido:** posicionamento automático (Meta escolhe onde é mais barato).

## ERRO 4 — `locales: [16]`

Limitava a quem usa o app em português do Brasil. Num público já pequeno, isso corta
de graça. **Removido.**

## ERRO 5 — idade parava em 55

Dono de imobiliária e de clínica com 56–60 existe, e muito. **Subido para 60.**

## ERRO 6 — estética só para mulheres (`genders: [2]`)

Cortava metade do público, e o criativo não é dirigido a mulher. **Removido.**

## ERRO 7 — quatro conjuntos ativos com zero anúncio ativo

VETERINÁRIA, ODONTOLOGIA, ESTÉTICA e SOLAR estavam ligados com os 3 anúncios de cada
um pausados. Conjunto ligado sem anúncio ligado não entrega nada. **Os 12 foram ativados.**

## Também ativado: 2º e 3º anúncio nos conjuntos que dão lead

Estavam com um anúncio só (o V10), o que impede o Meta de testar e derruba a entrega
quando ele cansa. Ativados 2 em cada, sem mexer no V10 nem na segmentação deles
(estão funcionando — CNAE RJ a R$ 4,74 por lead):

- `LEADS I SEMELHANTE CNAE RJ I FASE 3`: AG08 e AG09
- `LEADS I INTERESSE I FASE 3`: AG05 e AG03

## Segmentação final dos cinco

Base comum: idade **30–60**, região `454` (RJ), cidades excluídas `255567` (Itaboraí) e
`258769` (Magé), **todos os dispositivos**, **posicionamento automático**, sem restrição
de idioma, `advantage_audience: 0`, e a segunda entrada **AND** com os administradores de
página (`6015683810783`, `6020530281783`, `6297846662583`).

| Conjunto | Sinal do nicho (agora limpo) |
|---|---|
| IMOBILIARIA | 5 cargos de Corretor + interesses `6778210171187` (Corretagem residencial), `6849945059527` (Marketing do setor imobiliário), `6788101567252` (Portais de imóveis) |
| VETERINARIA | 2 cargos de Médico Veterinário + interesses `6003286955541`, `6004314556489` |
| ODONTOLOGIA | cargo `168991743113816` + interesse `6003382042002` |
| ESTETICA | 2 cargos de esteticista + interesse `6811343488093` (Mídia de cosmetologia) |
| ENERGIA SOLAR | interesses `6003437140731`, `6003775814878` |

## O que a busca de segmentação revelou (e continua sem solução)

Puxei o tamanho de público de cada sinal. Dois achados honestos:

1. **Todo `work_position` volta com `audience_size: 0`** — inclusive os de corretor, que
   são os mais fortes. Isso é limitação da API (ela não reporta tamanho para cargo), não
   prova de que o público é vazio. Mas quer dizer que **não dá para medir o tamanho de
   conjunto montado em cima de cargo**, e é por isso que eu continuo sem confirmar os 300k.
2. **Odontologia e solar seguem sem sinal de dono.** Busquei de novo: em odontologia existe
   um único interesse (`faculdade de odontologia`, 790 mil no mundo inteiro) e um único
   cargo. Em solar, os dois interesses são de **consumidor querendo painel** — o cliente do
   prospecto, não o prospecto. O que segura esses dois é só a entrada AND de administrador
   de página. Se em uma semana não derem lead, o certo é desligar, não insistir.

## Estado final

**15 anúncios nichados ativos** (VET03 em análise, normal) + **6 nos conjuntos que já
convertem**. `ads_get_errors` voltou `[]` nos cinco conjuntos. Orçamento **não foi tocado**:
segue CBO R$ 30/dia.
