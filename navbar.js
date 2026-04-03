// FinPath – shared navbar component
(function () {
  const NAV_HTML = `
  <nav class="navbar" id="main-nav">
    <a class="navbar-brand" href="dashboard.html" style="text-decoration:none;">
      Fin<span class="dot" style="color:#2ecc8e;">Path</span>
    </a>
    <ul class="navbar-nav">
      <li>
        <a href="dashboard.html" id="nav-home">
          <svg width="15" height="15" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <rect x="3" y="3" width="7" height="7" rx="1"/>
            <rect x="14" y="3" width="7" height="7" rx="1"/>
            <rect x="3" y="14" width="7" height="7" rx="1"/>
            <rect x="14" y="14" width="7" height="7" rx="1"/>
          </svg>
          Home
        </a>
      </li>
      <li>
        <a href="learn.html" id="nav-learn">
          <svg width="15" height="15" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
          </svg>
          Learn
        </a>
      </li>
      <li>
        <a href="coach.html" id="nav-coach">
          <svg width="15" height="15" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
          </svg>
          Coach
        </a>
      </li>
      <li>
        <a href="leaderboard.html" id="nav-lb">
          <svg width="15" height="15" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path d="M18 20V10M12 20V4M6 20v-6"/>
          </svg>
          Leaderboard
        </a>
      </li>
      <li>
        <a href="profile.html" id="nav-profile">
          <svg width="15" height="15" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
            <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
            <circle cx="12" cy="7" r="4"/>
          </svg>
          Profile
        </a>
      </li>
    </ul>
    <div class="navbar-right">
      <div class="xp-badge" id="nav-xp">0 XP</div>
      <a href="profile.html" style="text-decoration:none;">
        <div class="avatar" id="nav-avatar" title="Profile">?</div>
      </a>
    </div>
    <!-- Mobile hamburger -->
    <button class="nav-hamburger" id="nav-hamburger" onclick="toggleMobileNav()" aria-label="Menu">
      <span></span><span></span><span></span>
    </button>
  </nav>
  <!-- Mobile menu -->
  <div class="nav-mobile-menu" id="nav-mobile-menu">
    <a href="dashboard.html">Home</a>
    <a href="learn.html">Learn</a>
    <a href="coach.html">Coach</a>
    <a href="leaderboard.html">Leaderboard</a>
    <a href="profile.html">Profile</a>
  </div>
  <style>
    .navbar {
      position: sticky;
      top: 0;
      z-index: 100;
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 2.5rem;
      height: 68px;
      background: rgba(10, 22, 40, 0.92);
      backdrop-filter: blur(12px);
      border-bottom: 1px solid rgba(255,255,255,0.08);
      box-shadow: 0 2px 20px rgba(0,0,0,0.3);
    }
    .navbar-brand {
      font-size: 1.45rem;
      font-weight: 800;
      color: #fff;
      letter-spacing: -.02em;
      white-space: nowrap;
    }
    .navbar-nav {
      display: flex;
      align-items: center;
      gap: .25rem;
      list-style: none;
      margin: 0;
      padding: 0;
    }
    .navbar-nav a {
      display: flex;
      align-items: center;
      gap: .45rem;
      padding: .5rem 1rem;
      border-radius: 9px;
      font-size: .9rem;
      font-weight: 500;
      color: rgba(255,255,255,0.6);
      text-decoration: none;
      transition: .15s;
      white-space: nowrap;
    }
    .navbar-nav a:hover {
      background: rgba(255,255,255,0.08);
      color: #fff;
    }
    .navbar-nav a.active {
      background: rgba(46,204,142,0.15);
      color: #2ecc8e;
      font-weight: 700;
    }
    .navbar-right {
      display: flex;
      align-items: center;
      gap: .85rem;
    }
    .xp-badge {
      display: flex;
      align-items: center;
      gap: .3rem;
      background: rgba(245,166,35,0.15);
      border: 1px solid rgba(245,166,35,0.3);
      color: #f5c06a;
      padding: .35rem .85rem;
      border-radius: 100px;
      font-size: .82rem;
      font-weight: 700;
      white-space: nowrap;
    }
    .avatar {
      width: 38px;
      height: 38px;
      border-radius: 50%;
      background: linear-gradient(135deg, #2ecc8e, #0f1f3d);
      display: flex;
      align-items: center;
      justify-content: center;
      color: #fff;
      font-weight: 700;
      font-size: .9rem;
      cursor: pointer;
      border: 2px solid rgba(46,204,142,0.3);
      transition: .15s;
    }
    .avatar:hover { border-color: #2ecc8e; }

    /* Hamburger */
    .nav-hamburger {
      display: none;
      flex-direction: column;
      gap: 5px;
      background: none;
      border: none;
      cursor: pointer;
      padding: .5rem;
    }
    .nav-hamburger span {
      display: block;
      width: 24px;
      height: 2px;
      background: rgba(255,255,255,0.8);
      border-radius: 2px;
      transition: .2s;
    }

    /* Mobile menu */
    .nav-mobile-menu {
      display: none;
      flex-direction: column;
      background: rgba(10,22,40,0.97);
      border-bottom: 1px solid rgba(255,255,255,0.08);
      position: sticky;
      top: 68px;
      z-index: 99;
    }
    .nav-mobile-menu a {
      padding: 1rem 2rem;
      color: rgba(255,255,255,0.75);
      text-decoration: none;
      font-size: .95rem;
      font-weight: 500;
      border-bottom: 1px solid rgba(255,255,255,0.05);
      transition: .15s;
    }
    .nav-mobile-menu a:hover {
      background: rgba(255,255,255,0.05);
      color: #fff;
    }
    .nav-mobile-menu.open { display: flex; }

    /* Responsive */
    @media (max-width: 768px) {
      .navbar { padding: 0 1.25rem; height: 60px; }
      .navbar-nav { display: none; }
      .navbar-right { display: none; }
      .nav-hamburger { display: flex; }
    }

    @media (min-width: 769px) and (max-width: 1024px) {
      .navbar { padding: 0 1.5rem; }
      .navbar-nav a { padding: .5rem .7rem; font-size: .84rem; }
      .xp-badge { font-size: .76rem; padding: .3rem .65rem; }
    }
  </style>`;

  const PAGE_NAV_MAP = {
    'dashboard.html':   'nav-home',
    'learn.html':       'nav-learn',
    'lesson.html':      'nav-learn',
    'coach.html':       'nav-coach',
    'leaderboard.html': 'nav-lb',
    'profile.html':     'nav-profile',
  };

  document.addEventListener('DOMContentLoaded', function () {
    const root = document.getElementById('nav-root');
    if (!root) return;

    root.innerHTML = NAV_HTML;

    // Highlight active page
    const page = window.location.pathname.split('/').pop() || 'dashboard.html';
    const activeId = PAGE_NAV_MAP[page];
    if (activeId) {
      const el = document.getElementById(activeId);
      if (el) el.classList.add('active');
    }

    // Load real user data
    const token = localStorage.getItem('fp_token');
    if (!token) return;

    Promise.all([
      fetch('https://project-finpath-production.up.railway.app/auth/me', {
        headers: { 'Authorization': 'Bearer ' + token }
      }).then(r => r.ok ? r.json() : null),
      fetch('https://project-finpath-production.up.railway.app/progress/overview', {
        headers: { 'Authorization': 'Bearer ' + token }
      }).then(r => r.ok ? r.json() : null),
    ]).then(([me, progress]) => {
      if (me) {
        const initial = (me.username || 'U')[0].toUpperCase();
        document.getElementById('nav-avatar').textContent = initial;
        document.getElementById('nav-avatar').title = me.username;
      }
      if (progress) {
        const xp = progress.completed_lessons * 20;
        document.getElementById('nav-xp').textContent = xp + ' XP';
      }
    }).catch(() => {});
  });

  // Mobile menu toggle
  window.toggleMobileNav = function() {
    const menu = document.getElementById('nav-mobile-menu');
    if (menu) menu.classList.toggle('open');
  };

  // Close mobile menu when clicking outside
  document.addEventListener('click', function(e) {
    const menu = document.getElementById('nav-mobile-menu');
    const hamburger = document.getElementById('nav-hamburger');
    if (menu && hamburger && !menu.contains(e.target) && !hamburger.contains(e.target)) {
      menu.classList.remove('open');
    }
  });
})();