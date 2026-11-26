#!/bin/bash
# Arma el reel "Manos en la tierra" desde el video original.
# Uso: ./editar.sh ruta/al/video.mp4
set -e
# Textos: se renderizan antes con "node textos.js $PWD" (PNG transparentes en out/txt)
V="$1"; F=../fonts-marca/AndesRounded-Black.otf; O=out
mkdir -p $O textos
# toma: inicio fin texto
cat > tomas.txt <<'T'
4.28|5.22|¿Cómo se siente?
10.48|11.45|¿Qué pasa si
le pongo agua?
14.51|15.62|¿Cabe más?
18.40|19.03|Se hace barro…
11.54|12.49|Probando sus
propias teorías.
20.80|21.70|Tierra, agua y tiempo
para explorar sin apuro.
21.76|22.46|Así se ve
un aprendizaje.
T
python3 - <<'P'
import re
raw=open('tomas.txt').read()
items=re.findall(r'^([\d.]+)\|([\d.]+)\|(.*?)(?=^\d|\Z)', raw, re.S|re.M)
with open('tomas.list','w') as f:
    for i,(a,b,t) in enumerate(items):
        open(f'textos/t{i}.txt','w').write(t.strip())
        f.write(f'{i} {a} {b}\n')
P
: > $O/lista.txt
while read i a b; do
  dur=$(python3 -c "print(($b-$a)*2.6)")
  ffmpeg -nostdin -v error -y -ss $a -to $b -i "$V" -loop 1 -i $O/txt/t$i.png -an -filter_complex \
"[0:v]setpts=2.6*PTS,minterpolate=fps=30:mi_mode=blend,scale=720:1280[v];\
[1:v]format=rgba,fade=in:st=0.1:d=0.4:alpha=1,fade=out:st=$(python3 -c "print($dur-0.45)"):d=0.35:alpha=1[t];\
[v][t]overlay=0:0:shortest=1" \
    -c:v libx264 -pix_fmt yuv420p -r 30 -crf 18 $O/s$i.mp4
  echo "file 's$i.mp4'" >> $O/lista.txt
done < tomas.list
ffmpeg -nostdin -v error -y -f concat -safe 0 -i $O/lista.txt -c copy $O/tomas.mp4
ffmpeg -nostdin -v error -y -loop 1 -t 3.5 -i $O/cierre.png -vf "fps=30,format=yuv420p" -c:v libx264 -crf 18 $O/cierre.mp4
D=$(ffprobe -v error -show_entries format=duration -of csv=p=0 $O/tomas.mp4)
ffmpeg -nostdin -v error -y -i $O/tomas.mp4 -i $O/cierre.mp4 -filter_complex \
 "[0][1]xfade=transition=fade:duration=0.5:offset=$(python3 -c "print($D-0.5)"),format=yuv420p" \
 -c:v libx264 -crf 18 -movflags +faststart $O/integrio-reel-manos-en-la-tierra.mp4
ffprobe -v error -show_entries format=duration -of csv=p=0 $O/integrio-reel-manos-en-la-tierra.mp4
