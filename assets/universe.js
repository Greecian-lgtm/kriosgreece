/* KRIOS Universe prototype: Memory Room question picker. No network, no storage, nothing typed is kept. */
(function () {
  var list = document.querySelector('.u-qs');
  if (!list) return;
  var items = [].slice.call(list.children);
  var i = 0, status = document.getElementById('u-status');
  function show(n, announce) {
    items.forEach(function (li, k) {
      li.classList.toggle('is-on', k === n);
      if (k === n) { li.classList.remove('u-fade'); void li.offsetWidth; li.classList.add('u-fade'); }
    });
    if (announce && status) status.textContent = 'Question ' + (n + 1) + ' of ' + items.length;
  }
  show(0, false);
  var next = document.getElementById('u-next'), copy = document.getElementById('u-copy');
  if (next) next.addEventListener('click', function () { i = (i + 1) % items.length; show(i, true); });
  if (copy) copy.addEventListener('click', function () {
    var t = items[i].querySelector('.u-q-text').textContent.trim();
    function ok() { if (status) status.textContent = 'Question copied.'; }
    function fallback() {
      var r = document.createRange(); r.selectNodeContents(items[i].querySelector('.u-q-text'));
      var s = window.getSelection(); s.removeAllRanges(); s.addRange(r);
      if (status) status.textContent = 'Question selected. Copy it with your keyboard.';
    }
    if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(t).then(ok, fallback); else fallback();
  });
})();
