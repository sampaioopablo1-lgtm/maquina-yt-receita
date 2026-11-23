// uso: node render.js timeline.json saida_video_mudo.mp4 [so_quadro_t]
const fs=require('fs'), path=require('path'), {spawn}=require('child_process');
const {chromium}=require('playwright');
(async()=>{
  const [tl, out, so]=process.argv.slice(2);
  const T=JSON.parse(fs.readFileSync(tl,'utf8'));
  const fontes=path.join(process.env.FONTES_DIR);
  let html=fs.readFileSync(path.join(__dirname,'cena.html'),'utf8')
    .replace('FONT900','file://'+path.join(fontes,'montserrat-latin-900-normal.woff2'))
    .replace('FONT800','file://'+path.join(fontes,'montserrat-latin-800-normal.woff2'))
    .replace('TIMELINE',JSON.stringify(T));
  const tmp=path.join(path.dirname(path.resolve(out)),'_cena.html'); fs.writeFileSync(tmp,html);
  const b=await chromium.launch(); const pg=await b.newPage({viewport:{width:1080,height:1920}});
  await pg.goto('file://'+tmp); await pg.evaluate(()=>document.fonts.ready);
  if(so!==undefined){ await pg.evaluate(t=>render(t),parseFloat(so)); await pg.screenshot({path:out}); await b.close(); return; }
  const fps=30, n=Math.ceil(T.total*fps);
  const ff=spawn('ffmpeg',['-y','-v','error','-f','image2pipe','-framerate',String(fps),'-i','-',
    '-c:v','libx264','-preset','medium','-crf','20','-pix_fmt','yuv420p',out],{stdio:['pipe','inherit','inherit']});
  for(let f=0;f<n;f++){
    await pg.evaluate(t=>render(t),f/fps);
    const buf=await pg.screenshot({type:'jpeg',quality:92});
    if(!ff.stdin.write(buf)) await new Promise(r=>ff.stdin.once('drain',r));
    if(f%150===0) console.log(`quadro ${f}/${n}`);
  }
  ff.stdin.end(); await new Promise(r=>ff.on('close',r)); await b.close();
})();
