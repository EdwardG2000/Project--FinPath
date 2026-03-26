// FinPath – shared navbar component
// Injected into every page via <div id="nav-root"></div>

(function () {
  const NAV_HTML = `
  <nav class="navbar" id="main-nav">
    <a class="navbar-brand" href="dashboard.html">
      Fin<span class="dot">Path</span>
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
      <div class="xp-badge">⚡ 340 XP</div>
      <button class="lang-btn">🌐 EN ▾</button>
      <a href="profile.html"><div class="avatar" title="Eddie">E</div></a>
    </div>
  </nav>`;

  // Page → nav link ID map
  const PAGE_NAV_MAP = {
    'dashboard.html': 'nav-home',
    'learn.html':     'nav-learn',
    'lesson.html':    'nav-learn',
    'coach.html':     'nav-coach',
    'leaderboard.html': 'nav-lb',
    'profile.html':   'nav-profile',
  };

  document.addEventListener('DOMContentLoaded', function () {
    const root = document.getElementById('nav-root');
    if (!root) return;

    root.innerHTML = NAV_HTML;

    // Highlight the active nav link
    const page = window.location.pathname.split('/').pop() || 'index.html';
    const activeId = PAGE_NAV_MAP[page];
    if (activeId) {
      const el = document.getElementById(activeId);
      if (el) el.classList.add('active');
    }
  });
})();
