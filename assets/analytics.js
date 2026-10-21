/* KRIOS analytics (draft). Google Analytics 4 loads only after the visitor chooses "Allow analytics".
   Nothing from Google is requested before that. Global Privacy Control and Do Not Track count as "No".
   Ad personalization and Google signals are off. The choice is kept in this browser only and can be changed from the footer. */
(function () {
  var ID = 'G-CR9SJHDTPB', KEY = 'krios_analytics';
  function get() { try { return localStorage.getItem(KEY); } catch (e) { return null; } }
  function set(v) { try { localStorage.setItem(KEY, v); } catch (e) {} }
  var gpc = navigator.globalPrivacyControl === true || navigator.doNotTrack === '1' || window.doNotTrack === '1';

  function load() {
    if (window.__kriosGa) return; window.__kriosGa = true;
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    gtag('consent', 'default', { analytics_storage: 'granted', ad_storage: 'denied', ad_user_data: 'denied', ad_personalization: 'denied' });
    gtag('js', new Date());
    gtag('config', ID, { allow_google_signals: false, allow_ad_personalization_signals: false });
    var s = document.createElement('script'); s.async = true; s.src = 'https://www.googletagmanager.com/gtag/js?id=' + ID;
    document.head.appendChild(s);
  }
  function stop() {
    window['ga-disable-' + ID] = true;
    try { document.cookie.split(';').forEach(function (c) { var n = c.split('=')[0].trim(); if (n.indexOf('_ga') === 0) document.cookie = n + '=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/;domain=' + location.hostname; }); } catch (e) {}
  }

  var box;
  function close() { if (box && box.parentNode) box.parentNode.removeChild(box); box = null; }
  function choose(v) { set(v); close(); if (v === 'granted') { window['ga-disable-' + ID] = false; load(); } else { stop(); } }
  function ask() {
    if (box) return;
    box = document.createElement('div'); box.className = 'kr-an'; box.setAttribute('role', 'region'); box.setAttribute('aria-label', 'Analytics choice');
    box.innerHTML = '<p>May we count visits with Google Analytics? It helps us see which pages families find useful. It stays off unless you say yes. <a href="/legal/#privacy">Details</a></p>' +
      '<div><button type="button" data-v="granted">Allow analytics</button><button type="button" data-v="denied">No thanks</button></div>';
    box.addEventListener('click', function (e) { var v = e.target && e.target.getAttribute && e.target.getAttribute('data-v'); if (v) choose(v); });
    document.body.appendChild(box);
  }

  var st = document.createElement('style');
  st.textContent = '.kr-an{position:fixed;left:12px;right:12px;bottom:12px;z-index:60;max-width:760px;margin:0 auto;background:#101a2e;color:#f5edd8;border:1px solid #c9a35e;border-radius:6px;padding:14px 16px;display:flex;gap:14px;flex-wrap:wrap;align-items:center;justify-content:space-between;box-shadow:0 12px 30px rgba(0,0,0,.35);font:17px/1.4 "EB Garamond",Georgia,serif}' +
    '.kr-an p{margin:0;flex:1 1 320px}.kr-an a{color:#e3c27e}.kr-an div{display:flex;gap:10px}' +
    '.kr-an button{min-height:44px;padding:8px 18px;border-radius:3px;border:1px solid #c9a35e;background:transparent;color:#f5edd8;font:inherit;font-weight:600;cursor:pointer}' +
    '.kr-an button:hover{background:#1c2d4d}.kr-an button:focus-visible{outline:3px solid #fff;outline-offset:2px}' +
    '.kr-an-link{background:none;border:0;padding:0;color:inherit;font:inherit;text-decoration:underline;cursor:pointer}';
  document.head.appendChild(st);

  function footerLink() {
    var f = document.querySelector('footer .wrap'); if (!f) return;
    var p = document.createElement('p'); p.style.cssText = 'grid-column:1/-1;margin:6px 0 0;font-size:.95rem';
    var b = document.createElement('button'); b.type = 'button'; b.className = 'kr-an-link'; b.textContent = 'Analytics choice';
    b.addEventListener('click', ask); p.appendChild(b); f.appendChild(p);
  }

  function init() {
    footerLink();
    var v = get();
    if (gpc) { stop(); return; }
    if (v === 'granted') load();
    else if (v === 'denied') stop();
    else ask();
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', init); else init();
})();
