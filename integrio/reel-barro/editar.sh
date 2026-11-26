#!/bin/bash
# Arma el reel "Manos en la tierra" desde el video original.
# Uso: ./editar.sh ruta/al/video.mp4
set -e
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
  ffmpeg -nostdin -v error -y -ss $a -to $b -i "$V" -an -vf "setpts=2.6*PTS,minterpolate=fps=30:mi_mode=blend,scale=720:1280,\
drawtext=fontfile=$F:textfile=textos/t$i.txt:fontsize=50:fontcolor=0xc07a5a:line_spacing=8:\
box=1:boxcolor=0xfffcf8@0.94:boxborderw=26:x=(w-text_w)/2:y=h*0.74:\
alpha='if(lt(t,0.25),t/0.25,if(gt(t,$dur-0.25),($dur-t)/0.25,1))'" \
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
