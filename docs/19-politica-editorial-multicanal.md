# Política Editorial — Produtora Multilíngue

> Documento de referência para operação de múltiplos canais simultâneos.
> Última revisão: 2026-08-10.

## Objetivo

Operar até 10 canais em diferentes países e idiomas. Volume máximo: 10 vídeos/canal/dia.

**Ordem de prioridade (não inverter):**
1. Originalidade
2. Valor real para o espectador
3. Retenção
4. Diferenciação entre vídeos
5. Adequação cultural ao país
6. Conformidade com políticas do YouTube
7. Escalabilidade
8. Volume

10 vídeos/dia é LIMITE MÁXIMO, não obrigação. Se 4 passarem no gate, publique 4.

---

## Regra Absoluta — Proibido traduzir e replicar

Nunca executar: roteiro original → tradução → mesma estrutura → mesmo vídeo em outro idioma.

O mesmo **tema** pode existir em canais diferentes. O mesmo **vídeo** não.

Para cada canal reconstruir editorialmente:
- ângulo, abertura, exemplos, narrativa, estrutura, imagens, título, thumbnail
- vocabulário e CTA adaptados ao mercado
- pesquisar contexto local antes de criar

---

## Localização Cultural

Antes de criar, definir:

```
PAÍS:
IDIOMA:
PERSONA:
NÍVEL CULTURAL:
INTERESSE CENTRAL:
PROMESSA DO VÍDEO:
POR QUE ALGUÉM DESTE PAÍS ASSISTIRIA:
QUAL É O ELEMENTO ORIGINAL DESTE VÍDEO:
```

Se a última pergunta não tiver resposta convincente → **NÃO PRODUZIR**.

---

## Teste de Originalidade (antes da renderização)

1. Este vídeo possui uma ideia central própria?
2. Ele entrega algo diferente dos últimos vídeos?
3. A abertura é diferente?
4. A progressão narrativa é diferente?
5. Os exemplos são diferentes?
6. Os visuais foram criados para esta narrativa?
7. O espectador que assistir 5 vídeos seguidos perceberá conteúdo novo?
8. Existe começo, desenvolvimento e conclusão?
9. O conteúdo educa, informa ou conta uma história de forma clara?
10. Ele existiria mesmo se monetização não fosse o objetivo?

Qualquer resposta crítica NÃO → **REPROVAR E REFAZER**.

---

## Quality Score (0–100)

| Dimensão | Peso |
|---|---|
| Originalidade | 25 |
| Valor para audiência | 20 |
| Narrativa | 15 |
| Adequação cultural | 10 |
| Qualidade visual | 10 |
| Narração | 10 |
| Metadata | 5 |
| Compliance | 5 |

**Publicar somente se SCORE ≥ 80.** Se < 80, reformular — não publicar para cumprir quota.

---

## Proibições Editoriais

Não publicar:
- slideshow genérico ou textos lidos sobre imagens aleatórias
- tradução direta de vídeo de outro canal
- vídeos sem arco narrativo
- títulos enganosos ou thumbnails que prometem o que o vídeo não entrega
- fatos, citações ou estatísticas inventadas
- conteúdo estruturalmente idêntico ao anterior (alterar só palavras não é diferente)

---

## Estrutura Narrativa

Variar formatos. Não usar sempre Hook/Problema/3 pontos/Conclusão. Alternativas:

investigação · história cronológica · mistério · comparação · estudo de caso ·
análise · transformação · descoberta · pergunta progressiva · documental ·
explicação visual · lista (só quando editorialmente justificada)

---

## Controle de Similaridade

Antes de publicar, comparar com:
- últimos 30 vídeos do canal
- vídeos produzidos no mesmo dia
- vídeos dos demais canais da produtora

Se parecer versão superficialmente modificada de outro → **bloquear publicação**.

---

## Upload

- Usar `videos.insert` com todos os campos na chamada inicial (snippet + status)
- `notifySubscribers = false` em lotes altos para não bombardear inscritos
- `containsSyntheticMedia = true` sempre que IA gerar narração/imagem
- Distribuir publicações ao longo do dia conforme timezone do mercado

---

## Classificação Semanal de Canais

| Classe | Critério | Ação |
|---|---|---|
| A | forte crescimento | aumentar investimento editorial |
| B | promissor | testar |
| C | teste | experimentar |
| D | baixo desempenho | reformular ou pausar |

---

## Compliance Log por Upload

Registrar por vídeo: `channel_id`, `video_id`, `date`, `language`, `original_concept`,
`script_hash`, `asset_sources`, `voice_source`, `synthetic_media_status`,
`made_for_kids_status`, `upload_endpoint`, `API_project`, `publication_status`, `quality_score`.

---

## Regra Final

**Maximize: QUALIDADE × ORIGINALIDADE × RETENÇÃO × ESCALA.**

A automação existe para produzir mais conteúdo original — nunca para produzir repetição mais rapidamente.
