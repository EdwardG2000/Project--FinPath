(function() {
  var style = document.createElement('style');
  style.textContent = '.bg-canvas{position:fixed;inset:0;z-index:0;background:#0a1628;} .fp-orb{display:none;} .fp-p{display:none;}';
  document.head.appendChild(style);

  var bg = document.createElement('div');
  bg.className = 'bg-canvas';
  document.body.appendChild(bg);
})();
