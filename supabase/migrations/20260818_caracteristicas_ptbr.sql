-- 18/08/2026 — Vocabulário PT-BR das características do imóvel.
--
-- As características chegam do Vista já normalizadas para o código VRSync
-- ("Pool", "Maids Quarters"), e as que não têm equivalente VRSync chegam com
-- o rótulo do Vista maltratado: sem acento e com CamelCase quebrado
-- ("Energia Eletrica", "Portaria24 Hrs", "Sala T V"). Nenhum dos dois formatos
-- serve para ler dentro de uma descrição de anúncio.
--
-- Esta tabela é o dicionário. Só entra o que o Vista realmente manda — os 77
-- códigos em uso hoje, levantados por contagem no acervo ativo.

create table if not exists public.feed_caracteristica_ptbr (
  codigo text primary key,
  ptbr   text not null
);

insert into public.feed_caracteristica_ptbr (codigo, ptbr) values
  ('Maids Quarters','dependência de empregada'),
  ('Veranda','varanda'),
  ('BBQ','churrasqueira'),
  ('Cooling','ar-condicionado'),
  ('Fenced Yard','quintal fechado'),
  ('Backyard','quintal'),
  ('Party Room','salão de festas'),
  ('Playground','playground'),
  ('Pool','piscina'),
  ('Balcony','sacada'),
  ('Elevator','elevador'),
  ('Garden Area','área verde'),
  ('Sports Court','quadra poliesportiva'),
  ('Game room','salão de jogos'),
  ('Intercom','interfone'),
  ('Controlled Access','acesso controlado'),
  ('BarbecueBalcony','varanda gourmet com churrasqueira'),
  ('Gourmet Area','espaço gourmet'),
  ('Exterior View','vista livre'),
  ('Kitchen','cozinha'),
  ('Home Office','home office'),
  ('Tennis court','quadra de tênis'),
  ('Security Guard on Duty','segurança 24 horas'),
  ('Furnished','mobiliado'),
  ('Fireplace','lareira'),
  ('Sauna','sauna'),
  ('Laundry','lavanderia'),
  ('Ocean View','vista para o mar'),
  ('Heating','aquecimento'),
  ('Warehouse','depósito'),
  ('Spa','spa'),
  ('Generator','gerador'),
  ('Energia Eletrica','energia elétrica'),
  ('Pavimentacao','rua pavimentada'),
  ('Escritorio','escritório'),
  ('Agua','água encanada'),
  ('Espaco Gourmet','espaço gourmet'),
  ('Banheiro Social','banheiro social'),
  ('Rede Esgoto','rede de esgoto'),
  ('Aceita Pet','aceita pet'),
  ('Portaria24 Hrs','portaria 24 horas'),
  ('Possui Viabilidade','viabilidade construtiva'),
  ('Copa','copa'),
  ('Cozinha Planejada','cozinha planejada'),
  ('Sala De Recepcao','sala de recepção'),
  ('Lavabo','lavabo'),
  ('Forro','forro'),
  ('Cabine De Forca','cabine de força'),
  ('Dormitorio Com Armario','dormitório com armário'),
  ('Poco Artesiano','poço artesiano'),
  ('Sala T V','sala de TV'),
  ('Portaria','portaria'),
  ('Despensa','despensa'),
  ('Armario Embutido','armário embutido'),
  ('Sala Jantar','sala de jantar'),
  ('Estacionamento Visitantes','estacionamento para visitantes'),
  ('Cozinha Americana','cozinha americana'),
  ('Agua Quente','água quente'),
  ('Energia Trifasica','energia trifásica'),
  ('Canaletas No Rodape','canaletas no rodapé'),
  ('Monitoramento','monitoramento 24 horas'),
  ('Circuito Fechado T V','circuito fechado de TV'),
  ('Reformado','reformado'),
  ('Semi Mobiliado','semimobiliado'),
  ('Estacionamento','estacionamento'),
  ('Jardim Inverno','jardim de inverno'),
  ('Capacidade Piso','piso de alta capacidade de carga'),
  ('Piso Elevado','piso elevado'),
  ('Edicula','edícula'),
  ('Espera Split','ponto para ar-condicionado split'),
  ('Brinquedoteca','brinquedoteca'),
  ('Bicicletario','bicicletário'),
  ('Cerca Eletrica','cerca elétrica'),
  ('Vitrine','vitrine'),
  ('Sala Armarios','sala com armários'),
  ('Copa Cozinha','copa e cozinha')
on conflict (codigo) do update set ptbr = excluded.ptbr;

-- 'Tour360' fica DE FORA de propósito: é metadado de mídia, não característica
-- do imóvel. Anunciar "tour 360" como diferencial de um imóvel cujo link de
-- tour não está publicado seria promessa que a página não cumpre.

alter table public.feed_caracteristica_ptbr enable row level security;
create policy leitura_publica on public.feed_caracteristica_ptbr for select to authenticated using (true);
