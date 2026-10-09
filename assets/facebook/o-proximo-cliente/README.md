# Capa do Facebook — O Próximo Cliente

Arquivos:

- `capa-1640x624.png` — a imagem para subir no Facebook (tamanho recomendado, 2× de 820×312).
- `capa-preview-celular.png` — como fica no celular: o Facebook corta ~180 px de cada lado, então todo o texto está nos 1280 px centrais.
- `capa.html` — a fonte editável. Troque o texto ou as cores em `:root` e renderize de novo.
- `render.js` — gera os dois PNGs com o Chromium do Playwright.
- `fonts/` — Montserrat 500/700/900 (licença OFL), para o render sair igual em qualquer máquina.

Renderizar:

```bash
cd assets/facebook/o-proximo-cliente
NODE_PATH=$(npm root -g) node render.js
```

Requer o pacote `playwright` instalado (global ou local) e o Chromium dele.
