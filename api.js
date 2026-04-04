const API = 'https://project-finpath-production.up.railway.app';

function getToken() { return localStorage.getItem('fp_token'); }
function saveToken(t) { localStorage.setItem('fp_token', t); }
function clearToken() { localStorage.removeItem('fp_token'); }

function requireAuth() {
  if (!getToken()) window.location.href = 'login.html';
}

async function apiFetch(path, options = {}) {
  const res = await fetch(API + path, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer ' + getToken(),
      ...(options.headers || {}),
    },
  });
  if (res.status === 401) { clearToken(); window.location.href = 'login.html'; return; }
  if (!res.ok) { const e = await res.json().catch(() => ({})); throw new Error(e.detail || 'Failed'); }
  if (res.status === 204 || res.headers.get('content-length') === '0') return null;
  return res.json().catch(() => null);
}

async function login(email, password) {
  const res = await fetch(API + '/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  });
  if (!res.ok) { const e = await res.json(); throw new Error(e.detail); }
  const data = await res.json();
  saveToken(data.access_token);
  return data;
}
async function getLeaderboard() { return apiFetch('/progress/leaderboard'); }
async function getMe()            { return apiFetch('/auth/me'); }
async function getProgress()      { return apiFetch('/progress/overview'); }
async function getModules()       { return apiFetch('/modules'); }
async function getModule(id)      { return apiFetch('/modules/' + id); }
async function getLessons(modId)  { return apiFetch('/lessons/module/' + modId); }
async function getLesson(id)      { return apiFetch('/lessons/' + id); }
async function completeLesson(id) { return apiFetch('/lessons/' + id + '/complete', { method: 'POST' }); }
async function getQuiz(modId)     { return apiFetch('/quiz/' + modId); }
async function submitQuiz(modId, answers) {
  return apiFetch('/quiz/' + modId + '/submit', {
    method: 'POST',
    body: JSON.stringify({ answers }),
  });
}
