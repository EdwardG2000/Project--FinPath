// FinPath - Shared animated background
// Add <script src="background.js"></script> to every page

(function() {
  // Inject background elements
  const bgCanvas = document.createElement('div');
  bgCanvas.className = 'bg-canvas';
  document.body.insertBefore(bgCanvas, document.body.firstChild);

  ['orb-1','orb-2','orb-3'].forEach(function(cls) {
    const orb = document.createElement('div');
    orb.className = 'orb ' + cls;
    document.body.insertBefore(orb, document.body.firstChild);
  });

  const particlesDiv = document.createElement('div');
  particlesDiv.className = 'particles';
  document.body.insertBefore(particlesDiv, document.body.firstChild);

  // Create floating particles
  const EMOJIS = ['💳','💰','📊','🏦','📈','💎','🎯','⚡','🔥','🏆','📱','💡'];
  for (let i = 0; i < 12; i++) {
    const el = document.createElement('div');
    el.className = 'particle';
    el.textContent = EMOJIS[Math.floor(Math.random() * EMOJIS.length)];
    el.style.left = Math.random() * 100 + 'vw';
    el.style.fontSize = (Math.random() * 1 + 0.7) + 'rem';
    const duration = Math.random() * 15 + 12;
    const delay = Math.random() * 10;
    el.style.animation = 'floatUp ' + duration + 's ' + delay + 's linear infinite';
    particlesDiv.appendChild(el);
  }
})();
