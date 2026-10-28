const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:400}});
for(const s of process.argv.slice(2)){await p.goto('file://'+process.cwd()+'/'+s+'.html');await p.addStyleTag({content:'body{height:auto!important}'});await p.screenshot({path:'remuneracao-'+s+'.png',fullPage:true});}
await b.close();})()
