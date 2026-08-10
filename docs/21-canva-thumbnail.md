# Thumbnails via Canva — Setup

O pipeline usa Canva para o thumbnail final quando `thumbnail_provider: "canva"` está no
`default.yaml` (já configurado). Se os secrets faltarem, o fallback é PIL + OpenAI
automaticamente — nenhum vídeo falha por causa do Canva.

---

## Por que Canva para thumbnail?

| | PIL + OpenAI | Canva |
|---|---|---|
| Tipografia | DejaVu Bold genérico | Fontes editorials, kerning |
| Composição | Texto centralizado fixo | Template profissional (regra dos terços) |
| Marca | Nenhuma consistência | Brand Kit do canal (paleta, logo) |
| CTR esperado | Mediano | +20–40% (benchmarks de criadores) |

---

## 1. Criar a integração Canva (uma vez)

1. Acesse **developer.canva.com** → Log in com sua conta Canva
2. "Create integration" → Tipo: **API integration**
3. Escopos necessários:
   ```
   asset:read  asset:write
   design:content:read  design:content:write  design:meta:read
   ```
4. Anote o **Client ID** e o **Client Secret**

---

## 2. Criar o template de thumbnail

1. No **Canva Studio**, criar um design em branco:
   - Dimensões: **1280 × 720 px** (YouTube Thumbnail)
2. Montar o layout do canal Setiap Level:
   - Fundo: imagem que ocupará toda a área (campo nomeado **`fundo`**)
   - Texto principal no topo/diagonal: campo de texto nomeado **`titulo`**
   - Paleta: branco, traço preto, vermelho `#E63946`, amarelo `#FFD700`
3. Salvar como **Brand Template** (não como design pessoal)
4. Abrir o template → copiar o ID da URL:
   ```
   https://www.canva.com/design/DAFxxxxxxx/...
                                ^^^^^^^^^^^  ← CANVA_TEMPLATE_ID
   ```

> **Nomeação dos campos**: o pipeline busca exatamente os campos `fundo` (imagem)
> e `titulo` (texto). Se quiser outros nomes, edite `providers/canva.py` → `_autofill()`.

---

## 3. Adicionar secrets no GitHub

`github.com/sampaioopablo1-lgtm/maquina-yt-receita/settings/secrets/actions`

| Secret | Valor |
|--------|-------|
| `CANVA_CLIENT_ID` | Client ID da integração |
| `CANVA_CLIENT_SECRET` | Client Secret da integração |
| `CANVA_TEMPLATE_ID` | ID do template (ex.: `DAFxxxxxxx`) |

---

## 4. Verificar

Rode o workflow **Producao de video** com qualquer título — nos logs você verá:

```
canva: enviando imagem de fundo...
canva: autofill no template DAFxxxxxxx...
canva: exportando design DAGxxxxxxx...
thumbnail Canva salvo: out/setiap-level/slug/thumbnail.jpg
```

Se os secrets não estiverem configurados:
```
canva nao configurado (secrets ausentes) — fallback para PIL
```

---

## Fallback

`thumbnail_provider: "openai"` no `default.yaml` desativa o Canva para todos os
canais. Para desativar só para um canal específico, adicione no YAML do canal:
```yaml
thumbnail_provider: "openai"
```
