<script setup>
import { ref, computed, onMounted } from 'vue'
import { RouterLink } from 'vue-router'
import CourseCard from '@/components/CourseCard.vue'
import { useEnrollmentStore } from '@/stores/enrollment'

const courses = ref([])
const loading = ref(true)
const searchTerm = ref('')
const store = useEnrollmentStore()

const filteredCourses = computed(() =>
  courses.value.filter((course) =>
    course.name.toLowerCase().includes(searchTerm.value.toLowerCase())
  )
)

onMounted(async () => {
  const response = await fetch('https://jsonplaceholder.typicode.com/posts?_limit=5')
  const posts = await response.json()
  courses.value = posts.map((post, index) => ({
    id: post.id,
    name: post.title.slice(0, 28),
    code: `CS10${index + 1}`,
    credits: 3 + (index % 2),
    grade: ['A', 'A-', 'B+', 'B', 'A'][index],
  }))
  loading.value = false
})
</script>

<template>
  <section id="courses">
    <h2>Course Catalogue</h2>

    <input
      type="text"
      class="search-input"
      placeholder="Search courses..."
      v-model="searchTerm"
    />

    <p v-if="loading" class="status-msg">Loading courses...</p>

    <div class="course-grid">
      <div v-for="course in filteredCourses" :key="course.id">
        <RouterLink :to="`/courses/${course.id}`" class="card-link">
          <CourseCard :name="course.name" :code="course.code" :credits="course.credits" :grade="course.grade" />
        </RouterLink>
        <button class="enroll-btn" @click="store.enroll(course)">Enroll</button>
      </div>
    </div>
  </section>
</template>
