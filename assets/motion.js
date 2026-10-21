/* KRIOS motion layer (draft). Adds decorative SVG only; never changes text, links or the order of content.
   Skips animation when the visitor prefers reduced motion; decorations then appear in their final state. */
(function () {
  var NS = 'http://www.w3.org/2000/svg';
  var reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
  var canObserve = 'IntersectionObserver' in window;
  var animate = !reduce && canObserve;
  if (animate) document.documentElement.classList.add('mo-on');

  function el(name, attrs, parent) {
    var n = document.createElementNS(NS, name);
    for (var k in attrs) n.setAttribute(k, attrs[k]);
    if (parent) parent.appendChild(n);
    return n;
  }
  function svg(cls, vb) {
    var s = el('svg', { 'class': cls, viewBox: vb, 'aria-hidden': 'true', focusable: 'false' });
    return s;
  }

  /* 70 Topographic Survey: nested wavy contours, built from fixed sinusoids so every page looks the same */
  function topo(host) {
    var s = svg('mo-topo', '0 0 1000 400'); s.setAttribute('preserveAspectRatio', 'xMidYMid slice');
    var g = el('g', {}, s), cx = 700, cy = 200;
    for (var k = 1; k <= 11; k++) {
      var r = 28 * k, d = '';
      for (var i = 0; i <= 96; i++) {
        var t = i / 96 * 2 * Math.PI;
        var rr = r * (1 + 0.14 * Math.sin(2 * t + k * 0.35) + 0.08 * Math.sin(3 * t + 1.2) + 0.04 * Math.sin(5 * t + k * 0.2));
        d += (i ? 'L' : 'M') + (cx + rr * 1.9 * Math.cos(t)).toFixed(1) + ' ' + (cy + rr * Math.sin(t)).toFixed(1);
      }
      el('path', { d: d + 'Z' }, g);
    }
    var stars = el('g', { 'class': 'mo-stars' }, s);
    [[120,70],[340,120],[520,70],[690,40],[830,110],[960,60],[300,230],[560,200],[880,210]].forEach(function (p, k) {
      var c = el('circle', { cx: p[0], cy: p[1], r: k % 3 === 0 ? 3 : 2.2 }, stars); c.setAttribute('style', '--k:' + k);
    });
    var glow = document.createElement('div'); glow.className = 'mo-glow'; glow.setAttribute('aria-hidden', 'true');
    host.insertBefore(glow, host.firstChild);
    host.classList.add('mo-host');
    host.insertBefore(s, host.firstChild);
  }

  /* 10 Illuminated Manuscript: a small gold flourish under section headings */
  function rule(h2, center) {
    var s = svg('mo-rule' + (center ? ' mo-center' : ''), '0 0 150 18');
    el('line', { x1: 4, y1: 9, x2: 62, y2: 9, pathLength: 1 }, s);
    el('line', { x1: 88, y1: 9, x2: 146, y2: 9, pathLength: 1 }, s);
    el('path', { d: 'M62 9 C66 3 70 3 72 9 M88 9 C84 3 80 3 78 9', pathLength: 1 }, s);
    el('path', { 'class': 'mo-gem', d: 'M75 3 L80 9 L75 15 L70 9 Z' }, s);
    h2.parentNode.insertBefore(s, h2.nextSibling);
    return s;
  }

  /* 57 Cross-Stitch Sampler: running stitch with a cross every so often */
  function stitch(before) {
    var s = svg('mo-stitch', '0 0 520 22');
    el('line', { x1: 2, y1: 11, x2: 518, y2: 11 }, s);
    for (var x = 40; x < 520; x += 96) {
      el('path', { 'class': 'mo-x', d: 'M' + (x - 5) + ' 6 L' + (x + 5) + ' 16 M' + (x + 5) + ' 6 L' + (x - 5) + ' 16' }, s);
    }
    before.parentNode.insertBefore(s, before);
    return s;
  }

  var targets = [];
  var sacred = location.pathname.indexOf('/sacred-days') === 0;   /* devotional pages: no manuscript or stitch ornament */
  var rules = 0;
  [].forEach.call(document.querySelectorAll('.hero, .m-sdhero, .m-filmhero'), topo);

  [].forEach.call(document.querySelectorAll('main h2'), function (h) {
    if (sacred) return;
    if (h.closest('.hero, .m-sdhero, .m-filmhero, .m-card, .m-feat, .m-read, .m-src')) return;
    if (h.closest('.ask')) { targets.push(stitch(h)); return; }                    // closing "Who taught you yours?": the one stitched divider
    if (h.closest('#family') || rules >= 2) return;                                // at most two flourishes per page
    rules++;
    targets.push(rule(h, !!h.closest('.m-begin') && getComputedStyle(h).textAlign === 'center'));
  });
  var sp = document.querySelector('#story > p');
  if (sp && !sacred && /^[A-Za-z]/.test(sp.textContent.trim())) sp.classList.add('mo-dropcap');

  [].forEach.call(document.querySelectorAll('[data-mo]'), function (n) { targets.push(n); });

  if (!animate) { targets.forEach(function (t) { t.classList.add('mo-in'); }); return; }
  var io = new IntersectionObserver(function (es) {
    es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('mo-in'); io.unobserve(e.target); } });
  }, { rootMargin: '0px 0px -10% 0px', threshold: 0.2 });
  targets.forEach(function (t) { io.observe(t); });
})();
