# LOG — 5 conjuntos nichados na campanha de formulário (11/09/2026)

Campanha: **LEADS I FORM I FS1** — `120247320350570766`
Conta: `1695865631502778` · Orçamento **CBO R$ 30,00/dia** (subido nesta data, com autorização do Pablo)
Tudo criado **PAUSADO**. Método: Windsor.ai (`create_ad` reaproveitando o criativo da V10 + `update_ad_creative`).

## Por que CBO e não R$ 6,00 por conjunto
Fase de aprendizado do Meta = 50 eventos/semana por conjunto.
Piso diário = (CPA × 50) ÷ 7. Com o CPA real de R$ 1,71 → **R$ 12,21/dia por conjunto**.
R$ 6,00 fica abaixo do piso em todos os cinco e ainda tiraria verba dos conjuntos que já geram lead.
O CBO concentra sozinho no que converte. Decisão: manter CBO.

## Os 5 conjuntos

| Conjunto | ID | Sinal de nicho na segmentação |
|---|---|---|
| LEADS I NICHO IMOBILIARIA | `120247394519840766` | 5 cargos de Corretor — **forte** |
| LEADS I NICHO VETERINARIA | `120247394531020766` | Médico Veterinário + interesses — **forte** |
| LEADS I NICHO ODONTOLOGIA | `120247394538270766` | 1 cargo + interesse faculdade — **fraca** |
| LEADS I NICHO ESTETICA | `120247394547600766` | 2 cargos de esteticista, `genders:[2]` — **média** |
| LEADS I NICHO ENERGIA SOLAR | `120247394549710766` | interesses de fotovoltaica (consumidor) — **fraca** |

Honestidade sobre as duas fracas: o catálogo do Meta **não tem um bom sinal de dono de negócio**
para odontologia, estética e energia solar. No solar o interesse disponível mira o morador que
quer painel — ou seja, o *cliente* do prospecto, não o prospecto. Quem segura esses dois é a
entrada AND de administrador de página, abaixo.

## Segmentação comum aos cinco
- `age_min: 30`, `age_max: 55`
- Região `454` (Rio de Janeiro)
- **Cidades excluídas:** `255567` (Itaboraí) e `258769` (Magé)
- facebook + instagram · feed + reels · **mobile only**
- `locales: [16]` (português BR)
- `targeting_automation: {advantage_audience: 0}`
- **Segunda entrada de `flexible_spec` (AND)** com comportamentos de administrador de página:
  - `6020530281783` Administradores de página comercial
  - `6297846662583` Admins de perfil comercial do Instagram
  - `6015683810783` Admins de Página do Facebook

Lembrete de mecanismo: entradas de `flexible_spec` são **E** entre si e **OU** dentro da mesma entrada.

## Os 15 anúncios (3 por conjunto: dor / concorrente / corte)
Cada um com o nicho nomeado na headline e foto distinta — correção pedida pelo Pablo
("cada nicho precisa ter em destaque na headline, como exemplo: Dono de Imobiliária do RJ").

- **IMOB:** `120247394564290766` "Dono de imobiliária no RJ" · `120247394581570766` "Corretor no RJ: ele aparece" · `120247394628950766` "Imobiliária do RJ que já vende"
- **VET:** `120247394636950766` "Clínica veterinária no RJ" · `120247394648600766` "Veterinário no RJ: a do lado" · `120247394669910766` "Clínica vet do RJ que atende"
- **ODO:** `120247394782230766` "Consultório odonto no RJ" · `120247394803340766` "Dentista no RJ: ele aparece" · `120247394932260766` "Odonto no RJ que já fatura"
- **EST:** `120247394938410766` "Clínica de estética no RJ" · `120247394942400766` "Estética no RJ: não é técnica" · `120247394952470766` "Estética no RJ que já fatura"
- **SOL:** `120247394959910766` "Integrador solar no RJ" · `120247394983150766` "Solar no RJ: ele só aparece" · `120247395035640766` "Solar no RJ que já instala"

Headline: **máximo 32 caracteres** (é o que a V10 usa). Acima de ~40 corta no feed.

## O que ficou sem medir
**Não consegui ler o tamanho do público.** `reach_estimate` recusou a geo com o erro
`1885364` ("Adicione pelo menos uma localização") e não achei a forma aceita pela API.
Não vou dizer que passou dos 300 mil sem ter medido. **Pablo: confere no Gerenciador;
se algum estiver abaixo de 300k, me diz qual que eu amplio** (o caminho é afrouxar a
entrada AND de administrador ou subir o teto de idade).

## Pendências
- Gerar as artes específicas de cada nicho (profissional do nicho no template da V10) — passo caro, adiado.
- Renomear os 10 criativos AG dos conjuntos da FASE 3 (herdaram o nome da V10).
- Ativar os anúncios (decisão do Pablo).
