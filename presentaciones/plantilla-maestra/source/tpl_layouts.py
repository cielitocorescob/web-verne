"""VERNE master template — theme, slide master and layouts as raw OOXML.

Coordinates are in inches on a 13.333 x 7.5 in (16:9) canvas.
"""
from xml.sax.saxutils import escape

EMU = 914400
W, H, M = 13.333, 7.5, 0.65
R = W - M            # right content edge
CW = R - M           # content width

# ---- VERNE palette -----------------------------------------------------------------
PURPLE, NAVY, LAV, TXT, WHITE = '6D4ABE', '25283D', 'C0B0F4', '333333', 'FFFFFF'
LAVBG, LINE, GRAY, NOTE, MID, PANEL, DEEP = 'F3F0FB', 'D8D4EA', '6B6E80', '9A9CAB', '8F72D6', 'F5F5F7', '171828'

NS = ('xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" '
      'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
      'xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"')


def E(v):
    return int(round(v * EMU))


def xfrm(x, y, w, h):
    return f'<a:xfrm><a:off x="{E(x)}" y="{E(y)}"/><a:ext cx="{E(w)}" cy="{E(h)}"/></a:xfrm>'


def solid(color, alpha=None):
    a = f'<a:alpha val="{int(alpha * 1000)}"/>' if alpha is not None else ''
    return f'<a:solidFill><a:srgbClr val="{color}">{a}</a:srgbClr></a:solidFill>'


def rpr(sz, color, b=False, i=False, spc=None, cap=False, tag='a:defRPr', lang=True):
    attrs = f' sz="{int(sz * 100)}" b="{1 if b else 0}" i="{1 if i else 0}"'
    if spc is not None: attrs += f' spc="{spc}"'
    if cap: attrs += ' cap="all"'
    if lang and tag != 'a:defRPr': attrs = ' lang="es-PE"' + attrs
    return (f'<{tag}{attrs}>{solid(color)}<a:latin typeface="Poppins"/><a:ea typeface="Poppins"/>'
            f'<a:cs typeface="Poppins"/></{tag}>')


# ---- Typographic system (single source of truth, also documented in the guide) ----
# name: (size pt, bold, line spacing %, italic, letter spacing, caps)
TYPE = {
    'eyebrow':   (10.5, True, 100, False, 300, True),
    'title_xl':  (46, True, 92, False, None, False),
    'title':     (34, True, 95, False, None, False),
    'subtitle':  (16, False, 115, False, None, False),
    'body':      (12, False, 125, False, None, False),
    'highlight': (20, True, 105, False, None, False),
    'figure':    (66, True, 88, False, None, False),
    'figure_xl': (150, True, 82, False, None, False),
    'head':      (16, True, 105, False, None, False),
    'caption':   (10, False, 115, False, None, False),
    'note':      (8.5, False, 115, True, None, False),
    'number':    (30, True, 90, False, None, False),
    'quote':     (32, True, 112, False, None, False),
    'statement': (52, True, 95, False, None, False),
}


