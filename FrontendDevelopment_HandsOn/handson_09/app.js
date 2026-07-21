import { courses } from './data.js';

// ---------- Task 1: ES6+ syntax practice ----------

// Destructuring + loop
for (const { name, credits } of courses) {
  console.log(`${name}: ${credits} credits`);
}

// Array.map() — formatted strings
const formattedCourses = courses.map(
  (course) => `${course.code} — ${course.name} (${course.credits} credits)`
);
console.log('Formatted courses:', formattedCourses);

// Array.filter() — credits >= 4
const highCreditCourses = courses.filter((course) => course.credits >= 4);
console.log('High-credit course count:', highCreditCourses.length);

// Array.reduce() — total credits
const totalCredits = courses.reduce((sum, course) => sum + course.credits, 0);
console.log('Total credits enrolled:', totalCredits);

// ---------- Task 2: DOM selection & dynamic rendering ----------

const courseGrid = document.querySelector('.course-grid');
const totalCreditsEl = document.querySelector('#total-credits');
const resultsCountEl = document.querySelector('#results-count');

function renderCourses(list) {
  courseGrid.innerHTML = '';
  const fragment = document.createDocumentFragment();

  list.forEach((course) => {
    const article = document.createElement('article');
    article.className = 'course-card';
    article.dataset.id = course.id;
    article.tabIndex = 0;
    article.innerHTML = `
      <h3>${course.name}</h3>
      <p>${course.code}</p>
      <span>${course.credits} credits</span>
    `;
    fragment.appendChild(article);
  });

  courseGrid.appendChild(fragment);

  const shownTotal = list.reduce((sum, c) => sum + c.credits, 0);
  totalCreditsEl.textContent = `Total credits: ${shownTotal}`;

  // aria-live="polite" region — announced to screen readers without stealing focus
  resultsCountEl.textContent = `${list.length} course${list.length === 1 ? '' : 's'} found`;
}

renderCourses(courses);

// ---------- Task 3: Event listeners & interactivity ----------

const searchInput = document.querySelector('#search-courses');
const sortButton = document.querySelector('#sort-credits');
const selectedCourseEl = document.querySelector('#selected-course');
const menuToggle = document.querySelector('#menu-toggle');
const mainNav = document.querySelector('#main-nav');

let currentCourses = [...courses];

searchInput.addEventListener('input', (event) => {
  const term = event.target.value.toLowerCase();
  const filtered = currentCourses.filter((course) =>
    course.name.toLowerCase().includes(term)
  );
  renderCourses(filtered);
});

sortButton.addEventListener('click', () => {
  currentCourses = [...currentCourses].sort((a, b) => b.credits - a.credits);
  renderCourses(currentCourses);
});

function selectCourse(card) {
  const course = courses.find((c) => c.id === Number(card.dataset.id));
  if (course) {
    selectedCourseEl.textContent = `Selected: ${course.name} — Grade: ${course.grade}`;
  }
}

// Event delegation: single click listener on the container
courseGrid.addEventListener('click', (event) => {
  const card = event.target.closest('.course-card');
  if (card) selectCourse(card);
});

// Keyboard access: Enter on a focused card triggers the same action as a click
courseGrid.addEventListener('keydown', (event) => {
  if (event.key !== 'Enter') return;
  const card = event.target.closest('.course-card');
  if (card) selectCourse(card);
});

// Mobile hamburger menu — aria-expanded toggled between true/false on open/close
menuToggle.addEventListener('click', () => {
  const isOpen = menuToggle.getAttribute('aria-expanded') === 'true';
  menuToggle.setAttribute('aria-expanded', String(!isOpen));
  mainNav.classList.toggle('nav-open', !isOpen);
});
