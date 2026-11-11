// Exporta cada pieza (section.pieza) a PNG con su propio tamaño.
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1200, height: 2000 } });
  await p.goto('file://' + path.join(__dirname, 'comunicado.html'));
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(500);
  for (const el of await p.$$('section.pieza')) {
    const id = await el.getAttribute('id');
    await el.screenshot({ path: path.join(__dirname, 'png', `integrio-${id}.png`) });
  }
  await b.close();
  console.log('ok');
})();
