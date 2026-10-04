// Gera config/muapi_modelos.json a partir do models.js do Open Higgsfield AI.
//
// O models.js (packages/studio/src) e a fonte unica dos 200+ modelos da Muapi
// que o app expoe; o JSON e a versao que o Python le (src/maquina/providers/
// muapi.py e fabrica/muapi.py) sem precisar de Node. Rode depois de atualizar
// o app vendido em ferramentas/open-higgsfield-ai:
//
//   node scripts/catalogo_muapi.mjs
import { readFileSync, writeFileSync } from 'node:fs';
import { execSync } from 'node:child_process';

const RAIZ = new URL('..', import.meta.url).pathname;
const ORIGEM = 'ferramentas/open-higgsfield-ai/packages/studio/src/models.js';
const DESTINO = 'config/muapi_modelos.json';

let commit = 'desconhecido';
try {
  commit = execSync('git log -1 --format=%h -- ' + ORIGEM, { cwd: RAIZ }).toString().trim() || commit;
} catch {}

const src = readFileSync(RAIZ + ORIGEM, 'utf8').replace(/export /g, '');
const m = {};
// O arquivo e uma lista de `const xModels = [...]` + helpers puros: avaliar e
// o jeito mais barato de le-lo sem um bundler.
eval(src + ';Object.assign(m,{t2iModels,i2iModels,t2vModels,i2vModels,v2vModels,lipsyncModels});');

const out = {
  gerado_de: `${ORIGEM} (commit ${commit})`,
  base_url: 'https://api.muapi.ai',
  modelos: [],
};
const grupos = { t2i: m.t2iModels, i2i: m.i2iModels, t2v: m.t2vModels,
                 i2v: m.i2vModels, v2v: m.v2vModels, lipsync: m.lipsyncModels };
for (const [categoria, lista] of Object.entries(grupos)) {
  for (const x of lista) {
    const inp = x.inputs || {};
    const e = { id: x.id, nome: x.name, categoria, endpoint: x.endpoint || x.id,
                campos: Object.keys(inp) };
    for (const f of ['aspect_ratio', 'resolution', 'duration', 'quality', 'mode']) {
      if (inp[f] && inp[f].enum) e[f] = inp[f].enum;
    }
    if (x.imageField) e.imageField = x.imageField;
    if (x.videoField) e.videoField = x.videoField;
    if (x.maxImages) e.maxImages = x.maxImages;
    if (x.category) e.modo = x.category;
    out.modelos.push(e);
  }
}
writeFileSync(RAIZ + DESTINO, JSON.stringify(out, null, 1) + '\n');
console.log(`${out.modelos.length} modelos -> ${DESTINO}`);
