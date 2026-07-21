import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useEnrollmentStore = defineStore('enrollment', () => {
  const enrolledCourses = ref([])

  const totalCredits = computed(() =>
    enrolledCourses.value.reduce((sum, course) => sum + course.credits, 0)
  )

  function enroll(course) {
    if (!enrolledCourses.value.some((c) => c.id === course.id)) {
      enrolledCourses.value.push(course)
    }
  }

  function unenroll(courseId) {
    enrolledCourses.value = enrolledCourses.value.filter((c) => c.id !== courseId)
  }

  // Advanced pattern (Hands-On 10 concept): fetch + enroll in one action
  async function fetchAndEnroll(courseId) {
    const response = await fetch(`https://jsonplaceholder.typicode.com/posts/${courseId}`)
    const post = await response.json()
    enroll({
      id: post.id,
      name: post.title.slice(0, 28),
      code: `CS10${courseId}`,
      credits: 3 + (Number(courseId) % 2),
    })
  }

  function $reset() {
    enrolledCourses.value = []
  }

  return { enrolledCourses, totalCredits, enroll, unenroll, fetchAndEnroll, $reset }
})
