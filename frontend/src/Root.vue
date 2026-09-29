<template>
  <div class="min-h-screen">
    <router-view v-slot="{ Component }">
      <component v-if="!shouldKeepAlive" :is="Component" />
      <keep-alive v-else><component :is="Component" /></keep-alive>
    </router-view>
    <MusicPlayer v-if="showMusicPlayer" />
  </div>
</template>

<script setup>
import { computed } from 'vue';
import { useRoute } from 'vue-router';
import MusicPlayer from './components/MusicPlayer.vue';

const route = useRoute();
const showMusicPlayer = computed(() => route.name !== 'Welcome' && route.name !== 'App');
const shouldKeepAlive = computed(() => route.meta?.keepAlive !== false);
</script>
