# Compartamos Impulsa · Resultados 2026

Infografía 4:5 (1080×1350, exportada a 2x = 2160×2700) con la marca Compartamos.

- `infografia.html` — fuente editable (texto, colores en `:root`, íconos SVG inline).
- `infografia-1080x1350.png` — render final.
- Re-render: `node render.js infografia.html infografia-1080x1350.png 1080 1350 2`

Notas:
- Tipografías sustitutas (Baloo 2 + Asap) en lugar de Bree, la tipografía comercial de la marca. Para usar Bree, cambia `font-family` en el CSS.
- El logo se recortó de la pieza de referencia; conviene reemplazarlo por el PNG oficial.

## v2 (`infografia-v2.html` → `infografia-v2-1080x1350.png`)
Composición editorial en vez de cuadrícula: titular grande, cifras héroe (totales calculados: 3,576 + 3,407 + 600 + 457 = 8,040 personas; 700 mil + 475 mil = +1.17 millones de visualizaciones; validar con el cliente), barras proporcionales para los programas presenciales y panel oscuro para los digitales. Una sola familia tipográfica: toma Bree si está disponible y, si no, Baloo 2.
Re-render: `node render.js infografia-v2.html infografia-v2-1080x1350.png 1080 1350 2`
