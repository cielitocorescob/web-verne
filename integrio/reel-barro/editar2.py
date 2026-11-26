#!/usr/bin/env python3
# Reel "Manos en la tierra" v2: ritmo ágil, mezcla de video y fotos con zoom lento.
# Uso: python3 editar2.py VIDEO_ORIGINAL.mp4 VIDEO_NUEVO.mov
import subprocess, sys, os
V1, V2 = sys.argv[1], sys.argv[2]
O = 'out'; os.makedirs(f'{O}/v2', exist_ok=True); os.makedirs('textos2', exist_ok=True)
# (tipo, fuente, inicio, fin|duración, velocidad|desplazamiento x, texto)
SEG = [
 ('vid', V1, 4.28, 5.22, 1.8, '¿Cómo se siente?'),
 ('img', 'fotos/sonrisa.jpg', 0, 1.8, 240, ''),
 ('vid', V2, 3.30, 4.95, 1.3, '¿Qué pasa si\nle pongo agua?'),
 ('img', 'fotos/vierte.jpg', 0, 1.8, 200, ''),
 ('vid', V1, 14.51, 15.62, 1.8, '¿Cabe más?'),
 ('img', 'fotos/frasco.jpg', 0, 2.0, 380, 'Probando sus\npropias teorías.'),
 ('img', 'fotos/barro-dos.jpg', 0, 2.0, 160, 'Se hace barro…'),
 ('img', 'fotos/grupo.jpg', 0, 2.6, 240, 'Tierra, agua y tiempo\npara explorar sin apuro.'),
 ('img', 'fotos/mirada.jpg', 0, 2.0, 120, 'Así se ve\nun aprendizaje.'),
]
def run(a): subprocess.run(['ffmpeg','-nostdin','-v','error','-y']+a, check=True)
# textos a PNG
for i,s in enumerate(SEG):
    open(f'textos2/t{i}.txt','w').write(s[5])
lista=[]
for i,(tipo,src,a,b,p,txt) in enumerate(SEG):
    out=f'{O}/v2/s{i}.mp4'
    if tipo=='vid':
        dur=(b-a)*p
        base=f"setpts={p}*PTS,minterpolate=fps=30:mi_mode=blend,scale=720:1280:force_original_aspect_ratio=increase,crop=720:1280"
        inp=['-ss',str(a),'-to',str(b),'-i',src]
    else:
        dur=b; n=int(dur*30)
        base=(f"scale=1920:2560,crop=1440:2560:{p}:0,"
              f"zoompan=z='1+0.07*on/{n}':d={n}:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=720x1280:fps=30")
        inp=['-i',src]
    if txt:
        fo=dur-0.35
        fc=(f"[0:v]{base},setsar=1[v];[1:v]format=rgba,fade=in:st=0.05:d=0.3:alpha=1,"
            f"fade=out:st={fo:.2f}:d=0.3:alpha=1[t];[v][t]overlay=0:0:shortest=1")
        run(inp+['-loop','1','-i',f'{O}/txt2/t{i}.png','-an','-filter_complex',fc,
                 '-t',f'{dur:.3f}','-c:v','libx264','-pix_fmt','yuv420p','-r','30','-crf','18',out])
    else:
        run(inp+['-an','-vf',base+',setsar=1','-t',f'{dur:.3f}','-c:v','libx264','-pix_fmt','yuv420p','-r','30','-crf','18',out])
    lista.append(f"file 's{i}.mp4'")
open(f'{O}/v2/lista.txt','w').write('\n'.join(lista)+'\n')
run(['-f','concat','-safe','0','-i',f'{O}/v2/lista.txt','-c','copy',f'{O}/v2/tomas.mp4'])
D=float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f'{O}/v2/tomas.mp4']))
run(['-i',f'{O}/v2/tomas.mp4','-i',f'{O}/cierre.mp4','-filter_complex',
     f'[0][1]xfade=transition=fade:duration=0.4:offset={D-0.4:.3f},format=yuv420p',
     '-c:v','libx264','-crf','18','-movflags','+faststart',f'{O}/integrio-reel-manos-en-la-tierra-v2.mp4'])
print(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f'{O}/integrio-reel-manos-en-la-tierra-v2.mp4']).decode().strip())
