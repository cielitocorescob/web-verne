import re, sys
S=sys.argv[1]; E='/home/user/web-verne/ebook'
old=open(E+'/respaldos/marca-directiva-web-antes-contenido-completo.html',encoding='utf8').read()
main_eb=open(E+'/marca-directiva.html',encoding='utf8').read()
head=old[:old.index('<style>')]
head=head.replace('<title>Marca Directiva · Verne</title>','<title>Marca Directiva · Verne</title>\n<meta name="color-scheme" content="light dark">\n<script>(function(){var t;try{t=localStorage.getItem("verne-ebook-tema")}catch(e){}if(t!=="light"&&t!=="dark"){t=window.matchMedia&&matchMedia("(prefers-color-scheme: dark)").matches?"dark":"light"}document.documentElement.setAttribute("data-theme",t)})();</script>')+'<style>'
css_old=open(S+'/base.css').read()
css=css_old+open(S+'/new.css').read()+open(S+'/theme.css').read()+open(S+'/audit.css').read()+open(S+'/print.css').read()+'</style>\n\n'
body=open(S+'/body.html').read()
MOD='<span class="mod" aria-hidden="true"><i></i><i></i></span>'
BTNI='<svg class="btn-i" viewBox="0 0 26 14" aria-hidden="true"><circle class="d" cx="5" cy="7" r="3"/><rect class="c" x="11" y="4" width="12" height="6" rx="3"/><path class="h" d="M16.5 2.5 L21.5 7 L16.5 11.5"/></svg>'
body=body.replace('{{BTNIPLAIN}}','<svg class="btn-i" viewBox="0 0 26 14" aria-hidden="true" style="width:30px"><path d="M2 7 H22 M16.5 2.5 L21.5 7 L16.5 11.5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>')
body=body.replace('{{MOD}}',MOD).replace('{{BTNI}}',BTNI)
body=body.replace('{{CTAMODS}}','<div class="cta__mods" aria-hidden="true"><span><i style="width:18px"></i><i style="width:90px"></i></span><span><i style="width:54px"></i><i style="width:18px"></i><i style="width:36px"></i></span><span><i style="width:18px"></i><i style="width:54px"></i></span></div>')
body=body.replace('{{OPMODS}}','<div class="opener__mods" aria-hidden="true"><span><i class="w" style="width:12px"></i><i style="width:36px"></i></span><span><i style="width:60px"></i><i class="w" style="width:12px"></i></span><span><i style="width:12px"></i><i class="w" style="width:24px"></i></span></div>')
body=re.sub(r'\{\{DOTS:(\d+)\}\}',lambda m:'<i class="on"></i>'*int(m.group(1))+'<i></i>'*(100-int(m.group(1))),body)
def form(m):
    cid,label,kind=m.group(1),m.group(2),m.group(3)
    fields=[('nombre','Nombre','text','name','Escribe tu nombre.',''),('correo','Correo','email','email','Escribe un correo válido, por ejemplo nombre@empresa.com.',' inputmode="email"'),('celular','Celular','tel','tel','Escribe un número de celular válido, con al menos 9 dígitos.',' inputmode="tel"'),('cargo','Cargo','text','organization-title','Escribe tu cargo.',''),('empresa','Empresa','text','organization','Escribe el nombre de tu empresa.','')]
    out=f'<form class="lead" id="form-{cid}" data-cta="{cid}" data-kind="{kind}" novalidate hidden><div class="lead__grid">'
    for n,l,t,ac,err,extra in fields:
        i=f'form-{cid}-{n}'
        out+=f'<div class="lead__f"><label for="{i}">{l}</label><input id="{i}" name="{n}" type="{t}" autocomplete="{ac}" required aria-describedby="{i}-err"{extra}><p class="lead__err" id="{i}-err" hidden>{err}</p></div>'
    out+=f'<div class="lead__f lead__f--send"><button class="btn btn--primary" type="submit">{label} {BTNI}</button></div></div><p class="lead__status" role="status" aria-live="polite"></p></form>'
    return out
body=re.sub(r'\{\{FORM:(\w+):([^:]+):(\w+)\}\}',form,body)
def pf(m):
    slug,name,role,rank,share,pct,p1,p2=m.group(1).split(':')
    posts=''.join(f'<li><span class="t">{t}</span><span class="n">{n}<small>interacciones</small></span></li>' for t,n in (p.split('|') for p in (p1,p2)))
    return (f'<article class="pf"><p class="pf__k">Directivo destacado</p><div class="pf__id"><div class="av"><img src="assets/directivos/{slug}.png" alt="Retrato de {name}" width="240" height="240" loading="lazy"><span class="av__rank">{rank}</span></div>'
            f'<div><p class="pf__name">{name}</p><p class="pf__role">{role}</p></div></div>'
            f'<div class="pf__share"><p><b>{share}</b></p><div class="pf__meter"><div class="hb__t" aria-hidden="true"><div class="hb__f" style="--v:{pct}"></div></div><span>{pct}% de las suyas</span></div></div>'
            f'<ul class="pf__posts">{posts}</ul></article>')
body=re.sub(r'\{\{PF:([^}]+)\}\}',pf,body)
ph=old[old.index('<div class="ph-panels">')+len('<div class="ph-panels">'):]
ph=ph[:ph.index('      </div>\n    </div>\n\n    <aside')].strip()
body=body.replace('{{PHASES}}',ph)
logos=re.search(r'<ul class="logos-grid w"[^>]*>(.*?)</ul>',main_eb,re.S).group(1).replace(' loading="eager"',' loading="lazy"')
body=body.replace('{{LOGOS}}',logos)
assert '{{' not in body, re.findall(r'\{\{[^}]*\}\}',body)[:5]
js=open(S+'/app.js').read()
out=head+css+body+'\n'+js
open(E+'/propuesta-web/marca-directiva-web.html','w',encoding='utf8').write(out)
print(len(out))
