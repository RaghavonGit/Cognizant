<script setup>
import { RouterView } from 'vue-router'
import Header from './components/Header.vue'
</script>

<template>
  <Header />
  <main>
    <RouterView />
  </main>
  <footer class="site-footer">
    <p>&copy; 2026 Student Portal. All rights reserved.</p>
  </footer>
</template>
