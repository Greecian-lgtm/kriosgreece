/* KRIOS accessible mobile menu: button toggles the site links; Escape closes and returns focus. */
(function () {
  var btn = document.querySelector('[data-menu-btn]');
  if (!btn) return;
  var menu = document.getElementById(btn.getAttribute('aria-controls'));
  if (!menu) return;
  function set(open, focusBack) {
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    menu.classList.toggle('open', open);
    if (open) { var first = menu.querySelector('a'); if (first) first.focus(); }
    else if (focusBack) btn.focus();
  }
  btn.addEventListener('click', function () { set(btn.getAttribute('aria-expanded') !== 'true', false); });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape' && btn.getAttribute('aria-expanded') === 'true') set(false, true);
  });
  document.addEventListener('click', function (e) {
    if (btn.getAttribute('aria-expanded') === 'true' && !menu.contains(e.target) && !btn.contains(e.target)) set(false, false);
  });
  menu.addEventListener('focusout', function (e) {
    if (btn.getAttribute('aria-expanded') === 'true' && e.relatedTarget && !menu.contains(e.relatedTarget) && e.relatedTarget !== btn) set(false, false);
  });
  window.matchMedia('(min-width: 861px)').addEventListener('change', function (m) { if (m.matches) set(false, false); });
})();
/* Site-wide language layer (English, Greek, Spanish); loads once on every page that has the menu script. */
(function () { if (document.querySelector('script[src="/assets/site-i18n.js"]')) return; var sc = document.createElement("script"); sc.src = "/assets/site-i18n.js"; sc.defer = true; document.head.appendChild(sc); })();
