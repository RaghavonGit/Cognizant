<script setup>
import { reactive } from 'vue'
import { storeToRefs } from 'pinia'
import { useEnrollmentStore } from '@/stores/enrollment'

const store = useEnrollmentStore()
// storeToRefs keeps reactivity when destructuring — plain destructuring would not.
const { enrolledCourses, totalCredits } = storeToRefs(store)

const profile = reactive({ name: '', email: '', semester: '' })
</script>

<template>
  <section class="profile-form">
    <h2>Student Profile</h2>
    <form @submit.prevent>
      <label>
        Name
        <input type="text" v-model="profile.name" />
      </label>
      <label>
        Email
        <input type="email" v-model="profile.email" />
      </label>
      <label>
        Semester
        <input type="number" v-model="profile.semester" />
      </label>
    </form>
    <p class="profile-preview">
      {{ profile.name || 'Name' }} · {{ profile.email || 'email@example.com' }} · Semester {{ profile.semester || '-' }}
    </p>
  </section>

  <section class="enrolled-list">
    <h2>Enrolled Courses ({{ enrolledCourses.length }}) · {{ totalCredits }} total credits</h2>
    <p v-if="enrolledCourses.length === 0" class="status-msg">No courses enrolled yet.</p>
    <div class="course-grid">
      <article class="course-card" v-for="course in enrolledCourses" :key="course.id">
        <h3>{{ course.name }}</h3>
        <p>{{ course.code }}</p>
        <span>{{ course.credits }} credits</span>
        <button class="remove-btn" @click="store.unenroll(course.id)">Remove</button>
      </article>
    </div>
    <button v-if="enrolledCourses.length > 0" class="reset-btn" @click="store.$reset()">Reset All</button>
  </section>
</template>