class Layout:
    def __init__(self, name, dark=False, bg=None, bg_image=None, chrome=None):
        self.name, self.dark, self.bg, self.bg_image = name, dark, bg, bg_image
        self.chrome = chrome if chrome is not None else dark   # draw own logo/number/url when master is hidden
        self.shapes, self._id, self.images = [], 2, {}

    def nid(self):
        self._id += 1
        return self._id

    # -- placeholders --------------------------------------------------------------
    def ph(self, kind, idx, x, y, w, h, prompt, style='body', color=TXT, anchor='t', align='l',
           geom='rect', fill=None, size=None, bold=None, lvl2=False, autofit=True):
        sz, b, ln, it, spc, cap = TYPE[style]
        if size: sz = size
        if bold is not None: b = bold
        sid = self.nid()
        typ = f' type="{kind}"' if kind != 'body' else ''
        idxa = f' idx="{idx}"' if idx is not None else ''
        ppr = (f'<a:lvl1pPr marL="0" indent="0" algn="{align}"><a:lnSpc><a:spcPct val="{ln * 1000}"/></a:lnSpc>'
               f'<a:spcBef><a:spcPts val="0"/></a:spcBef><a:spcAft><a:spcPts val="{600 if style == "body" else 0}"/></a:spcAft>'
               f'<a:buNone/>{rpr(sz, color, b, it, spc, cap)}</a:lvl1pPr>')
        if lvl2:
            ppr += (f'<a:lvl2pPr marL="228600" indent="-228600" algn="l"><a:lnSpc><a:spcPct val="{ln * 1000}"/></a:lnSpc>'
                    f'<a:spcAft><a:spcPts val="400"/></a:spcAft><a:buClr><a:srgbClr val="{PURPLE}"/></a:buClr>'
                    f'<a:buFont typeface="Arial"/><a:buChar char="•"/>{rpr(sz, color, False)}</a:lvl2pPr>')
        if style in ('figure', 'figure_xl', 'quote', 'statement', 'number', 'title_xl'): autofit = False
        fit = '<a:normAutofit/>' if autofit else '<a:noAutofit/>'
        fillx = solid(fill) if fill else '<a:noFill/>'
        body = (f'<p:txBody><a:bodyPr wrap="square" lIns="0" tIns="0" rIns="0" bIns="0" anchor="{anchor}">{fit}</a:bodyPr>'
                f'<a:lstStyle>{ppr}</a:lstStyle><a:p><a:r><a:rPr lang="es-PE"/><a:t>{escape(prompt)}</a:t></a:r></a:p></p:txBody>')
        if kind == 'pic':
            body = (f'<p:txBody><a:bodyPr wrap="square" lIns="91440" tIns="91440" rIns="91440" bIns="91440" anchor="ctr">'
                    f'<a:normAutofit/></a:bodyPr><a:lstStyle><a:lvl1pPr marL="0" indent="0" algn="ctr"><a:buNone/>'
                    f'{rpr(10, GRAY if not self.dark else LAV)}</a:lvl1pPr></a:lstStyle>'
                    f'<a:p><a:r><a:rPr lang="es-PE"/><a:t>{escape(prompt)}</a:t></a:r></a:p></p:txBody>')
        self.shapes.append(
            f'<p:sp><p:nvSpPr><p:cNvPr id="{sid}" name="{escape(prompt[:40])} {sid}"/><p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr>'
            f'<p:nvPr><p:ph{typ}{idxa} hasCustomPrompt="1"/></p:nvPr></p:nvSpPr>'
            f'<p:spPr>{xfrm(x, y, w, h)}<a:prstGeom prst="{geom}"><a:avLst/></a:prstGeom>{fillx}</p:spPr>{body}</p:sp>')

    def gframe(self, kind, idx, x, y, w, h):
        """Table / chart placeholder (graphic frame)."""
        sid = self.nid()
        self.shapes.append(
            f'<p:sp><p:nvSpPr><p:cNvPr id="{sid}" name="{kind} {sid}"/><p:cNvSpPr><a:spLocks noGrp="1"/></p:cNvSpPr>'
            f'<p:nvPr><p:ph type="{kind}" idx="{idx}"/></p:nvPr></p:nvSpPr><p:spPr>{xfrm(x, y, w, h)}</p:spPr>'
            f'<p:txBody><a:bodyPr/><a:lstStyle/><a:p><a:endParaRPr lang="es-PE"/></a:p></p:txBody></p:sp>')

    # -- decoration ----------------------------------------------------------------
    def rect(self, x, y, w, h, color, alpha=None, geom='rect', line=None):
        sid = self.nid()
        ln = f'<a:ln w="9525">{solid(line)}</a:ln>' if line else '<a:ln><a:noFill/></a:ln>'
        fill = solid(color, alpha) if color else '<a:noFill/>'
        self.shapes.append(
            f'<p:sp><p:nvSpPr><p:cNvPr id="{sid}" name="Forma {sid}"/><p:cNvSpPr/><p:nvPr userDrawn="1"/></p:nvSpPr>'
            f'<p:spPr>{xfrm(x, y, w, h)}<a:prstGeom prst="{geom}"><a:avLst/></a:prstGeom>{fill}{ln}</p:spPr>'
            f'<p:txBody><a:bodyPr/><a:lstStyle/><a:p><a:endParaRPr lang="es-PE"/></a:p></p:txBody></p:sp>')

    def hline(self, x, y, w, color=LINE, alpha=None):
        self.rect(x, y, w, 0.012, color, alpha)

    def vline(self, x, y, h, color=LINE, alpha=None):
        self.rect(x, y, 0.012, h, color, alpha)

    def text(self, x, y, w, h, s, sz, color, b=False, align='l', field=None, spc=None, anchor='t'):
        sid = self.nid()
        run = (f'<a:fld id="{{B6F15528-21DE-4FAA-801E-634DDDAF4B2B}}" type="{field}">{rpr(sz, color, b, tag="a:rPr", spc=spc)}<a:t>‹#›</a:t></a:fld>'
               if field else f'<a:r>{rpr(sz, color, b, tag="a:rPr", spc=spc)}<a:t>{escape(s)}</a:t></a:r>')
        self.shapes.append(
            f'<p:sp><p:nvSpPr><p:cNvPr id="{sid}" name="Texto {sid}"/><p:cNvSpPr txBox="1"/><p:nvPr userDrawn="1"/></p:nvSpPr>'
            f'<p:spPr>{xfrm(x, y, w, h)}<a:prstGeom prst="rect"><a:avLst/></a:prstGeom><a:noFill/></p:spPr>'
            f'<p:txBody><a:bodyPr wrap="square" lIns="0" tIns="0" rIns="0" bIns="0" anchor="{anchor}"/><a:lstStyle/>'
            f'<a:p><a:pPr algn="{align}"/>{run}</a:p></p:txBody></p:sp>')

    def image(self, key, x, y, w, h):
        sid = self.nid()
        self.images.setdefault(key, None)
        self.shapes.append(
            f'<p:pic><p:nvPicPr><p:cNvPr id="{sid}" name="Imagen {sid}"/><p:cNvPicPr><a:picLocks noChangeAspect="1"/></p:cNvPicPr>'
            f'<p:nvPr userDrawn="1"/></p:nvPicPr><p:blipFill><a:blip r:embed="{{{key}}}"/><a:stretch><a:fillRect/></a:stretch></p:blipFill>'
            f'<p:spPr>{xfrm(x, y, w, h)}<a:prstGeom prst="rect"><a:avLst/></a:prstGeom></p:spPr></p:pic>')

    # -- common blocks -------------------------------------------------------------
    def header(self, x=M, w=CW, title_w=None, eyebrow=True, sub=True, title_h=0.85, sub_y=None, title_size=None):
        dark = self.dark
        if eyebrow:
            self.ph('body', 10, x, 1.0, w, 0.28, 'CATEGORÍA · TEMA', 'eyebrow', LAV if dark else PURPLE)
        self.ph('title', None, x, 1.28, title_w or w, title_h, 'Título de la diapositiva', 'title',
                WHITE if dark else NAVY, size=title_size)
        if sub:
            self.ph('body', 11, x, sub_y or (1.28 + title_h + 0.1), title_w or w, 0.65,
                    'Bajada: una o dos líneas que den el contexto necesario.', 'subtitle', LINE if dark else GRAY)

    def xml(self):
        bg = ''
        if self.bg_image:
            bg = (f'<p:bg><p:bgPr><a:blipFill dpi="0" rotWithShape="1"><a:blip r:embed="{{{self.bg_image}}}"/><a:srcRect/>'
                  f'<a:stretch><a:fillRect/></a:stretch></a:blipFill><a:effectLst/></p:bgPr></p:bg>')
            self.images.setdefault(self.bg_image, None)
        elif self.bg:
            bg = f'<p:bg><p:bgPr>{solid(self.bg)}<a:effectLst/></p:bgPr></p:bg>'
        show = ' showMasterSp="0"' if self.chrome else ''
        return (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:sldLayout {NS} preserve="1" userDrawn="1"{show}>'
                f'<p:cSld name="{escape(self.name)}">{bg}<p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
                f'<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'
                f'{"".join(self.shapes)}</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sldLayout>')


