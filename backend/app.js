

const API = 'http://localhost:8000';

// ── Token helpers ──────────────────────────────────────────
function getToken() {
  return localStorage.getItem('fp_token');
}
function saveToken(token) {
  localStorage.setItem('fp_token', token);
}
function clearToken() {
  localStorage.removeItem('fp_token');
}
function isLoggedIn() {
  return !!getToken();
}
function requireAuth() {
  if (!isLoggedIn()) window.location.href = 'index.html';
}

// ── Core fetch wrapper ─────────────────────────────────────
async function apiFetch(path, options = {}) {
  const headers = { 'Content-Type': 'application/json' };
  if (getToken()) headers['Authorization'] = 'Bearer ' + getToken();
  const res = await fetch(API + path, { ...options, headers });
  if (res.status === 401) { clearToken(); window.location.href = 'index.html'; }
  if (!res.ok) throw await res.json();
  if (res.status === 204) return null;
  return res.json();
}

// ── Auth ───────────────────────────────────────────────────
async function login(email, password) {
  const data = await apiFetch('/auth/login', {
    method: 'POST',
    body: JSON.stringify({ email, password }),
  });
  saveToken(data.access_token);
  return data;
}
async function getMe() {
  return apiFetch('/auth/me');
}
function logout() {
  clearToken();
  window.location.href = 'index.html';
}

// ── Progress ───────────────────────────────────────────────
async function getProgress() {
  return apiFetch('/progress/overview');
}

// ── Modules ────────────────────────────────────────────────
async function getModules() {
  return apiFetch('/modules');
}
async function getModule(id) {
  return apiFetch('/modules/' + id);
}

// ── Lessons ────────────────────────────────────────────────
async function getModuleLessons(moduleId) {
  return apiFetch('/lessons/module/' + moduleId);
}
async function getLesson(id) {
  return apiFetch('/lessons/' + id);
}
async function completeLesson(id) {
  return apiFetch('/lessons/' + id + '/complete', { method: 'POST' });
}

// ── Quiz ───────────────────────────────────────────────────
async function getQuiz(moduleId) {
  return apiFetch('/quiz/' + moduleId);
}
async function submitQuiz(moduleId, answers) {
  return apiFetch('/quiz/' + moduleId + '/submit', {
    method: 'POST',
    body: JSON.stringify({ answers }),
  });
}

// ── AI Coach ───────────────────────────────────────────────
async function askCoach(message, conversationId) {
  return apiFetch('/ai/coach', {
    method: 'POST',
    body: JSON.stringify({ message, conversation_id: conversationId }),
  });
}