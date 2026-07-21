<script setup>
import { ref, watchEffect } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useEnrollmentStore } from '@/stores/enrollment'

const route = useRoute()
const router = useRouter()
const store = useEnrollmentStore()
const course = ref(null)
const loading = ref(true)

watchEffect(async () => {
  loading.value = true
  const id = route.params.id
  const response = await fetch(`https://jsonplaceholder.typicode.com/posts/${id}`)
  const post = await response.json()
  course.value = {
    id: post.id,
    name: post.title.slice(0, 28),
    code: `CS10${id}`,
    credits: 3 + (Number(id) % 2),
    body: post.body,
  }
  loading.value = false
})

function handleEnroll() {
  store.enroll(course.value)
  router.push('/profile')
}
</script>

<template>
  <p v-if="loading" class="status-msg">Loading course...</p>
  <section v-else class="course-detail">
    <h2>{{ course.name }}</h2>
    <p>{{ course.code }} · {{ course.credits }} credits</p>
    <p class="course-body">{{ course.body }}</p>
    <button class="enroll-btn" @click="handleEnroll">Enroll</button>
  </section>
</template>
