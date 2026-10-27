<script>
/* Test «¿Qué arquetipo de directivo digital eres?» — preguntas, perfiles y textos entregados por Verne. */
(function () {
  var box = document.getElementById('test-arquetipo');
  var opener = document.querySelector('[data-test-open]');
  if (!box || !opener) return;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var Q = [
    { q: 'Cuando publicas algo en LinkedIn, ¿qué tipo de contenido te sale más natural?', o: [
      ['Una reflexión sobre algo que aprendí o viví liderando', 'I'], ['Un logro del equipo o un hito de la organización', 'E'],
      ['Una explicación de algo de mi industria que pocos entienden bien', 'D'], ['Mi postura sobre un tema de agenda pública que toca a mi sector', 'A']] },
    { q: 'Un medio te invita a escribir una columna. ¿Sobre qué escribes?', o: [
      ['Una lección que cambió cómo tomo decisiones', 'I'], ['Lo que estamos construyendo como organización y hacia dónde vamos', 'E'],
      ['Una tendencia del sector que muchos subestiman', 'D'], ['Un problema social o ambiental donde las empresas deberían actuar', 'A']] },
    { q: 'Tu equipo de comunicaciones te propone tres publicaciones para la semana. ¿Cuál priorizas?', o: [
      ['Un texto donde cuento qué me llevé de un evento o conversación reciente', 'I'], ['Un post que muestra un proyecto del equipo con resultados concretos', 'E'],
      ['Un análisis de un cambio regulatorio que impacta a la industria', 'D'], ['Una declaración sobre sostenibilidad o inclusión respaldada con acciones de la empresa', 'A']] },
    { q: 'Cuando te presentan en un panel, ¿cómo preferirías que te describan?', o: [
      ['Como alguien que piensa diferente y comparte su criterio abiertamente', 'I'], ['Como quien lidera una organización que vale la pena conocer', 'E'],
      ['Como una referencia que hace accesible lo complejo del sector', 'D'], ['Como alguien que usa su posición para impulsar cambios concretos', 'A']] },
    { q: '¿Qué te confirma que una publicación funcionó?', o: [
      ['Que alguien me diga “eso me hizo pensar”', 'I'], ['Que un colaborador lo comparta y diga “así se trabaja aquí”', 'E'],
      ['Que alguien use lo que escribí para entender mejor algo de la industria', 'D'], ['Que mi postura abra una conversación incómoda pero necesaria', 'A']] },
    { q: 'Un cliente potencial revisa tu LinkedIn antes de una reunión. ¿Qué te gustaría que encuentre?', o: [
      ['Que tiene enfrente a alguien con criterio propio y puntos de vista claros', 'I'], ['Que la empresa que represento tiene una historia sólida detrás', 'E'],
      ['Que entiende su sector tan bien como él y puede aportar perspectiva', 'D'], ['Que no evita los temas difíciles y respalda con hechos lo que dice', 'A']] }
  ];
  var P = {
    I: { name: 'El inspirador', pct: '6,5 %',
      desc: 'Tu marca directiva se construye desde tu criterio personal. Publicas desde lo que piensas, lo que aprendiste y cómo ves las cosas, y eso es lo que conecta. Tu audiencia te sigue por tu punto de vista, no por tu cargo.',
      risk: 'El riesgo: que tu contenido se desconecte de la organización que representas. Equilibra la reflexión propia con los pilares de tu empresa para que ambas marcas se potencien.',
      ex: 'Ejemplos en el Ranking 2026: Fernando Eguiluz (CEO BBVA Perú), Rubén Sánchez (CEO Grupo San Antonio).' },
    E: { name: 'El embajador', pct: '65,4 %',
      desc: 'Tu marca directiva funciona como amplificador de tu organización. Muestras lo que hace el equipo, compartes logros institucionales e involucras a tus colaboradores en la conversación. Es el perfil que más engagement genera.',
      risk: 'El riesgo: que tu perfil se confunda con el canal corporativo. Lo que diferencia al embajador del comunicado de prensa es que el directivo aporta su lectura, no solo la noticia.',
      ex: 'Ejemplos en el Ranking 2026: Mario Potestá (CEO Rimac Seguros), Katerina Añaños (Gerente General ISM).' },
    D: { name: 'El educador', pct: '4,1 %',
      desc: 'Tu marca directiva se sostiene en tu capacidad de hacer accesible lo complejo. Explicas tendencias, traduces regulaciones, aterrizas conceptos del sector. Tu audiencia te busca para entender, no para entretenerse.',
      risk: 'El riesgo: que tu contenido sea tan sectorial que solo lo lean tus pares. Mezcla la profundidad técnica con preguntas que le importen a quien toma decisiones fuera de tu industria.',
      ex: 'Ejemplos en el Ranking 2026: Javier Ichazo (Gerente General Mibanco), Marco Fragale (CEO Orygen).' },
    A: { name: 'El activista', pct: '24,0 %',
      desc: 'Tu marca directiva se define por dónde te paras. Opinas sobre coyuntura, sostenibilidad o inclusión, y lo haces desde una posición visible. Tu audiencia valora que no evites los temas incómodos.',
      risk: 'El riesgo: que lo que digas no coincida con lo que tu empresa hace. La consistencia entre discurso y acción es lo que separa al activista creíble del que solo busca titulares.',
      ex: 'Ejemplos en el Ranking 2026: Juan Stoessel (CEO Casa Andina), Diego Cavero Belaunde (Gerente General BCP).' }
  };
  /* Destino del registro del test. null = sin integración: se muestra el resultado y no se envía nada. */
  var TEST_ENDPOINT = null;

  var $ = function (s) { return box.querySelector(s); };
  var steps = box.querySelectorAll('[data-step]');
  var cur = 0, scores, sel = null, win = 'I', ties = [];
  function show(name, focusEl) {
    steps.forEach(function (s) {
      var on = s.getAttribute('data-step') === name; s.hidden = !on;
      if (on && !reduce) { s.classList.remove('enter'); void s.offsetWidth; s.classList.add('enter'); }
    });
    if (focusEl) focusEl.focus({ preventScroll: true });
  }
  function shuffle(a) { a = a.slice(); for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; } return a; }
  function reset() { cur = 0; sel = null; scores = { I: 0, E: 0, D: 0, A: 0 }; }
  function question() {
    sel = null;
    var q = Q[cur], next = $('[data-quiz="next"]');
    $('.quiz__bar i').style.width = (cur / Q.length * 100) + '%';
    $('.quiz__bar').setAttribute('aria-valuenow', cur);
    $('.quiz__count').textContent = 'Pregunta ' + (cur + 1) + ' de ' + Q.length;
    $('.quiz__question').textContent = q.q;
    var wrap = $('.quiz__opts'); wrap.innerHTML = '';
    shuffle(q.o).forEach(function (o) {
      var b = document.createElement('button');
      b.type = 'button'; b.className = 'quiz__opt'; b.textContent = o[0]; b.setAttribute('aria-pressed', 'false');
      b.addEventListener('click', function () {
        wrap.querySelectorAll('.quiz__opt').forEach(function (x) { x.setAttribute('aria-pressed', 'false'); });
        b.setAttribute('aria-pressed', 'true'); sel = o[1]; next.disabled = false;
      });
      wrap.appendChild(b);
    });
    next.disabled = true;
    next.firstChild.nodeValue = (cur === Q.length - 1 ? 'Ver resultado' : 'Siguiente') + ' ';
  }
  function decide() {
    var max = 0; ties = [];
    Object.keys(scores).forEach(function (k) {
      if (scores[k] > max) { max = scores[k]; win = k; ties = [k]; } else if (scores[k] === max) { ties.push(k); }
    });
  }
  opener.addEventListener('click', function (e) {
    e.preventDefault();
    var open = opener.getAttribute('aria-expanded') === 'true';
    opener.setAttribute('aria-expanded', open ? 'false' : 'true');
    box.hidden = open;
    if (!open) { reset(); show('intro', $('[data-quiz="start"]')); }
  });
  $('[data-quiz="start"]').addEventListener('click', function () { reset(); question(); show('quiz', $('.quiz__opt')); });
  $('[data-quiz="next"]').addEventListener('click', function () {
    if (!sel) return;
    scores[sel]++; cur++;
    if (cur < Q.length) { question(); $('.quiz__opt').focus(); return; }
    decide();
    $('[data-quiz="gate-name"]').textContent = P[win].name;
    show('gate', $('[data-quiz="gate-name"]'));
  });
  var gate = $('.quiz__gate');
  gate.addEventListener('submit', function (e) {
    e.preventDefault();
    var n = gate.nombre.value.trim(), m = gate.correo.value.trim(), c = gate.empresa.value.trim(), err = $('.quiz__err');
    if (!n || !m || !c) { err.textContent = 'Completa los tres campos para ver tu resultado.'; return; }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(m)) { err.textContent = 'Ingresa un correo válido.'; gate.correo.focus(); return; }
    err.textContent = '';
    if (TEST_ENDPOINT) {
      /* Integración pendiente: enviar {nombre, correo, empresa, arquetipo, puntajes} a TEST_ENDPOINT. */
    }
    var p = P[win];
    $('[data-quiz="result-name"]').textContent = p.name;
    $('[data-quiz="pct"]').textContent = p.pct + ' de los directivos evaluados en el Ranking 2026 tiene este perfil.';
    var mix = $('[data-quiz="mix"]');
    mix.hidden = ties.length < 2;
    mix.textContent = ties.length > 1 ? 'Perfil mixto: ' + ties.map(function (t) { return P[t].name; }).join(' + ') : '';
    $('[data-quiz="desc"]').textContent = p.desc;
    $('[data-quiz="risk"]').textContent = p.risk;
    $('[data-quiz="ex"]').textContent = p.ex;
    show('result', $('[data-quiz="result-name"]'));
  });
  $('[data-quiz="retry"]').addEventListener('click', function () { gate.reset(); reset(); show('intro', $('[data-quiz="start"]')); });
})();
</script>
