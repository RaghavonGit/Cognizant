<script setup>
import { RouterLink } from 'vue-router'
import { useEnrollmentStore } from '@/stores/enrollment'

const store = useEnrollmentStore()
</script>

<template>
  <header class="site-header">
    <div class="site-name">Student Portal</div>
    <nav>
      <RouterLink to="/">Home</RouterLink>
      <RouterLink to="/courses">Courses</RouterLink>
      <RouterLink to="/profile">Profile</RouterLink>
    </nav>
    <div class="enrolled-badge">Enrolled: {{ store.enrolledCourses.length }}</div>
  </header>
</template>