def chrome(L, logo=True, number=True, url=True, on_color=False):
    """Logo, slide number and web address for layouts that hide the master graphics."""
    if logo: L.image('logo_white', 11.97, 0.42, 1.05, 0.37)
    if number: L.text(0.0, 7.06, 0.74, 0.25, '', 9, WHITE, True, align='r', field='slidenum')
    if url: L.text(11.02, 7.02, 1.66, 0.22, 'www.verne.la', 9, LAVBG if on_color else LINE, align='r')


def build_layouts():
    Ls = []

    # 01 Portada principal ------------------------------------------------------------
    L = Layout('01 Portada principal', dark=True, bg_image='glow_a')
    L.image('logo_white', M, 0.6, 1.6, 0.563)
    L.ph('body', 10, M, 2.2, 8, 0.28, 'CATEGORÍA · AÑO', 'eyebrow', LAV)
    L.ph('ctrTitle', None, M, 2.6, 10.6, 2.75, 'Título principal de la presentación', 'title_xl', WHITE, anchor='t')
    L.ph('subTitle', 1, M, 5.5, 7.4, 0.8, 'Bajada o descripción breve de la presentación', 'subtitle', LINE)
    L.hline(M, 6.5, 0.6, LAV)
    L.ph('body', 11, M, 6.65, 7, 0.3, 'Cliente · Fecha · Lugar', 'caption', LINE)
    chrome(L, logo=False, number=False)
    Ls.append(L)

    # 02 Portada con imagen -----------------------------------------------------------
    L = Layout('02 Portada con imagen', dark=True, bg=NAVY)
    L.ph('pic', 13, 6.0, 0, W - 6.0, H, 'Inserta una fotografía protagonista', fill='3E3A62')
    L.image('logo_white', M, 0.6, 1.45, 0.51)
    L.ph('body', 10, M, 2.25, 4.9, 0.28, 'CATEGORÍA · AÑO', 'eyebrow', LAV)
    L.ph('ctrTitle', None, M, 2.65, 5.0, 2.5, 'Título principal de la presentación', 'title', WHITE, size=40)
    L.ph('subTitle', 1, M, 5.25, 4.9, 0.8, 'Bajada o descripción breve', 'subtitle', LINE)
    L.ph('body', 11, M, 6.65, 5, 0.3, 'Cliente · Fecha · Lugar', 'caption', LINE)
    Ls.append(L)

    # 03 Apertura de sección ----------------------------------------------------------
    L = Layout('03 Apertura de sección', dark=True, bg=PURPLE)
    chrome(L, on_color=True)
    L.ph('body', 12, M, 0.95, 6, 2.3, '01', 'figure_xl', LAV)
    L.ph('title', None, M, 3.55, 9.5, 1.6, 'Nombre de la sección', 'title_xl', WHITE)
    L.ph('body', 11, M, 5.3, 7.5, 0.9, 'Una línea que anticipe lo que viene en esta sección.', 'subtitle', LAVBG)
    Ls.append(L)

    # 04 Título + bajada --------------------------------------------------------------
    L = Layout('04 Título + bajada')
    L.header(title_w=11)
    L.ph('body', 14, M, 3.15, 7.6, 3.4, 'Texto de desarrollo. Usa párrafos breves; el segundo nivel crea viñetas.', 'body', TXT, lvl2=True)
    Ls.append(L)

    # 05 Texto + imagen ---------------------------------------------------------------
    L = Layout('05 Texto + imagen')
    L.ph('pic', 13, 7.05, 1.0, R - 7.05, 5.85, 'Inserta una imagen', fill=LAVBG)
    L.header(w=5.9, title_h=1.4)
    L.ph('body', 15, M, 3.95, 5.7, 0.9, 'Destacado: la idea que debe recordarse.', 'highlight', PURPLE)
    L.ph('body', 14, M, 5.0, 5.7, 1.6, 'Texto de apoyo breve.', 'body', TXT, lvl2=True)
    Ls.append(L)

    # 06 Imagen + texto ---------------------------------------------------------------
    L = Layout('06 Imagen + texto')
    L.ph('pic', 13, 0, 0, 5.6, H, 'Inserta una imagen vertical', fill=LAVBG)
    X = 6.2
    L.header(x=X, w=R - X)
    L.hline(X, 3.25, R - X)
    L.ph('body', 14, X, 3.45, R - X, 3.2, 'Desarrollo, lista o pasos. El segundo nivel crea viñetas.', 'body', TXT, lvl2=True)
    Ls.append(L)

    # 07 Imagen a pantalla completa ---------------------------------------------------
    L = Layout('07 Imagen a pantalla completa', dark=True, bg=DEEP, chrome=True)
    L.ph('pic', 13, 0, 0, W, H, 'Inserta una fotografía a pantalla completa. Añade el overlay de la guía para asegurar legibilidad.', fill='2E2F47')
    L.ph('body', 10, M, 4.0, 8, 0.28, 'CATEGORÍA · TEMA', 'eyebrow', LAV)
    L.ph('title', None, M, 4.3, 8.6, 1.6, 'Mensaje principal sobre la imagen', 'title', WHITE, size=40, anchor='b')
    L.ph('body', 11, M, 6.05, 7.4, 0.6, 'Bajada breve, máximo dos líneas.', 'subtitle', WHITE)
    Ls.append(L)

    # 08 Gran titular / statement -----------------------------------------------------
    L = Layout('08 Gran titular / statement', bg=LAVBG)
    L.ph('body', 10, M, 1.0, 9, 0.28, 'CATEGORÍA · TEMA', 'eyebrow', PURPLE)
    L.ph('title', None, M, 1.6, 11.6, 3.7, 'Una idea poderosa, dicha en una sola frase.', 'statement', NAVY)
    L.ph('body', 11, M, 5.6, 7.5, 0.8, 'Contexto opcional en una línea.', 'subtitle', GRAY)
    Ls.append(L)

    # 09 Cifra protagonista -----------------------------------------------------------
    L = Layout('09 Cifra protagonista')
    L.ph('body', 10, M, 1.0, 9, 0.28, 'CATEGORÍA · TEMA', 'eyebrow', PURPLE)
    L.ph('title', None, M, 1.28, 11, 0.8, 'Título de la diapositiva', 'title', NAVY, size=28)
    L.ph('body', 16, M - 0.05, 2.35, 6.6, 2.9, '90%', 'figure_xl', PURPLE, anchor='ctr')
    L.vline(7.25, 2.75, 2.6)
    L.ph('body', 17, 7.6, 2.75, 5.0, 0.9, 'Qué mide la cifra', 'highlight', NAVY, size=22)
    L.ph('body', 14, 7.6, 3.75, 5.0, 1.4, 'Explicación breve: qué significa y por qué importa.', 'body', TXT, size=13)
    L.ph('body', 18, 7.6, 5.3, 5.0, 0.3, 'Fuente: nombre de la fuente, año', 'note', NOTE)
    Ls.append(L)

    # 10 Dos columnas -----------------------------------------------------------------
    L = Layout('10 Dos columnas')
    L.header()
    for i, x in enumerate((M, M + 6.19)):
        L.hline(x, 3.15, 5.84)
        L.ph('body', 20 + i, x, 3.35, 5.84, 0.45, 'Subtítulo de columna', 'head', NAVY)
        L.ph('body', 22 + i, x, 3.9, 5.6, 2.7, 'Texto de la columna.', 'body', TXT, lvl2=True)
    Ls.append(L)

    # 11 Tres columnas ----------------------------------------------------------------
    L = Layout('11 Tres columnas')
    L.header()
    for i in range(3):
        x = M + i * 4.08
        L.hline(x, 3.15, 3.87)
        L.ph('body', 30 + i, x, 3.3, 3.87, 0.6, f'0{i + 1}', 'number', LAV)
        L.ph('body', 33 + i, x, 3.95, 3.7, 0.45, 'Subtítulo', 'head', NAVY)
        L.ph('body', 36 + i, x, 4.5, 3.6, 2.0, 'Texto breve de apoyo.', 'body', TXT)
    Ls.append(L)

    # 12 Comparación ------------------------------------------------------------------
    L = Layout('12 Comparación')
    L.header(sub=False)
    L.rect(M, 2.45, 5.84, 4.2, PANEL)
    L.rect(M + 6.19, 2.45, 5.84, 4.2, NAVY)
    for i, (x, dark) in enumerate(((M, False), (M + 6.19, True))):
        L.ph('body', 40 + 3 * i, x + 0.4, 2.8, 5.0, 0.28, 'OPCIÓN A' if not i else 'OPCIÓN B', 'eyebrow', LAV if dark else PURPLE)
        L.ph('body', 41 + 3 * i, x + 0.4, 3.15, 5.0, 0.9, 'Encabezado de la comparación', 'highlight', WHITE if dark else NAVY)
        L.ph('body', 42 + 3 * i, x + 0.4, 4.15, 5.0, 2.2, 'Puntos a comparar.', 'body', LINE if dark else TXT, lvl2=True)
    Ls.append(L)

    # 13 Proceso / pasos --------------------------------------------------------------
    L = Layout('13 Proceso / pasos')
    L.header()
    L.hline(M, 3.3, CW, LINE)
    for i in range(4):
        x = M + i * 3.07
        L.ph('body', 50 + i, x, 3.5, 2.8, 0.55, f'0{i + 1}', 'number', PURPLE, size=26)
        L.ph('body', 54 + i, x, 4.1, 2.8, 0.75, 'Nombre del paso', 'head', NAVY)
        L.ph('body', 58 + i, x, 4.9, 2.75, 1.7, 'Qué ocurre en este paso.', 'body', GRAY, size=11.5)
    Ls.append(L)

    # 14 Timeline ---------------------------------------------------------------------
    L = Layout('14 Timeline', dark=True, bg_image='glow_b')
    chrome(L)
    L.header()
    L.hline(M, 4.2, CW, WHITE, alpha=25)
    for i in range(4):
        x = M + i * 3.07
        L.ph('body', 70 + i, x, 3.5, 2.8, 0.55, 'Fecha', 'highlight', LAV, size=22, anchor='b')
        L.rect(x, 4.12, 0.17, 0.17, PURPLE, geom='ellipse')
        L.ph('body', 75 + i, x, 4.5, 2.8, 0.45, 'Hito', 'head', WHITE, size=15)
        L.ph('body', 80 + i, x, 5.0, 2.75, 1.5, 'Descripción breve del hito.', 'body', LINE, size=11)
    Ls.append(L)

    # 15 Diagrama / ecosistema --------------------------------------------------------
    L = Layout('15 Diagrama / ecosistema')
    L.header(w=5.6, title_h=1.4)
    L.ph('body', 14, M, 4.0, 5.4, 2.6, 'Explica cada nivel del diagrama.', 'body', TXT, lvl2=True)
    cx, cy = 9.55, 4.05
    for d, c in ((5.3, LAVBG), (3.7, LAV), (2.1, PURPLE)):
        L.rect(cx - d / 2, cy - d / 2, d, d, c, geom='ellipse')
    L.ph('body', 90, cx - 0.95, cy - 0.45, 1.9, 0.9, 'Núcleo', 'head', WHITE, align='ctr', anchor='ctr', size=14)
    L.ph('body', 91, cx - 1.5, cy - 1.72, 3.0, 0.55, 'Nivel 2', 'caption', NAVY, align='ctr', anchor='ctr', bold=True, size=11)
    L.ph('body', 92, cx - 1.8, cy - 2.52, 3.6, 0.55, 'Nivel 3', 'caption', PURPLE, align='ctr', anchor='ctr', bold=True, size=11)
    Ls.append(L)

    # 16 Servicios o soluciones -------------------------------------------------------
    L = Layout('16 Servicios o soluciones', dark=True, bg_image='glow_a')
    chrome(L)
    L.header(sub=False)
    for i in range(4):
        x = M + i * 3.1
        if i: L.vline(x - 0.2, 2.5, 3.95, WHITE, alpha=16)
        L.ph('pic', 100 + i, x, 2.55, 0.85, 0.85, 'Ícono', geom='ellipse', fill=PURPLE)
        L.ph('body', 104 + i, x, 3.6, 2.7, 0.78, 'Nombre', 'head', WHITE, size=19, anchor='b')
        L.ph('body', 108 + i, x, 4.5, 2.6, 0.5, 'Bajada corta', 'caption', LAV, bold=True, size=11.5)
        L.ph('body', 112 + i, x, 5.1, 2.6, 1.4, 'Qué hace y para quién.', 'body', LINE, size=11)
    Ls.append(L)

    # 17 Casos / proyectos ------------------------------------------------------------
    L = Layout('17 Casos / proyectos')
    L.ph('pic', 13, 7.45, 1.0, R - 7.45, 3.35, 'Imagen del caso', fill=LAVBG)
    L.header(w=6.3, title_h=1.4)
    L.ph('body', 14, M, 4.0, 6.1, 2.6, 'Qué hicimos y cómo.', 'body', TXT, lvl2=True)
    for i in range(3):
        x = 7.45 + i * 1.75
        L.hline(x, 4.7, 1.6)
        L.ph('body', 120 + i, x, 4.85, 1.7, 0.75, '+00%', 'figure', PURPLE, size=30, anchor='b')
        L.ph('body', 123 + i, x, 5.65, 1.6, 0.6, 'Qué mide', 'caption', GRAY)
    Ls.append(L)

    # 18 Clientes / logos -------------------------------------------------------------
    L = Layout('18 Clientes / logos')
    L.ph('body', 10, M, 1.0, 3.8, 0.28, 'CLIENTES', 'eyebrow', PURPLE)
    L.ph('title', None, M, 1.28, 3.8, 1.8, 'Confían en nosotros', 'title', NAVY, size=40)
    L.ph('body', 11, M, 3.25, 3.4, 1.2, 'Contexto breve sobre los clientes.', 'subtitle', GRAY)
    X0, WR = 4.75, R - 4.75
    for r in range(3):
        y = 1.15 + r * 1.85
        L.hline(X0, y, WR)
        L.ph('body', 130 + r, X0, y + 0.15, WR, 0.3, 'Sector o grupo', 'caption', PURPLE, bold=True, size=11)
        for c in range(5):
            L.ph('pic', 140 + r * 5 + c, X0 + c * (WR / 5), y + 0.6, WR / 5 - 0.3, 0.7, 'Logo')
    Ls.append(L)

    # 19 Equipo / perfiles ------------------------------------------------------------
    L = Layout('19 Equipo / perfiles')
    L.header()
    for i in range(3):
        x = M + i * 4.08
        L.ph('pic', 160 + i, x, 3.0, 1.25, 1.25, 'Foto', geom='ellipse', fill=LAVBG)
        L.ph('body', 163 + i, x, 4.45, 3.75, 0.45, 'Nombre Apellido', 'head', NAVY, size=20)
        L.ph('body', 166 + i, x, 4.95, 3.75, 0.3, 'CARGO', 'eyebrow', PURPLE, size=9.5)
        L.ph('body', 169 + i, x, 5.35, 3.6, 1.3, 'Experiencia y aporte en dos o tres líneas.', 'body', TXT, size=11)
    Ls.append(L)

    # 20 Testimonio o cita ------------------------------------------------------------
    L = Layout('20 Testimonio o cita', dark=True, bg_image='glow_b')
    chrome(L)
    L.text(M - 0.05, 0.55, 2.0, 2.0, '“', 160, LAV, True)
    L.ph('body', 170, M, 2.35, 10.2, 2.6, 'Cita textual del cliente o vocero, con comillas implícitas.', 'quote', WHITE)
    L.ph('pic', 171, M, 5.45, 0.9, 0.9, 'Foto', geom='ellipse', fill='3E3A62')
    L.ph('body', 172, 1.8, 5.5, 7, 0.4, 'Nombre Apellido', 'head', WHITE)
    L.ph('body', 173, 1.8, 5.92, 7, 0.3, 'Cargo · Empresa', 'caption', LINE, size=11)
    Ls.append(L)

    # 21 Datos / métricas -------------------------------------------------------------
    L = Layout('21 Datos / métricas')
    L.header()
    for i in range(4):
        x = M + i * 3.07
        L.hline(x, 3.25, 2.8)
        L.ph('body', 180 + i, x, 3.4, 2.85, 1.15, '+00%', 'figure', PURPLE, size=54, anchor='b')
        L.ph('body', 184 + i, x, 4.65, 2.8, 0.45, 'Indicador', 'head', NAVY, size=14)
        L.ph('body', 188 + i, x, 5.15, 2.7, 1.0, 'Contexto de la cifra.', 'body', GRAY, size=11)
    L.ph('body', 192, M, 6.45, 10, 0.3, 'Fuente: nombre de la fuente, año', 'note', NOTE)
    Ls.append(L)

    # 22 Tabla simple -----------------------------------------------------------------
    L = Layout('22 Tabla simple')
    L.header()
    L.gframe('tbl', 200, M, 3.05, CW, 3.3)
    L.ph('body', 201, M, 6.5, 10, 0.3, 'Nota o fuente de la tabla', 'note', NOTE)
    Ls.append(L)

    # 23 Gráfico ----------------------------------------------------------------------
    L = Layout('23 Gráfico')
    L.header(w=CW)
    L.gframe('chart', 210, M, 3.0, 7.9, 3.6)
    L.vline(8.95, 3.1, 3.3)
    L.ph('body', 15, 9.25, 3.1, 3.4, 1.4, 'Lectura clave del gráfico', 'highlight', PURPLE)
    L.ph('body', 14, 9.25, 4.6, 3.4, 1.6, 'Explica qué muestra y qué implica.', 'body', TXT, size=11)
    L.ph('body', 211, 9.25, 6.3, 3.4, 0.3, 'Fuente: nombre, año', 'note', NOTE)
    Ls.append(L)

    # 24 Cierre -----------------------------------------------------------------------
    L = Layout('24 Cierre', dark=True, bg_image='glow_b')
    chrome(L, logo=False, url=False)
    L.image('logo_white', M, 0.6, 1.6, 0.563)
    L.ph('title', None, M, 2.4, 10, 2.2, 'Gracias', 'statement', WHITE, size=72)
    L.ph('body', 11, M, 4.75, 8.5, 0.9, 'Mensaje de cierre o siguiente paso.', 'subtitle', LINE, size=18)
    L.hline(M, 6.35, 0.6, LAV)
    L.text(M, 6.5, 4, 0.35, 'www.verne.la', 14, LAV, True)
    Ls.append(L)

    # 25 Contacto ---------------------------------------------------------------------
    L = Layout('25 Contacto')
    L.ph('pic', 13, 7.45, 1.0, R - 7.45, 5.85, 'Inserta una imagen', fill=LAVBG)
    L.ph('body', 10, M, 1.0, 6, 0.28, 'CONTACTO', 'eyebrow', PURPLE)
    L.ph('title', None, M, 1.28, 6.3, 1.0, 'Conversemos', 'title_xl', NAVY)
    L.ph('body', 11, M, 2.4, 6.0, 0.7, 'Una línea de invitación a continuar la conversación.', 'subtitle', GRAY)
    for i in range(3):
        y = 3.5 + i * 1.0
        L.hline(M, y, 6.2)
        L.ph('body', 220 + i, M, y + 0.15, 6.2, 0.28, 'ETIQUETA', 'eyebrow', PURPLE, size=9)
        L.ph('body', 223 + i, M, y + 0.45, 6.2, 0.45, 'Dato de contacto', 'head', NAVY, size=17)
    Ls.append(L)

    # 26 Solo título ------------------------------------------------------------------
    L = Layout('26 Solo título')
    L.header(sub=False)
    Ls.append(L)

    # 27 En blanco --------------------------------------------------------------------
    Ls.append(Layout('27 En blanco'))
    return Ls


