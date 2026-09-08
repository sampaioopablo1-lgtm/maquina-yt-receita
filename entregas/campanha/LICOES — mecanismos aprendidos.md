# Lições de mecanismo — como as ferramentas realmente se comportam
*Memória da máquina. Cada linha custou tempo ou lead para descobrir. Ler antes de mexer em qualquer coisa; acrescentar sempre que um comportamento surpreender.*

## Prospect Halo
| Mecanismo | Consequência prática | Descoberto |
|---|---|---|
| Regra **obrigatória** (`additionalCriteria`) que o LinkedIn não consegue provar → o prospect é **adiado**, nunca contatado | Exclusão negativa ("não é agência") como obrigatória mata volume em silêncio. Usar como **preferida**. | 08/09 |
| Muitos filtros somados (títulos × setores × locais × exclusões) → o LinkedIn descarta em silêncio o que não reconhece e busca em todo lugar | Alvo enxuto rende mais: 6 títulos e 5 setores levaram a revisão de 1 para 10 perfis por passada | 08/09 |
| A API **não edita alvo** de agente existente (`update_agent` com titles/industries/locations retorna erro) | Mudar alvo = apagar e recriar. Definir bem antes de acumular leads. | 08/09 |
| Não existe importação de lista: leads só nascem da descoberta no LinkedIn | Cadência por lista de CNPJ roda fora da ferramenta | 08/09 |
| **Existe uma cota diária protegida de "verificação de perfil" (hydration), separada de convites e de créditos de prospect.** Quando ela acaba: `progressStatus: waiting_for_profile_capacity`, `waitingReason: LinkedIn profile verification capacity is currently exhausted`, e `nextRetryAt` diz a hora do reset | É o gargalo invisível nº 1. A busca acha os candidatos, mas eles ficam parados em `remainingCandidates` sem serem processados. Nada aparece como erro nem como pausa de segurança. **Sempre ler `progressStatus` e `waitingReason` antes de culpar a segmentação.** | 08/09 |
| Recriar agente reprocessa perfis e **queima a cota de verificação do dia** | Cada recriação custa capacidade real, não só a fila. Máximo uma recriação por dia. | 08/09 |
| `find_leads` não devolve e-mail; enriquecimento gasta 1 de 50 créditos/mês | E-mail é complemento para lead quente, nunca volume | 08/09 |
| Página de empresa publica conteúdo, mas não prospecta nem manda mensagem | Prospecção sempre pelo perfil pessoal | 08/09 |
| Autopilot de conteúdo gera o post ~20h antes de publicar | Dá para revisar e corrigir na véspera | 08/09 |
| Só conversas que já receberam resposta aceitam `reply_to_lead` | Não dá para puxar conversa parada pela API | 08/09 |

## Meta Ads
| Mecanismo | Consequência prática | Descoberto |
|---|---|---|
| `ads_update_entity` força `status=PAUSED` em campanha e conjunto | Sempre chamar `ads_activate_entity` depois de qualquer edição | 07/09 |
| Vários públicos personalizados num conjunto = **união**, sem relatório por lista | Impossível saber de qual lista veio o lead. Separar exige orçamento por conjunto. | 08/09 |
| Lista nacional + geo estadual = interseção pequena | CPM dispara (R$78) e o orçamento não gasta | 08/09 |
| Editar segmentação reinicia a fase de aprendizado | Não mexer em conjunto que acabou de destravar | 08/09 |
| `instagram_user_id` é rejeitado no `object_story_spec` | Omitir o campo | 07/09 |
| Criação de anúncio de formulário falha pela API (falta permissão de ler os termos) | Anúncio de lead se cria no Gerenciador | 07/09 |

## Google
| Mecanismo | Consequência prática | Descoberto |
|---|---|---|
| Perfil do LinkedIn não tem escrita por API (só leitura) | Título e "Sobre" são copiar e colar | 08/09 |
| Bloco de rotina marcado como "ocupado" some da busca de horário livre | Marcar como "disponível" o bloco em que se aceita reunião | 08/09 |
| `GOOGLEDRIVE_LIST_FILES` ignora `query`; usa `folderId` | Listar sempre por pasta | 07/09 |
| HTML enviado com mime `application/vnd.google-apps.document` vira Google Doc | Caminho para documento legível no celular | 07/09 |

## Regras de conduta que saíram dessas lições
1. Quando um número não tem explicação, procurar o **mecanismo**, não o botão. O que some em silêncio (adiado, descartado, não entregue) importa mais que o que aparece no relatório.
2. Achou um defeito num lugar, procurar o mesmo defeito em **todos os lugares análogos** antes de encerrar.
3. Antes de mexer em algo que acabou de melhorar, calcular o que se perde reiniciando o aprendizado.
4. Registrar o mecanismo aqui na hora. Redescobrir custa dias.
