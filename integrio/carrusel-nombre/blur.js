// Difumina los carteles con nombres de los niños antes de diseñar.
// Regiones en píxeles de la foto original: [x, y, ancho, alto]
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
const R = {
  '04': [[1130,1540,200,320]],
  '05': [[1040,450,250,320]],
  '07': [[540,1090,270,230]],
  '09': [[580,1120,260,260],[-120,1540,400,420],[1200,740,150,200]],
  '11': [[-120,990,480,380],[400,880,320,260]],
  '12': [[290,1040,290,290],[545,945,90,90]],
};
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  for (const f of fs.readdirSync(path.join(__dirname,'fotos-original'))) {
    const id = f.slice(0,2), src = 'data:image/jpeg;base64,' + fs.readFileSync(path.join(__dirname,'fotos-original',f)).toString('base64');
    const out = await p.evaluate(async ([src, regs]) => {
      const img = new Image(); img.src = src; await img.decode();
      const c = document.createElement('canvas'); c.width = img.naturalWidth; c.height = img.naturalHeight;
      const x = c.getContext('2d'); x.drawImage(img, 0, 0);
      const bl = document.createElement('canvas'); bl.width = c.width; bl.height = c.height;
      const bx = bl.getContext('2d'); bx.filter = 'blur(9px)'; bx.drawImage(img, -70, -70, c.width + 140, c.height + 140);
      const m = document.createElement('canvas'); m.width = c.width; m.height = c.height;
      const mx = m.getContext('2d'); mx.filter = 'blur(16px)'; mx.fillStyle = '#000';
      for (const [rx, ry, rw, rh] of regs) { mx.beginPath(); mx.roundRect(rx - 15, ry - 15, rw + 30, rh + 30, 50); mx.fill(); }
      bx.filter = 'none'; bx.globalCompositeOperation = 'destination-in'; bx.drawImage(m, 0, 0);
      if (regs.length) x.drawImage(bl, 0, 0);
      return c.toDataURL('image/jpeg', .92);
    }, [src, R[id] || []]);
    fs.writeFileSync(path.join(__dirname,'fotos',f), Buffer.from(out.split(',')[1], 'base64'));
  }
  await b.close(); console.log('ok');
})();
