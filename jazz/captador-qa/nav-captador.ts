/**
 * Menu único do módulo do captador.
 *
 * Antes desta correção, cada uma das seis telas do captador montava o array
 * `nav` do AppShell à mão, com um conjunto diferente de itens. Medido na
 * produção (Worker jazz-lead-conecta.pablo-jazzimob.workers.dev) em 20/08/2026:
 *
 *   /captador               Tarefas, Gestão, Recortes, Minhas Captações,
 *                           Minhas Metas, Imóveis, Chaves, Plantões,
 *                           [Admin], Ajuda
 *   /captador/gestao        Tarefas, Gestão, Recortes, Minhas Metas
 *   /captador/metas         Tarefas, Gestão, Metas, Operacional, Modo TV
 *   /captador/recortes      Painel, Gestão, Recortes, Externas
 *   /captador/prospeccoes   Painel, Gestão, Recortes, Externas
 *   /captador/minhas-captacoes
 *                           Painel, Gestão, Recortes, Minhas Captações, Externas
 *
 * Efeitos no uso: ao sair do painel para a Gestão o captador perde Imóveis,
 * Chaves, Plantões, Minhas Captações e Ajuda, e o admin perde o item Admin;
 * "Externas" (/captador/prospeccoes) não aparecia no painel principal, então
 * só dava para chegar lá vindo de Recortes ou de Minhas Captações; e
 * /captador se chamava "Tarefas" em três telas e "Painel" nas outras três.
 *
 * "Operacional" (/dashboard) e "Modo TV" (/tv) ficam FORA — foram tirados do
 * painel em 23/07 por serem menu duplicado, e a tela de metas era a única que
 * ainda os exibia. As telas seguem acessíveis por URL e pelo Admin.
 */
export type ItemNav = { to: string; label: string };

export function navCaptador({ isAdmin }: { isAdmin: boolean }): ItemNav[] {
  return [
    { to: "/captador", label: "Tarefas" },
    { to: "/captador/gestao", label: "📋 Gestão" },
    { to: "/captador/recortes", label: "🔔 Recortes" },
    { to: "/captador/prospeccoes", label: "🌐 Externas" },
    { to: "/captador/minhas-captacoes", label: "📋 Minhas Captações" },
    { to: "/captador/metas", label: "Minhas Metas" },
    { to: "/imoveis", label: "🏘️ Imóveis" },
    { to: "/chaves", label: "🔑 Chaves" },
    { to: "/plantoes", label: "🗓️ Plantões" },
    ...(isAdmin ? [{ to: "/admin", label: "⚙️ Admin" }] : []),
    { to: "/ajuda", label: "Ajuda" },
  ];
}

/**
 * Qual item do menu deve aparecer como ativo para um dado pathname.
 *
 * O AppShell marcava ativo com
 *   loc.pathname === n.to || loc.pathname.startsWith(n.to + "/")
 * e, como "/captador" é prefixo de "/captador/gestao", em TODA subtela do
 * captador dois itens acendiam ao mesmo tempo ("Tarefas" e "Gestão", etc.).
 *
 * Aqui vence o item mais específico: entre os que casam, o de `to` mais longo.
 * Devolve o índice do item ativo, ou -1 quando nenhum casa.
 */
export function indiceItemAtivo(itens: ItemNav[], pathname: string): number {
  let melhor = -1;
  let melhorTamanho = -1;
  itens.forEach((item, i) => {
    const casa = pathname === item.to || pathname.startsWith(item.to + "/");
    if (casa && item.to.length > melhorTamanho) {
      melhor = i;
      melhorTamanho = item.to.length;
    }
  });
  return melhor;
}

/** Data de hoje no fuso do NAVEGADOR, no formato yyyy-mm-dd (input type=date).
 *
 * Substitui `new Date().toISOString().slice(0, 10)`, que é UTC: no horário de
 * Brasília (UTC−3), entre 21h e 23h59 ele já devolve o dia seguinte. O
 * formulário de lançamento de metas sugeria amanhã, e as ligações da noite
 * entravam na data errada. Mesmo problema no nome do CSV da Gestão e na
 * janela do mês da tela de metas.
 */
export function hojeLocalISO(agora: Date = new Date()): string {
  return agora.toLocaleDateString("en-CA"); // en-CA já formata como yyyy-mm-dd
}
