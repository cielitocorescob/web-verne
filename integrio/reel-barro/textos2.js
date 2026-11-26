// Renderiza cada texto como PNG transparente 720x1280 (blanco, centrado, sombra suave, degradado inferior).
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
const dir = process.argv[2];
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 720, height: 1280 } });
  const font = '../fonts-marca/AndesRounded-Black.otf';
  for (const f of fs.readdirSync(path.join(dir, 'textos2')).sort()) {
    const t = fs.readFileSync(path.join(dir, 'textos2', f), 'utf8').trim().replace(/\n/g, '<br>');
    if (!t) continue;
    fs.writeFileSync(path.join(dir, '_texto.html'), `<html><head><style>
      @font-face{font-family:A;src:url(${font})}
      html,body{margin:0;width:720px;height:1280px;background:transparent}
      .g{position:absolute;left:0;right:0;bottom:0;height:560px;background:linear-gradient(180deg,rgba(40,28,20,0) 0%,rgba(40,28,20,.38) 100%)}
      .t{position:absolute;left:30px;right:30px;bottom:250px;text-align:center;font-family:A;color:#fff;font-size:54px;line-height:1.12;
         text-shadow:0 2px 14px rgba(0,0,0,.35),0 1px 3px rgba(0,0,0,.3)}
    </style></head><body><div class="g"></div><div class="t">${t}</div></body></html>`);
    await p.goto('file://' + path.join(dir, '_texto.html'));
    await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(300);
    if (!(await p.evaluate(() => document.fonts.check('54px A')))) throw new Error('Andes Rounded no cargó');
    await p.screenshot({ path: path.join(dir, 'out/txt2', f.replace('.txt', '.png')), omitBackground: true });
  }
  fs.unlinkSync(path.join(dir, '_texto.html')); await b.close(); console.log('ok');
})();
