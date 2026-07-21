<script setup>
defineProps({
  name: String,
  code: String,
  credits: Number,
  grade: String,
})
</script>

<template>
  <article class="course-card">
    <h3>{{ name }}</h3>
    <p>{{ code }}</p>
    <span>{{ credits }} credits<span v-if="grade"> · Grade: {{ grade }}</span></span>
  </article>
</template>
