// FinPath Gamification System
// Add <script src="gamification.js"></script> to every page

// ── Level System ──────────────────────────────────────────
const LEVELS = [
    { name: 'Beginner',  min: 0,    icon: '🥉', color: '#cd7f32' },
    { name: 'Bronze',    min: 100,  icon: '🥉', color: '#cd7f32' },
    { name: 'Silver',    min: 300,  icon: '🥈', color: '#8d9db5' },
    { name: 'Gold',      min: 600,  icon: '🥇', color: '#f5a623' },
    { name: 'Platinum',  min: 1000, icon: '💎', color: '#a78bfa' },
    { name: 'Diamond',   min: 2000, icon: '👑', color: '#2ecc8e' },
  ];
  
  function getLevel(xp) {
    let current = LEVELS[0];
    for (const level of LEVELS) {
      if (xp >= level.min) current = level;
      else break;
    }
    const idx = LEVELS.indexOf(current);
    const next = LEVELS[idx + 1] || null;
    const progress = next
      ? ((xp - current.min) / (next.min - current.min)) * 100
      : 100;
    return { current, next, progress: Math.round(progress), xp };
  }
  
  // ── XP Animation ──────────────────────────────────────────
  function showXPAnimation(amount, x, y) {
    const el = document.createElement('div');
    el.textContent = '+' + amount + ' XP';
    Object.assign(el.style, {
      position: 'fixed',
      left: (x || window.innerWidth / 2) + 'px',
      top: (y || window.innerHeight / 2) + 'px',
      transform: 'translate(-50%, -50%)',
      background: 'var(--green)',
      color: '#fff',
      padding: '.5rem 1.25rem',
      borderRadius: '100px',
      fontWeight: '800',
      fontSize: '1.2rem',
      zIndex: '99999',
      pointerEvents: 'none',
      transition: 'all 1s ease-out',
      opacity: '1',
    });
    document.body.appendChild(el);
    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        el.style.transform = 'translate(-50%, -200%)';
        el.style.opacity = '0';
      });
    });
    setTimeout(() => el.remove(), 1000);
  }
  
  // ── Badge Unlock Popup ────────────────────────────────────
  const BADGE_META = {
    FIRST_LESSON:          { icon: '🎯', label: 'First Steps',    desc: 'You completed your first lesson!' },
    FIRST_QUIZ:            { icon: '📝', label: 'Quiz Taker',     desc: 'You completed your first quiz!' },
    STREAK_3:              { icon: '🔥', label: 'On Fire!',       desc: 'You maintained a 3-day streak!' },
    STREAK_7:              { icon: '⚡', label: 'Week Warrior',   desc: 'You maintained a 7-day streak!' },
    SCORE_80:              { icon: '🏆', label: 'High Scorer',    desc: 'You scored 80%+ on a quiz!' },
    COMPLETE_FIRST_MODULE: { icon: '🎓', label: 'Module Master',  desc: 'You completed your first module!' },
  };
  
  function showBadgeUnlock(badgeType) {
    const meta = BADGE_META[badgeType] || { icon: '🏅', label: badgeType, desc: 'Badge unlocked!' };
  
    const overlay = document.createElement('div');
    Object.assign(overlay.style, {
      position: 'fixed', inset: '0',
      background: 'rgba(0,0,0,0.5)',
      zIndex: '999999',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      animation: 'fadeIn .3s ease',
    });
  
    overlay.innerHTML = `
      <div style="background:#fff;border-radius:24px;padding:3rem 2.5rem;text-align:center;
        max-width:340px;width:90%;box-shadow:0 20px 60px rgba(0,0,0,.2);
        animation:popIn .4s cubic-bezier(0.34,1.56,0.64,1);">
        <div style="font-size:4rem;margin-bottom:1rem;animation:spin .5s ease">${meta.icon}</div>
        <div style="font-size:.8rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;
          color:var(--green);margin-bottom:.5rem;">Badge Unlocked!</div>
        <div style="font-size:1.5rem;font-weight:800;color:var(--navy);margin-bottom:.5rem;">${meta.label}</div>
        <div style="font-size:.9rem;color:var(--muted);margin-bottom:2rem;">${meta.desc}</div>
        <button onclick="this.closest('[data-overlay]').remove()"
          style="background:var(--green);color:#fff;border:none;padding:.75rem 2rem;
            border-radius:12px;font-weight:700;font-size:.95rem;cursor:pointer;width:100%;">
          Awesome! 🎉
        </button>
      </div>`;
  
    overlay.setAttribute('data-overlay', '');
    overlay.addEventListener('click', function(e) {
      if (e.target === overlay) overlay.remove();
    });
  
    document.body.appendChild(overlay);
  
    // Auto close after 5 seconds
    setTimeout(() => { if (overlay.parentNode) overlay.remove(); }, 5000);
  }
  
  // ── Module Completion Confetti ────────────────────────────
  function showConfetti() {
    const colors = ['#2ecc8e', '#f5a623', '#a78bfa', '#f97316', '#3b82f6', '#ec4899'];
    const container = document.createElement('div');
    Object.assign(container.style, {
      position: 'fixed', inset: '0',
      pointerEvents: 'none',
      zIndex: '999998',
      overflow: 'hidden',
    });
    document.body.appendChild(container);
  
    for (let i = 0; i < 80; i++) {
      const piece = document.createElement('div');
      const color = colors[Math.floor(Math.random() * colors.length)];
      const size = Math.random() * 10 + 6;
      const left = Math.random() * 100;
      const delay = Math.random() * 0.8;
      const duration = Math.random() * 2 + 2;
      const rotate = Math.random() * 720;
  
      Object.assign(piece.style, {
        position: 'absolute',
        width: size + 'px',
        height: size + 'px',
        background: color,
        borderRadius: Math.random() > 0.5 ? '50%' : '2px',
        left: left + '%',
        top: '-20px',
        animation: `confettiFall ${duration}s ${delay}s ease-in forwards`,
      });
      container.appendChild(piece);
    }
  
    setTimeout(() => container.remove(), 4000);
  }
  
  // ── Module Completion Celebration ─────────────────────────
  function showModuleComplete(moduleName) {
    showConfetti();
  
    setTimeout(() => {
      const overlay = document.createElement('div');
      Object.assign(overlay.style, {
        position: 'fixed', inset: '0',
        background: 'rgba(0,0,0,0.5)',
        zIndex: '999999',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
      });
  
      overlay.innerHTML = `
        <div style="background:#fff;border-radius:24px;padding:3rem 2.5rem;text-align:center;
          max-width:360px;width:90%;box-shadow:0 20px 60px rgba(0,0,0,.2);
          animation:popIn .4s cubic-bezier(0.34,1.56,0.64,1);">
          <div style="font-size:4rem;margin-bottom:1rem;">🎓</div>
          <div style="font-size:.8rem;font-weight:700;text-transform:uppercase;letter-spacing:.1em;
            color:var(--green);margin-bottom:.5rem;">Module Complete!</div>
          <div style="font-size:1.4rem;font-weight:800;color:var(--navy);margin-bottom:.5rem;">${moduleName}</div>
          <div style="font-size:.9rem;color:var(--muted);margin-bottom:.5rem;">You've finished all lessons!</div>
          <div style="font-size:1.1rem;font-weight:700;color:var(--green);margin-bottom:2rem;">+100 Bonus XP 🎉</div>
          <div style="display:flex;gap:.75rem;">
            <button onclick="window.location.href='learn.html'"
              style="flex:1;background:var(--bg);color:var(--navy);border:1px solid var(--border);
                padding:.75rem;border-radius:12px;font-weight:700;cursor:pointer;">
              Next Module
            </button>
            <button onclick="this.closest('[data-overlay]').remove()"
              style="flex:1;background:var(--green);color:#fff;border:none;
                padding:.75rem;border-radius:12px;font-weight:700;cursor:pointer;">
              Keep Going!
            </button>
          </div>
        </div>`;
  
      overlay.setAttribute('data-overlay', '');
      overlay.addEventListener('click', function(e) {
        if (e.target === overlay) overlay.remove();
      });
      document.body.appendChild(overlay);
    }, 800);
  }
  
  // ── Daily XP Goal Tracker ─────────────────────────────────
  const DAILY_GOAL = 60; // XP per day
  
  function getDailyXP() {
    const today = new Date().toDateString();
    const stored = JSON.parse(localStorage.getItem('fp_daily_xp') || '{}');
    if (stored.date !== today) return 0;
    return stored.xp || 0;
  }
  
  function addDailyXP(amount) {
    const today = new Date().toDateString();
    const stored = JSON.parse(localStorage.getItem('fp_daily_xp') || '{}');
    const current = stored.date === today ? (stored.xp || 0) : 0;
    const newXP = current + amount;
    localStorage.setItem('fp_daily_xp', JSON.stringify({ date: today, xp: newXP }));
  
    // Check if goal reached
    if (current < DAILY_GOAL && newXP >= DAILY_GOAL) {
      showDailyGoalComplete();
    }
    return newXP;
  }
  
  function showDailyGoalComplete() {
    const toast = document.createElement('div');
    toast.innerHTML = '🎯 Daily goal reached! Amazing work!';
    Object.assign(toast.style, {
      position: 'fixed',
      bottom: '5rem',
      left: '50%',
      transform: 'translateX(-50%)',
      background: 'linear-gradient(135deg, var(--green), #059473)',
      color: '#fff',
      padding: '1rem 2rem',
      borderRadius: '100px',
      fontWeight: '700',
      fontSize: '1rem',
      zIndex: '99999',
      boxShadow: '0 4px 20px rgba(46,204,142,.4)',
      whiteSpace: 'nowrap',
      animation: 'slideUp .3s ease',
    });
    document.body.appendChild(toast);
    setTimeout(() => { toast.style.opacity = '0'; toast.style.transition = 'opacity .4s'; }, 3000);
    setTimeout(() => toast.remove(), 3400);
  }
  
  function renderDailyGoalWidget(containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;
  
    const dailyXP = getDailyXP();
    const pct = Math.min(Math.round((dailyXP / DAILY_GOAL) * 100), 100);
    const done = dailyXP >= DAILY_GOAL;
  
    container.innerHTML = `
      <div class="card" style="margin-bottom:1rem;">
        <div class="card-title" style="display:flex;justify-content:space-between;align-items:center;">
          <span>Daily Goal</span>
          <span style="color:${done ? 'var(--green)' : 'var(--muted)'};">${done ? '✓ Complete!' : dailyXP + ' / ' + DAILY_GOAL + ' XP'}</span>
        </div>
        <div style="margin-bottom:.5rem;">
          <div class="progress-bar-wrap">
            <div class="progress-bar-fill" style="width:${pct}%;background:${done ? 'var(--green)' : 'linear-gradient(90deg,var(--green),#f5a623)'}"></div>
          </div>
        </div>
        <div style="font-size:.8rem;color:var(--muted);">
          ${done ? 'You hit your daily goal! Come back tomorrow.' : 'Complete lessons to reach your ' + DAILY_GOAL + ' XP daily goal'}
        </div>
      </div>`;
  }
  
  // ── Level Badge Widget ────────────────────────────────────
  function renderLevelWidget(xp, containerId) {
    const container = document.getElementById(containerId);
    if (!container) return;
  
    const level = getLevel(xp);
  
    container.innerHTML = `
      <div class="card" style="margin-bottom:1rem;">
        <div class="card-title">Your Level</div>
        <div style="display:flex;align-items:center;gap:1rem;margin-bottom:1rem;">
          <div style="font-size:2.5rem;">${level.current.icon}</div>
          <div>
            <div style="font-size:1.1rem;font-weight:800;color:${level.current.color};">${level.current.name}</div>
            <div style="font-size:.8rem;color:var(--muted);">${xp} XP total</div>
          </div>
        </div>
        ${level.next ? `
          <div>
            <div style="display:flex;justify-content:space-between;font-size:.78rem;margin-bottom:.4rem;">
              <span style="color:var(--muted);">Progress to ${level.next.name} ${level.next.icon}</span>
              <span style="font-weight:700;color:${level.current.color};">${level.progress}%</span>
            </div>
            <div class="progress-bar-wrap">
              <div class="progress-bar-fill" style="width:${level.progress}%;background:${level.current.color}"></div>
            </div>
            <div style="font-size:.75rem;color:var(--muted);margin-top:.3rem;">
              ${level.next.min - xp} XP to ${level.next.name}
            </div>
          </div>` : `<div style="font-size:.85rem;color:var(--green);font-weight:700;">Maximum level reached! 👑</div>`}
      </div>`;
  }
  
  // ── CSS Animations ────────────────────────────────────────
  const style = document.createElement('style');
  style.textContent = `
    @keyframes fadeIn { from { opacity:0 } to { opacity:1 } }
    @keyframes popIn {
      from { transform: scale(0.5); opacity: 0; }
      to   { transform: scale(1);   opacity: 1; }
    }
    @keyframes spin {
      from { transform: rotate(-20deg) scale(0.5); }
      to   { transform: rotate(10deg)  scale(1); }
    }
    @keyframes confettiFall {
      0%   { transform: translateY(0) rotate(0deg); opacity: 1; }
      100% { transform: translateY(100vh) rotate(720deg); opacity: 0; }
    }
    @keyframes slideUp {
      from { transform: translateX(-50%) translateY(20px); opacity: 0; }
      to   { transform: translateX(-50%) translateY(0); opacity: 1; }
    }
  `;
  document.head.appendChild(style);
  
  // ── Global helpers used by lesson.html ────────────────────
  window.FinPathGamification = {
    showXPAnimation,
    showBadgeUnlock,
    showModuleComplete,
    showConfetti,
    addDailyXP,
    getDailyXP,
    renderDailyGoalWidget,
    renderLevelWidget,
    getLevel,
    DAILY_GOAL,
  };