<script setup>
import { RouterLink } from 'vue-router'
</script>

<template>
  <section class="hero-page">
    <h1>Welcome to the Student Portal</h1>
    <p>Track your courses, grades, and notifications all in one place.</p>
    <RouterLink to="/courses" class="cta-link">Explore Courses</RouterLink>
  </section>
</template>
