<script>
(function () {
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (!document.documentElement.lang) document.documentElement.lang = 'es';

  /* ---- Destinos de los diez CTA.
     Mientras no exista el destino definitivo (calendario, test, formulario), cada CTA abre un correo
     a julio@verne.la (contacto indicado en el Word) con el asunto del pedido. Al completar `url` o
     `formEndpoint`, ese destino reemplaza al correo. Ver ebook/PENDIENTES.md. ---- */
  var CTA_CONFIG = {
    cta1:  { formEndpoint: null, recurso: null }, /* Guía de 1 página */
    cta2:  { formEndpoint: null },                /* Formulario «Te ayudamos a liderar la conversación» */
    cta3:  { url: null },                         /* Agenda «Conoce tu puntaje» */
    cta4:  { url: null },                         /* Test de arquetipos */
    cta5:  { url: null },                         /* Calendario «Conoce tu nota (30 min)» */
    cta6:  { url: null },                         /* Auditoría «Hazlo aquí» */
    cta7:  { url: null },                         /* «Haz que la IA sea tu ayuda, no tu reemplazo» */
    cta8:  { formEndpoint: null, recurso: null }, /* Checklist GEO (1 hoja) */
    cta9:  { url: null },                         /* «Solicita tu reporte» */
    cta10: { url: null },                         /* Calendario de reservas */
    whatsapp: { url: null },                      /* Por defecto: wa.me/51966050678 (número de Julio Talledo en el Word) */
    privacidad: { url: "https://verne-preview.pages.dev/Politicas%20de%20Privacidad" } /* Políticas de privacidad de Verne */
  };
  document.querySelectorAll('[data-cta-link]').forEach(function (a) {
    var cfg = CTA_CONFIG[a.getAttribute('data-cta-link')];
    if (cfg && cfg.url) {
      a.setAttribute('href', cfg.url); a.setAttribute('target', '_blank'); a.setAttribute('rel', 'noopener');
    }
  });

  /* ---- Formularios (CTA 1, 2 y 8). El botón es un enlace mailto (útil en el PDF); en la web abre el formulario. ---- */
  document.querySelectorAll('[data-cta-open]').forEach(function (b) {
    var f = document.getElementById(b.getAttribute('aria-controls'));
    b.addEventListener('keydown', function (e) { if (e.key === ' ') { e.preventDefault(); b.click(); } });
    b.addEventListener('click', function (e) {
      e.preventDefault();
      var open = b.getAttribute('aria-expanded') === 'true';
      b.setAttribute('aria-expanded', open ? 'false' : 'true');
      f.hidden = open;
      if (!open) { var first = f.querySelector('input'); if (first) first.focus(); }
    });
  });
  var CHECKS = {
    nombres: function (v) { return v.trim().length >= 2; },
    apellidos: function (v) { return v.trim().length >= 2; },
    correo: function (v) { return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v.trim()); },
    celular: function (v) { if (!v.trim()) return true; var d = v.replace(/[^0-9]/g, ''); return /^[+0-9\s().-]+$/.test(v.trim()) && d.length >= 9 && d.length <= 15; },
    empresa: function (v) { return v.trim().length >= 2; }
  };
  /* Enlace a políticas de privacidad: solo si existe la URL */
  if (CTA_CONFIG.privacidad.url) document.querySelectorAll('[data-privacy]').forEach(function (s) {
    var a = document.createElement('a'); a.href = CTA_CONFIG.privacidad.url; a.target = '_blank'; a.rel = 'noopener'; a.textContent = s.textContent; s.replaceWith(a);
  });
  function checkField(inp) {
    var ok = inp.type === 'checkbox' ? inp.checked : (CHECKS[inp.name] || function () { return true; })(inp.value);
    var err = document.getElementById(inp.getAttribute('aria-describedby'));
    inp.setAttribute('aria-invalid', ok ? 'false' : 'true');
    if (err) err.hidden = ok;
    return ok;
  }
  document.querySelectorAll('form.lead').forEach(function (f) {
    var status = f.querySelector('.lead__status');
    f.querySelectorAll('input').forEach(function (inp) {
      inp.addEventListener('blur', function () { if (inp.value && inp.type !== 'checkbox') checkField(inp); });
      inp.addEventListener(inp.type === 'checkbox' ? 'change' : 'input', function () { if (inp.getAttribute('aria-invalid') === 'true') checkField(inp); });
    });
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var firstBad = null;
      f.querySelectorAll('input').forEach(function (inp) { if (!checkField(inp) && !firstBad) firstBad = inp; });
      if (firstBad) { status.textContent = 'Revisa los campos marcados.'; firstBad.focus(); return; }
      var cfg = CTA_CONFIG[f.getAttribute('data-cta')] || {};
      if (cfg.formEndpoint) { /* Integración pendiente: enviar a cfg.formEndpoint y, si corresponde, entregar cfg.recurso. */ return; }
      /* Sin integración: se arma el correo con los datos para que la persona lo envíe a Verne. */
      var opener = document.querySelector('[aria-controls="' + f.id + '"]');
      var subject = decodeURIComponent((opener.getAttribute('href').split('subject=')[1] || '').replace(/\+/g, ' '));
      var lines = [];
      f.querySelectorAll('input:not([type=checkbox]), select, textarea').forEach(function (el) {
        var v = el.value.trim(); if (!v) return;
        lines.push(f.querySelector('label[for="' + el.id + '"]').textContent.replace(/\s*\*$/, '') + ': ' + v);
      });
      lines.push('Acepta las políticas de privacidad: sí');
      var nombre = (f.querySelector('[name="nombres"]').value || '').trim().split(' ')[0];
      status.textContent = 'Gracias' + (nombre ? ', ' + nombre : '') + '. Abrimos tu correo con la solicitud para Verne; solo tienes que enviarlo. Si no se abre, escríbenos a julio@verne.la.';
      window.location.href = 'mailto:julio@verne.la?subject=' + encodeURIComponent(subject) + '&body=' + encodeURIComponent(lines.join('\n'));
    });
  });


  /* ---- Descargar PDF: en claude.ai usa la capacidad «downloads»; fuera de ella, el enlace descarga el archivo ---- */
  var pdfLinks = document.querySelectorAll('[data-pdf]');
  var pdfNote = null;
  function pdfStatus(msg) {
    if (!pdfNote) { pdfNote = document.createElement('p'); pdfNote.className = 'sr-only'; pdfNote.setAttribute('role', 'status'); document.body.appendChild(pdfNote); }
    pdfNote.textContent = msg;
  }
  pdfLinks.forEach(function (a) {
    a.addEventListener('click', function (e) {
      if (!window.claude || typeof window.claude.use !== 'function') return; /* página independiente: descarga normal */
      e.preventDefault();
      if (a.getAttribute('aria-busy') === 'true') return;
      a.setAttribute('aria-busy', 'true');
      var href = a.getAttribute('href');
      Promise.all([window.claude.use('downloads'), fetch(href).then(function (r) { if (!r.ok) throw new Error('pdf'); return r.blob(); })])
        .then(function (res) {
          var dl = res[0], blob = res[1];
          if (!dl) { window.open(href, '_blank', 'noopener'); return; }
          return dl.save({ filename: 'Marca-Directiva-Verne.pdf', data: blob }).then(function () { pdfStatus('PDF descargado.'); });
        })
        .catch(function (err) {
          if (err && err.code === 'declined') return;
          window.open(href, '_blank', 'noopener');
        })
        .then(function () { a.removeAttribute('aria-busy'); });
    });
  });


  /* ---- Fig. 3.2: resaltar el recorrido de un tipo de fuente ---- */
  document.querySelectorAll('.gen').forEach(function (fig) {
    var btns = fig.querySelectorAll('.gen__s');
    btns.forEach(function (b) {
      b.addEventListener('click', function () {
        var on = b.getAttribute('aria-pressed') !== 'true';
        btns.forEach(function (x) { x.setAttribute('aria-pressed', 'false'); });
        if (on) { b.setAttribute('aria-pressed', 'true'); fig.setAttribute('data-active', b.dataset.src); } else { fig.removeAttribute('data-active'); }
      });
    });
    if (!('IntersectionObserver' in window)) { fig.classList.add('in'); return; }
    new IntersectionObserver(function (es) { es.forEach(function (e) { fig.classList.toggle('in', e.isIntersecting); }); }).observe(fig);
  });


  /* ---- Cabecera en móvil: se oculta al bajar y vuelve al subir ---- */
  (function () {
    var top = document.querySelector('.top'), lastY = scrollY, mq = window.matchMedia('(max-width: 560px)');
    addEventListener('scroll', function () {
      var y = scrollY, menuOpen = !document.getElementById('menu').hidden;
      if (!mq.matches || menuOpen || top.contains(document.activeElement) || y < 120) { top.classList.remove('is-away'); lastY = y; return; }
      if (Math.abs(y - lastY) < 8) return;
      top.classList.toggle('is-away', y > lastY); lastY = y;
    }, { passive: true });
    top.addEventListener('focusin', function () { top.classList.remove('is-away'); });
  })();

  /* ---- Índice desplegable ---- */
  var menuBtn = document.querySelector('.menu-btn');
  var menu = document.getElementById('menu');
  function closeMenu(focus) { menu.hidden = true; menuBtn.setAttribute('aria-expanded', 'false'); if (focus) menuBtn.focus(); }
  menuBtn.addEventListener('click', function () {
    var open = menuBtn.getAttribute('aria-expanded') === 'true';
    if (open) { closeMenu(); return; }
    menu.hidden = false; menuBtn.setAttribute('aria-expanded', 'true');
    var cur = menu.querySelector('[aria-current="true"]') || menu.querySelector('a'); cur.focus();
  });
  menu.addEventListener('click', function (e) { if (e.target.closest('a')) closeMenu(); });
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && !menu.hidden) closeMenu(true); });
  document.addEventListener('click', function (e) { if (!menu.hidden && !menu.contains(e.target) && !menuBtn.contains(e.target)) closeMenu(); });

  /* ---- Progreso de lectura, capítulo en curso y subsección activa ---- */
  var bar = document.querySelector('.progress');
  function onScroll() {
    var h = document.documentElement.scrollHeight - innerHeight;
    bar.style.transform = 'scaleX(' + (h > 0 ? Math.min(1, scrollY / h) : 0) + ')';
  }
  addEventListener('scroll', onScroll, { passive: true }); onScroll();
  var now = document.querySelector('.top__now');
  var links = menu.querySelectorAll('a');
  if ('IntersectionObserver' in window) {
    var spy = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        var id = e.target.id, label = e.target.getAttribute('data-chap') || '';
        links.forEach(function (a) { if (a.dataset.spy === id) a.setAttribute('aria-current', 'true'); else a.removeAttribute('aria-current'); });
        var m = label.match(/^(\d\d) · (.*)$/);
        now.innerHTML = '';
        if (m) { var b = document.createElement('b'); b.textContent = m[1]; now.appendChild(b); now.appendChild(document.createTextNode(m[2])); }
        else if (id !== 'portada') now.textContent = label;
      });
    }, { rootMargin: '-35% 0px -60% 0px' });
    document.querySelectorAll('[data-chap]').forEach(function (s) { spy.observe(s); });

    var sub = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        var side = e.target.closest('.read').querySelector('.read__side');
        side.querySelectorAll('a').forEach(function (a) {
          if (a.getAttribute('href') === '#' + e.target.id) a.setAttribute('aria-current', 'true'); else a.removeAttribute('aria-current');
        });
      });
    }, { rootMargin: '-20% 0px -70% 0px' });
    document.querySelectorAll('.read__side a').forEach(function (a) {
      var t = document.getElementById(a.getAttribute('href').slice(1)); if (t) sub.observe(t);
    });

    /* Revelado discreto: solo si hay observador y movimiento permitido */
    if (!reduce) {
      document.documentElement.classList.add('js-reveal');
      var io = new IntersectionObserver(function (es) {
        es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
      }, { rootMargin: '0px 0px -8% 0px' });
      document.querySelectorAll('.rv').forEach(function (el) {
        if (el.getBoundingClientRect().top < innerHeight) el.classList.add('in'); else io.observe(el);
      });
    }
  }

  /* ---- Pestañas accesibles (criterios, arquetipos y fases) ---- */
  function tabs(sel, onChange) {
    var t = Array.prototype.slice.call(document.querySelectorAll(sel));
    var p = t.map(function (b) { return document.getElementById(b.getAttribute('aria-controls')); });
    function select(i, focus) {
      t.forEach(function (b, j) {
        var on = i === j;
        b.setAttribute('aria-selected', on ? 'true' : 'false'); b.tabIndex = on ? 0 : -1; p[j].hidden = !on;
        if (on && !reduce) { p[j].classList.remove('enter'); void p[j].offsetWidth; p[j].classList.add('enter'); }
      });
      if (focus) t[i].focus();
      if (onChange) onChange(i);
    }
    t.forEach(function (b, i) {
      b.addEventListener('click', function () { select(i); });
      b.addEventListener('keydown', function (e) {
        var n = { ArrowRight: i + 1, ArrowDown: i + 1, ArrowLeft: i - 1, ArrowUp: i - 1, Home: 0, End: t.length - 1 }[e.key];
        if (n === undefined) return; e.preventDefault(); select((n + t.length) % t.length, true);
      });
    });
    return select;
  }
  tabs('.crit-seg');
  tabs('.ar-tab');
  var track = document.querySelector('.track');
  var selectPhase = tabs('.phase', function (i) { track.style.setProperty('--p', i / 3); });
  document.querySelectorAll('.ph-nav [data-go]').forEach(function (b) {
    b.addEventListener('click', function () { var i = +b.dataset.go - 1; if (i >= 0) selectPhase(i, true); });
  });

  /* ---- Filtro de años del gráfico de frecuencia ---- */
  var fq = document.querySelector('.fq');
  document.querySelectorAll('.chips .chip').forEach(function (c, _, all) {
    c.addEventListener('click', function () {
      all.forEach(function (o) { o.setAttribute('aria-pressed', o === c ? 'true' : 'false'); });
      fq.dataset.show = c.dataset.show;
    });
  });


  /* ---- Tema claro / oscuro: preferencia del dispositivo al inicio, elección manual guardada ---- */
  var root = document.documentElement;
  var KEY = 'verne-ebook-tema';
  var sw = document.querySelector('.theme-sw');
  var mq = window.matchMedia ? window.matchMedia('(prefers-color-scheme: dark)') : null;
  function stored() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function sync() {
    var dark = root.getAttribute('data-theme') === 'dark';
    sw.setAttribute('aria-checked', dark ? 'true' : 'false');
  }
  function apply(t, animate) {
    if (animate && !reduce) {
      root.classList.add('theme-fade');
      clearTimeout(apply.t); apply.t = setTimeout(function () { root.classList.remove('theme-fade'); }, 450);
    }
    root.setAttribute('data-theme', t); sync();
  }
  sw.addEventListener('click', function () {
    var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
    apply(next, true);
    try { localStorage.setItem(KEY, next); } catch (e) {}
  });
  if (mq) {
    var onSys = function (e) { if (!stored()) apply(e.matches ? 'dark' : 'light', true); };
    if (mq.addEventListener) mq.addEventListener('change', onSys); else if (mq.addListener) mq.addListener(onSys);
  }
  sync();
  /* Al imprimir, siempre la versión clara */
  var themeBeforePrint = null;
  addEventListener('beforeprint', function () { themeBeforePrint = root.getAttribute('data-theme'); root.setAttribute('data-theme', 'light'); });
  addEventListener('afterprint', function () { if (themeBeforePrint) root.setAttribute('data-theme', themeBeforePrint); themeBeforePrint = null; });

  /* ---- Impresión: todo visible y abierto ---- */
  var details = document.querySelectorAll('.acc details');
  addEventListener('beforeprint', function () {
    document.querySelectorAll('.rv').forEach(function (el) { el.classList.add('in'); });
    details.forEach(function (d) { d.dataset.was = d.open ? '1' : ''; d.open = true; });
  });
  addEventListener('afterprint', function () { details.forEach(function (d) { d.open = !!d.dataset.was; }); });
})();
</script>
