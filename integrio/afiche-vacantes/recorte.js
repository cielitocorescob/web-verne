// Vuelve transparente el fondo plano (#fffaf7) de la foto del afiche original.
const { chromium } = require('playwright'); const fs = require('fs'), path = require('path');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  const src = 'data:image/jpeg;base64,' + fs.readFileSync(path.join(__dirname, 'fotos/afiche-original.jpg')).toString('base64');
  const out = await p.evaluate(async src => {
    const i = new Image(); i.src = src; await i.decode();
    const c = document.createElement('canvas'); c.width = i.width; c.height = i.height;
    const x = c.getContext('2d'); x.drawImage(i, 0, 0);
    const d = x.getImageData(0, 0, c.width, c.height), a = d.data;
    for (let k = 0; k < a.length; k += 4) {
      const dist = Math.abs(a[k] - 255) + Math.abs(a[k+1] - 250) + Math.abs(a[k+2] - 247);
      if (dist <= 4) a[k+3] = 0; else if (dist < 14) a[k+3] = Math.round(255 * (dist - 4) / 10);
    }
    x.putImageData(d, 0, 0); return c.toDataURL('image/png');
  }, src);
  fs.writeFileSync(path.join(__dirname, 'fotos/nino-recorte.png'), Buffer.from(out.split(',')[1], 'base64'));
  await b.close(); console.log('ok');
})();
