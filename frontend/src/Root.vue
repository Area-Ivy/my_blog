<template>
  <div class="relative min-h-screen">
    <div
      v-if="showLogoBackground"
      class="logo-background pointer-events-none"
      aria-hidden="true"
    >
      <div class="logo-background__base"></div>
      <div class="logo-background__glow"></div>
      <div class="logo-background__logo"></div>
    </div>
    <router-view v-slot="{ Component }">
      <component v-if="!shouldKeepAlive" :is="Component" />
      <keep-alive v-else>
        <component :is="Component" />
      </keep-alive>
    </router-view>
    <!-- MusicPlayer 提升到根组件，不受路由切换影响 -->
    <MusicPlayer v-if="showMusicPlayer" />
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';
import { useRoute } from 'vue-router';
import MusicPlayer from './components/MusicPlayer.vue';

const route = useRoute();
const WELCOME_ROUTE_NAME = 'Welcome';

// 判断是否显示 MusicPlayer（在有 SideNav 的页面显示）
const showMusicPlayer = computed(() => {
  const routeName = route.name;
  return routeName !== WELCOME_ROUTE_NAME && routeName !== 'App';
});

const showLogoBackground = computed(() => {
  const routeName = route.name;
  return routeName !== WELCOME_ROUTE_NAME;
});

const shouldKeepAlive = computed(() => route.meta?.keepAlive !== false);

</script>

<style scoped>
.logo-background {
  position: fixed;
  inset: 0;
  z-index: -1;
  overflow: hidden;
}

.logo-background__base,
.logo-background__glow,
.logo-background__logo {
  position: absolute;
  inset: 0;
}

.logo-background__base {
  background: var(--theme-page-bg);
}

.logo-background__glow {
  background: var(--theme-background-glow);
  opacity: 0.3;
  filter: blur(80px);
}

.logo-background__logo {
  background-image: url('/logo_mygo.png');
  background-repeat: no-repeat;
  background-position: center;
  background-size: min(65vmin, 560px);
  filter: blur(5px);
  opacity: var(--theme-logo-opacity);
  transform: scale(1.15);
  mix-blend-mode: screen;
}
</style>
