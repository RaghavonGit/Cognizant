import { courses } from './data.js';

const JSON_PLACEHOLDER = 'https://jsonplaceholder.typicode.com';

// ---------- Task 1: Promises and async/await ----------

// Promise-chain version
function fetchUserThen(id) {
  return fetch(`${JSON_PLACEHOLDER}/users/${id}`)
    .then((response) => response.json())
    .then((user) => {
      console.log('[.then] User name:', user.name);
      return user;
    });
}

// async/await version with try/catch
async function fetchUser(id) {
  try {
    const response = await fetch(`${JSON_PLACEHOLDER}/users/${id}`);
    const user = await response.json();
    console.log('[async/await] User name:', user.name);
    return user;
  } catch (error) {
    console.error('fetchUser failed:', error);
  }
}

// Simulated network delay returning local data
function fetchAllCourses() {
  return new Promise((resolve) => setTimeout(() => resolve(courses), 1000));
}

async function loadCourses() {
  const statusEl = document.querySelector('#courses-status');
  const grid = document.querySelector('.course-grid');

  statusEl.textContent = 'Loading courses...';
  const data = await fetchAllCourses();
  statusEl.textContent = '';

  grid.innerHTML = data
    .map(
      (course) => `
      <article class="course-card">
        <h3>${course.name}</h3>
        <p>${course.code}</p>
        <span>${course.credits} credits</span>
      </article>`
    )
    .join('');
}

// Promise.all() — two users fetched simultaneously
async function loadTwoUsers() {
  const [user1, user2] = await Promise.all([fetchUser(1), fetchUser(2)]);
  console.log('Promise.all both names:', user1.name, '&', user2.name);
}

loadCourses();
fetchUserThen(1);
loadTwoUsers();

// ---------- Task 2: Fetch API with error handling ----------

async function apiFetch(url) {
  const response = await fetch(url);
  if (!response.ok) {
    throw new Error(`Request to ${url} failed with status ${response.status}`);
  }
  return response.json();
}

async function loadNotifications(url = `${JSON_PLACEHOLDER}/posts`) {
  const statusEl = document.querySelector('#notif-status');
  const grid = document.querySelector('.notif-grid');
  const retryBtn = document.querySelector('#retry-btn');

  statusEl.className = 'status-msg';
  statusEl.innerHTML = '<div class="spinner"></div>Loading notifications...';
  retryBtn.classList.add('hidden');
  grid.innerHTML = '';

  try {
    const posts = await apiFetch(url);
    statusEl.textContent = '';
    grid.innerHTML = posts
      .slice(0, 6)
      .map(
        (post) => `
        <article class="notif-card">
          <h3>${post.title}</h3>
          <p>${post.body}</p>
        </article>`
      )
      .join('');
  } catch (error) {
    statusEl.className = 'status-msg error';
    statusEl.textContent = `Failed to load notifications: ${error.message}`;
    retryBtn.classList.remove('hidden');
    retryBtn.dataset.retryUrl = url;
  }
}

document.querySelector('#load-bad-url').addEventListener('click', () => {
  loadNotifications(`${JSON_PLACEHOLDER}/nonexistent`);
});

document.querySelector('#retry-btn').addEventListener('click', () => {
  // Retry hits the real endpoint so the user sees a successful recovery,
  // rather than repeating the same simulated bad URL forever.
  loadNotifications(`${JSON_PLACEHOLDER}/posts`);
});

loadNotifications();

// ---------- Task 3: Introduction to Axios ----------

// axios.interceptors.request.use() — logs every outgoing request
axios.interceptors.request.use((config) => {
  console.log(`API call started: ${config.url}`);
  return config;
});

async function apiFetchAxios(url, params = {}) {
  // Axios auto-parses JSON and throws on non-2xx by default — no response.ok check needed.
  const response = await axios.get(url, { params });
  return response.data;
}

async function loadAxiosDemo() {
  const statusEl = document.querySelector('#axios-status');
  const grid = document.querySelector('#axios-grid');

  statusEl.textContent = 'Loading via Axios...';
  const posts = await apiFetchAxios(`${JSON_PLACEHOLDER}/posts`, { userId: 1 });
  statusEl.textContent = '';

  grid.innerHTML = posts
    .map(
      (post) => `
      <article class="notif-card">
        <h3>${post.title}</h3>
        <p>${post.body}</p>
      </article>`
    )
    .join('');
}

loadAxiosDemo();

/*
 * Fetch vs Axios — three key differences:
 * 1. JSON parsing: fetch requires a manual `.json()` call; axios parses the response
 *    body automatically and exposes it as `response.data`.
 * 2. Error handling: fetch only rejects on network failure — a 404/500 still resolves
 *    successfully, so `response.ok` must be checked manually. Axios rejects
 *    automatically on any non-2xx status.
 * 3. Convenience features: axios has built-in request/response interceptors, a
 *    `timeout` option, and automatic query-param serialisation via `params`; fetch
 *    provides none of these out of the box.
 */
