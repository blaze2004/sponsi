<script setup>
import { RouterLink, RouterView } from 'vue-router'
import HelloWorld from './components/hello-world.vue'
</script>

<template>
  <header>
    <img alt="Vue logo" class="logo" src="@/assets/images/logo.png" width="125" height="125" />
    <p>ghfh</p>
    <div class="wrapper">
      <HelloWorld msg="You did it!" />

      <nav>
        <RouterLink to="/">Home</RouterLink>
      </nav>
    </div>
  </header>

  <RouterView />
</template>

<style scoped>

</style>