# ---- Slide master ----------------------------------------------------------------------
def lvl(n, sz, color, b=False, bullet=False, ln=120):
    marl = 0 if not bullet else 228600 * (n - 1)
    bu = (f'<a:buClr><a:srgbClr val="{PURPLE}"/></a:buClr><a:buFont typeface="Arial"/><a:buChar char="•"/>'
          if bullet else '<a:buNone/>')
    ind = ' indent="-228600"' if bullet else ' indent="0"'
    return (f'<a:lvl{n}pPr marL="{marl}"{ind} algn="l" defTabSz="914400" rtl="0" eaLnBrk="1" latinLnBrk="0" hangingPunct="1">'
            f'<a:lnSpc><a:spcPct val="{ln * 1000}"/></a:lnSpc><a:spcBef><a:spcPts val="0"/></a:spcBef>'
            f'<a:spcAft><a:spcPts val="600"/></a:spcAft>{bu}{rpr(sz, color, b)}</a:lvl{n}pPr>')


def master_xml(rid_layouts, rid_logo):
    body_lv = lvl(1, 14, TXT) + ''.join(lvl(n, 13 - (n - 2) * 0.5, TXT, bullet=True) for n in range(2, 10))
    title_lv = (f'<a:lvl1pPr algn="l" defTabSz="914400" rtl="0" eaLnBrk="1" latinLnBrk="0" hangingPunct="1">'
                f'<a:lnSpc><a:spcPct val="95000"/></a:lnSpc><a:spcBef><a:spcPct val="0"/></a:spcBef><a:buNone/>'
                f'{rpr(34, NAVY, True)}</a:lvl1pPr>')
    other = (f'<a:defPPr><a:defRPr lang="es-PE"/></a:defPPr>' +
             ''.join(f'<a:lvl{n}pPr marL="{(n - 1) * 457200}" algn="l" defTabSz="914400">{rpr(12, TXT)}</a:lvl{n}pPr>' for n in range(1, 10)))
    L = Layout('master')
    L.ph('title', None, M, 1.28, CW, 0.85, 'Título de la diapositiva', 'title', NAVY)
    L.shapes[-1] = L.shapes[-1].replace(' hasCustomPrompt="1"', '')
    L.ph('body', 1, M, 2.4, CW, 4.2, 'Texto', 'body', TXT)
    L.shapes[-1] = L.shapes[-1].replace(' hasCustomPrompt="1"', '')
    L.image('logo', 11.97, 0.42, 1.05, 0.37)
    L.text(0.0, 7.06, 0.74, 0.25, '', 9, TXT, True, align='r', field='slidenum')
    L.text(11.02, 7.02, 1.66, 0.22, 'www.verne.la', 9, GRAY, align='r')
    tree = ''.join(L.shapes).replace('{logo}', rid_logo)
    ids = ''.join(f'<p:sldLayoutId id="{2147483649 + i}" r:id="{rid}"/>' for i, rid in enumerate(rid_layouts))
    return (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?><p:sldMaster {NS}><p:cSld>'
            f'<p:bg><p:bgPr>{solid(WHITE)}<a:effectLst/></p:bgPr></p:bg><p:spTree><p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
            f'<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'
            f'{tree}</p:spTree></p:cSld>'
            f'<p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/>'
            f'<p:sldLayoutIdLst>{ids}</p:sldLayoutIdLst>'
            f'<p:txStyles><p:titleStyle>{title_lv}</p:titleStyle><p:bodyStyle>{body_lv}</p:bodyStyle><p:otherStyle>{other}</p:otherStyle></p:txStyles>'
            f'</p:sldMaster>')


