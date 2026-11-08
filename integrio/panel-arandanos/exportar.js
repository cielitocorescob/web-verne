// Exporta el panel a PDF A3 horizontal y PNG de vista previa.
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1587, height: 1123 }, deviceScaleFactor: 2 });
  await p.goto('file://' + path.join(__dirname, 'panel.html'));
  await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(600);
  await p.pdf({ path: path.join(__dirname, 'integrio-panel-arandanos-A3.pdf'), format: 'A3', landscape: true, printBackground: true, preferCSSPageSize: true });
  await p.screenshot({ path: path.join(__dirname, 'vista-previa.png') });
  await b.close(); console.log('ok');
})();
