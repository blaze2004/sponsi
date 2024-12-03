<template>
    <Navbar />
    <Toaster position="top-center" :rich-colors="true" />

    <div style="padding-top: 5.2rem">
        <RouterView />
    </div>

    <Footer />
</template>

<script setup>
import { RouterView } from 'vue-router';
import Navbar from './components/Navbar.vue';
import Footer from './components/Footer.vue';
import { Toaster } from 'vue-sonner';
</script>