THEME_COLORS = [('dk1', TXT), ('lt1', WHITE), ('dk2', NAVY), ('lt2', LAVBG), ('accent1', PURPLE), ('accent2', LAV),
                ('accent3', NAVY), ('accent4', MID), ('accent5', LINE), ('accent6', GRAY), ('hlink', PURPLE), ('folHlink', MID)]

TABLE_STYLE_ID = '{8A3F2C11-5E1B-4C7A-9D2E-7A1B3C4D5E6F}'


def table_styles_xml():
    def border(side, color, w=9525):
        return f'<a:{side}><a:ln w="{w}">{solid(color)}</a:ln></a:{side}>'
    font = f'<a:fontRef idx="minor"><a:prstClr val="black"/></a:fontRef><a:srgbClr val="{TXT}"/>'
    return (f'<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            f'<a:tblStyleLst xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" def="{TABLE_STYLE_ID}">'
            f'<a:tblStyle styleId="{TABLE_STYLE_ID}" styleName="VERNE · Tabla editorial">'
            f'<a:wholeTbl><a:tcTxStyle>{font}</a:tcTxStyle><a:tcStyle><a:tcBdr>'
            f'<a:left><a:ln><a:noFill/></a:ln></a:left><a:right><a:ln><a:noFill/></a:ln></a:right>'
            f'{border("top", LINE)}{border("bottom", LINE)}{border("insideH", LINE)}<a:insideV><a:ln><a:noFill/></a:ln></a:insideV>'
            f'</a:tcBdr><a:fill><a:noFill/></a:fill></a:tcStyle></a:wholeTbl>'
            f'<a:band1H><a:tcStyle><a:tcBdr/><a:fill>{solid(PANEL)}</a:fill></a:tcStyle></a:band1H>'
            f'<a:firstCol><a:tcTxStyle b="on"><a:fontRef idx="minor"><a:prstClr val="black"/></a:fontRef><a:srgbClr val="{NAVY}"/></a:tcTxStyle><a:tcStyle><a:tcBdr/></a:tcStyle></a:firstCol>'
            f'<a:firstRow><a:tcTxStyle b="on"><a:fontRef idx="minor"><a:prstClr val="black"/></a:fontRef><a:srgbClr val="{WHITE}"/></a:tcTxStyle>'
            f'<a:tcStyle><a:tcBdr>{border("bottom", PURPLE, 19050)}</a:tcBdr><a:fill>{solid(NAVY)}</a:fill></a:tcStyle></a:firstRow>'
            f'</a:tblStyle></a:tblStyleLst>')
