import apiClient from './apiClient';

export function getAllCourses() {
  return apiClient.get('/posts?_limit=5').then((posts) =>
    posts.map((post, index) => ({
      id: post.id,
      name: post.title.slice(0, 28),
      code: `CS10${index + 1}`,
      credits: 3 + (index % 2),
      grade: ['A', 'A-', 'B+', 'B', 'A'][index],
    }))
  );
}

export function getCourseById(id) {
  return apiClient.get(`/posts/${id}`).then((post) => ({
    id: post.id,
    name: post.title.slice(0, 28),
    code: `CS10${id}`,
    credits: 3 + (Number(id) % 2),
    body: post.body,
  }));
}

export function enrollStudent(studentId, courseId) {
  // JSONPlaceholder fakes the write — it always returns the posted body with an id.
  return apiClient.post('/posts', { studentId, courseId });
}
