<script setup>
import { RouterView } from 'vue-router'
</script>

<template>
<section style="width: 100%; height: 100vh; display: flex; justify-content: center; align-items: center;">
  <article style="margin: auto; border: 1px solid gray;">
    <RouterView />
  </article>
</section>
</template>

<style scoped>
</style>
