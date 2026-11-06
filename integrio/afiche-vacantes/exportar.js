// Exporta el afiche a PDF A4 para impresión y a PNG de vista previa.
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 794, height: 1123 }, deviceScaleFactor: 2 });
  await p.goto('file://' + path.join(__dirname, 'afiche.html'));
  await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(500);
  await p.pdf({ path: path.join(__dirname, 'integrio-vacantes-2027-A4.pdf'), format: 'A4', printBackground: true, preferCSSPageSize: true });
  await p.screenshot({ path: path.join(__dirname, 'vista-previa.png'), fullPage: false });
  await b.close(); console.log('ok');
})();
