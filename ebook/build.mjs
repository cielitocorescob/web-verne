// Genera ebook/index.html (documento independiente) a partir del fragmento publicado como Artifact.
import { readFileSync, writeFileSync } from 'node:fs';
const here = new URL('.', import.meta.url);
const body = readFileSync(new URL('marca-directiva.html', here), 'utf8');
const html = `<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<style>:root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>
</head>
<body>
${body}
</body>
</html>
`;
writeFileSync(new URL('index.html', here), html);
console.log('ebook/index.html generado');
