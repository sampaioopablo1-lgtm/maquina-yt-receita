# Integração XML — portal Chaves na Mão

Documento de entrega: o que informar ao portal para ligar a integração, e o que
o arquivo contém. O equivalente do que já existe com o Grupo Zap (VivaReal/OLX),
só que naquele caso o padrão é VRSync e aqui é o padrão próprio do Chaves na Mão.

## O que informar ao portal

| Item | Valor |
|---|---|
| Imobiliária | Jazz Imobiliária — São José dos Campos/SP |
| Contato técnico | rafael@imobiliariajazz.com.br |
| URL do XML | `https://cscczluzpblzhvojxanp.supabase.co/storage/v1/object/public/feeds-portais/chavesnamao.xml` |
| Padrão | Chaves na Mão, versão 0.0.4 da documentação oficial |
| Encoding | UTF-8 |
| Disponibilidade | público, sem autenticação, 24/7 |
| Atualização do arquivo | 2x/dia (03:40 e 15:40, horário de Brasília) |
| Leitura sugerida | 1x/dia, como o portal já opera |

O arquivo é dinâmico: é regerado a partir do acervo do Vista CRM, então imóvel
vendido, desativado ou com dado alterado aparece na carga seguinte sem
intervenção manual.

## Conformidade com a documentação do portal

Conferido contra o XML de exemplo publicado pelo portal — **53 tags por imóvel,
mesma ordem, mesma grafia**, todas presentes mesmo quando vazias, como a
documentação exige.

| Regra do portal | Como o feed atende |
|---|---|
| Raiz `<Document>` → `<imoveis>` → `<imovel>` | idem |
| Todas as tags presentes, mesmo vazias | bloco montado inteiro, com string vazia onde não há dado |
| Tags case sensitive | grafia copiada da documentação |
| Fotos: JPG, JPEG, WEBP | PNG é descartado na origem |
| Máximo de 30 fotos por imóvel | corte antes da emissão |
| Extensão da imagem na própria URL | as URLs do Vista já trazem extensão; quem não traz é descartado |
| `descritivo` até 3.000 caracteres | truncado com corte em fim de frase |
| Tipos exatamente como nas listas Residencial/Comercial | tabela fixa no gerador |
| `estado` com sigla oficial da UF | normalizado (aceita "São Paulo" ou "SP") |
| `transacao` V/L e `finalidade` RE/CO | derivados da finalidade do Vista |
| `valor` = venda quando há as duas transações | idem; locação pura usa `valor` + `periodo_locacao=1` |
| `data_atualizacao` em `AAAA-MM-DD HH:MM:SS` | data real da última atualização da ficha |
| Vídeo: link de YouTube, sem embed | Shorts, `/embed/` e Vimeo ficam de fora |

## O que vai preenchido

Referência (código do Vista), título, transação e finalidade, tipo, valores
(venda, locação, IPTU, condomínio), áreas total e útil, quartos, suítes,
banheiros, garagem, endereço (UF, cidade, bairro, CEP, logradouro, número),
descritivo, fotos com data, coordenadas quando existem, vídeo e tour 360
quando existem, itens de área comum e privativa, e `aceita_pet`.

Três observações de conteúdo, ditas abertamente:

1. **Número da rua é preservado** — o feed publica um número estável por imóvel
   que não é o número real do cadastro, prática já adotada no feed do Grupo
   Zap. Logradouro, bairro, CEP e coordenadas são reais.
2. **Cômodos que o portal numera e o Vista não** (closet, varanda, lareira,
   escritório, despensa, bar, área de serviço, dependência de empregada) saem
   como `1` quando a característica existe na ficha. Nunca um número maior sem
   respaldo no cadastro.
3. **Tour 360 é raro no acervo** — só é emitido quando há tour real; link de
   vídeo não é publicado como tour.

## Exemplo de um imóvel no arquivo

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Document>
  <imoveis>
    <imovel>
      <referencia>46824</referencia>
      <codigo_cliente>46824</codigo_cliente>
      <link_cliente></link_cliente>
      <titulo>Apartamento à venda e para alugar no Jardim Aquarius</titulo>
      <transacao>V</transacao>
      <transacao2>L</transacao2>
      <finalidade>RE</finalidade>
      <finalidade2></finalidade2>
      <destaque>0</destaque>
      <tipo>Apartamento</tipo>
      <tipo2></tipo2>
      <valor>350000</valor>
      <valor_locacao>2200</valor_locacao>
      <valor_iptu>201</valor_iptu>
      <valor_condominio>560</valor_condominio>
      <area_total>90</area_total>
      <area_util>72</area_util>
      <conservacao></conservacao>
      <quartos>2</quartos>
      <suites>1</suites>
      <garagem>1</garagem>
      <banheiro>2</banheiro>
      <closet>1</closet>
      <salas></salas>
      <despensa></despensa>
      <bar></bar>
      <cozinha></cozinha>
      <quarto_empregada></quarto_empregada>
      <escritorio></escritorio>
      <area_servico></area_servico>
      <lareira></lareira>
      <varanda>1</varanda>
      <lavanderia></lavanderia>
      <aceita_pet>1</aceita_pet>
      <estado>SP</estado>
      <cidade>São José dos Campos</cidade>
      <bairro>Jardim Aquarius</bairro>
      <cep>12246000</cep>
      <endereco>Avenida Cassiano Ricardo</endereco>
      <numero>211</numero>
      <complemento></complemento>
      <esconder_endereco_imovel>0</esconder_endereco_imovel>
      <descritivo><![CDATA[Apartamento à venda e para alugar no bairro Jardim Aquarius, São José dos Campos.

Especificações do imóvel:
- Área útil de 72 metros quadrados
- Área total de 90 metros quadrados
- 2 quartos, sendo 1 suíte
- 2 banheiros
- 1 vaga de garagem
- Construção de 2012]]></descritivo>
      <fotos_imovel>
        <foto>
          <url>https://.../46824-01.jpg</url>
          <data_atualizacao>2026-09-17 13:45:09</data_atualizacao>
        </foto>
      </fotos_imovel>
      <data_atualizacao>2026-09-17 13:45:09</data_atualizacao>
      <latitude>-23.2076</latitude>
      <longitude>-45.8985</longitude>
      <video></video>
      <tour_360></tour_360>
      <area_comum>
        <item>Piscina</item>
        <item>Churrasqueira</item>
        <item>Elevador</item>
      </area_comum>
      <area_privativa>
        <item>Varanda</item>
        <item>Closet</item>
      </area_privativa>
      <aceita_troca></aceita_troca>
      <periodo_locacao>1</periodo_locacao>
    </imovel>
  </imoveis>
</Document>
```

## Antes de enviar a URL ao portal

Nesta sessão não houve acesso ao Supabase da Jazz, então estes três passos
ficam para quem tem a credencial:

1. Aplicar a migração `20260918_feed_chavesnamao.sql` (cria o bucket público
   `feeds-portais` e agenda `feed-precomputar-chavesnamao`).
2. Publicar a Edge Function `chavesnamao-feed` e rodar
   `{"acao":"prever"}` — devolve quantos imóveis entram, o tamanho do arquivo e
   uma amostra, **sem** publicar nada.
3. Com o número conferido, rodar `{"acao":"precomputar"}`, abrir a URL pública
   e só então informá-la ao portal.

Detalhes técnicos, variáveis de ambiente e decisões do gerador estão em
`jazz/supabase/functions/chavesnamao-feed/README.md`.
