// Exporta cada slide del carrusel como PNG 1080x1350.
// Uso: node render.js   (requiere playwright)
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1200, height: 1400 } });
  await page.goto('file://' + path.join(__dirname, 'carrusel.html'));
  await page.evaluate(() => document.fonts.ready);
  const slides = await page.$$('section.slide');
  for (let i = 0; i < slides.length; i++) {
    await slides[i].screenshot({ path: path.join(__dirname, 'png', `integrio-juego-${String(i + 1).padStart(2, '0')}.png`) });
  }
  await browser.close();
  console.log(`${slides.length} slides exportadas`);
})();
