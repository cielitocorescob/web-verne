// Exporta el panel a PDF A3 y A1 horizontal, y PNG de vista previa.
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1587, height: 1123 }, deviceScaleFactor: 2 });
  await p.goto('file://' + path.join(__dirname, 'panel.html'));
  await p.evaluate(() => document.fonts.ready); await p.waitForTimeout(600);
  await p.pdf({ path: path.join(__dirname, 'integrio-panel-kusama-A3.pdf'), format: 'A3', landscape: true, printBackground: true, preferCSSPageSize: true });
  // A1 (841 x 594 mm): el diseño A3 escalado al doble, misma proporción
  await p.pdf({ path: path.join(__dirname, 'integrio-panel-kusama-A1.pdf'), width: '841mm', height: '594mm', scale: 2, printBackground: true });
  await p.screenshot({ path: path.join(__dirname, 'vista-previa.png') });
  await b.close(); console.log('ok');
})();
