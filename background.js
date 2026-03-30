(function() {
  var style = document.createElement('style');
  style.textContent = '.bg-canvas{position:fixed;inset:0;z-index:0;background:linear-gradient(135deg,#0a1628 0%,#0f2d1f 50%,#0a1628 100%);background-size:400% 400%;animation:bgShift 12s ease infinite;}@keyframes bgShift{0%{background-position:0% 50%}50%{background-position:100% 50%}100%{background-position:0% 50%}}.fp-orb{position:fixed;border-radius:50%;filter:blur(80px);z-index:0;pointer-events:none;}.fp-orb-1{width:500px;height:500px;background:#2ecc8e;opacity:.12;top:-200px;left:-100px;}.fp-orb-2{width:400px;height:400px;background:#3b82f6;opacity:.1;bottom:-150px;right:-100px;}.fp-orb-3{width:300px;height:300px;background:#a78bfa;opacity:.1;top:50%;left:40%;}.fp-p{position:fixed;pointer-events:none;z-index:0;font-size:1rem;animation:fpFloat linear infinite;}@keyframes fpFloat{0%{transform:translateY(110vh);opacity:0;}15%{opacity:0.12;}85%{opacity:0.12;}100%{transform:translateY(-150px);opacity:0;}}';
  document.head.appendChild(style);

  var bg = document.createElement('div');
  bg.className = 'bg-canvas';
  document.body.appendChild(bg);

  [1,2,3].forEach(function(n) {
    var o = document.createElement('div');
    o.className = 'fp-orb fp-orb-' + n;
    document.body.appendChild(o);
  });

  var E = ['💳','💰','📊','🏦','📈','💎','🎯','⚡','🔥','🏆','📱','💡'];
  for (var i = 0; i < 15; i++) {
    var el = document.createElement('div');
    el.className = 'fp-p';
    el.textContent = E[Math.floor(Math.random() * E.length)];
    var dur = Math.random() * 10 + 8;
    var delay = -(Math.random() * dur);
    el.style.left = Math.random() * 100 + 'vw';
    el.style.fontSize = (Math.random() * 0.8 + 0.8) + 'rem';
    el.style.animationDuration = dur + 's';
    el.style.animationDelay = delay + 's';
    document.body.appendChild(el);
  }
})();
