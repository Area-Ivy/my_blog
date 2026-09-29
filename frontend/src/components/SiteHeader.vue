<template>
  <header class="site-header">
    <div class="site-header__inner">
      <RouterLink to="/home" class="site-brand" aria-label="Area-Ivy 博客首页">
        <span class="site-brand__mark">A</span>
        <span>Area—Ivy</span>
      </RouterLink>

      <nav class="site-nav" aria-label="主导航">
        <RouterLink v-for="item in navItems" :key="item.to" :to="item.to">{{ item.label }}</RouterLink>
      </nav>

      <a class="site-header__github" href="https://github.com/Area-Ivy" target="_blank" rel="noopener noreferrer">
        GitHub <span aria-hidden="true">↗</span>
      </a>
      <button class="menu-button" type="button" :aria-expanded="menuOpen" aria-controls="mobile-nav" @click="menuOpen = !menuOpen">
        <span class="sr-only">切换导航菜单</span>
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true">
          <path v-if="!menuOpen" d="M4 7h16M4 12h16M4 17h16" />
          <path v-else d="M6 6l12 12M18 6L6 18" />
        </svg>
      </button>
    </div>
    <nav v-if="menuOpen" id="mobile-nav" class="mobile-nav" aria-label="移动端导航">
      <RouterLink v-for="item in navItems" :key="item.to" :to="item.to" @click="menuOpen = false">{{ item.label }}</RouterLink>
    </nav>
  </header>
</template>

<script setup>
import { ref } from 'vue';

const menuOpen = ref(false);
const navItems = [
  { to: '/home', label: '首页' },
  { to: '/posts', label: '文章' },
  { to: '/tools', label: '工具' },
  { to: '/footprints', label: '足迹' },
  { to: '/about', label: '关于' },
];
</script>

<style scoped>
.site-header { position: sticky; top: 0; z-index: 40; color: var(--ink); background: rgba(247,247,245,.86); border-bottom: 1px solid rgba(209,213,219,.75); backdrop-filter: saturate(180%) blur(18px); }
.site-header__inner { width: min(1180px, calc(100% - 40px)); min-height: 64px; margin: 0 auto; display: flex; align-items: center; gap: 32px; }
.site-brand { display: inline-flex; min-height: 44px; align-items: center; gap: 10px; font-size: 15px; font-weight: 720; letter-spacing: -.02em; }
.site-brand__mark { display: grid; width: 30px; height: 30px; place-items: center; color: #fff; background: var(--ink); border-radius: 9px; font-size: 14px; }
.site-nav { display: flex; align-items: center; gap: 6px; margin: 0 auto; }
.site-nav a { position: relative; min-height: 40px; padding: 8px 13px; border-radius: 999px; color: var(--ink-soft); font-size: 14px; font-weight: 550; }
.site-nav a:hover { color: var(--ink); background: rgba(17,24,39,.05); }
.site-nav a.router-link-active { color: var(--ink); background: var(--surface); box-shadow: 0 0 0 1px var(--line); }
.site-header__github { display: inline-flex; min-height: 44px; align-items: center; gap: 6px; color: var(--ink-soft); font-size: 14px; font-weight: 600; }
.site-header__github:hover { color: var(--ink); }
.menu-button { display: none; width: 44px; height: 44px; margin-left: auto; place-items: center; color: var(--ink); background: transparent; border: 0; border-radius: 10px; }
.mobile-nav { display: none; }
.sr-only { position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip: rect(0,0,0,0); white-space: nowrap; border: 0; }
@media (max-width: 767px) {
  .site-header__inner { width: calc(100% - 24px); min-height: 58px; }
  .site-nav, .site-header__github { display: none; }
  .menu-button { display: grid; }
  .mobile-nav { display: grid; width: calc(100% - 24px); margin: 0 auto; padding: 8px 0 14px; grid-template-columns: repeat(2, 1fr); gap: 6px; }
  .mobile-nav a { min-height: 44px; padding: 10px 12px; color: var(--ink-soft); border-radius: 10px; font-size: 15px; }
  .mobile-nav a.router-link-active { color: var(--ink); background: var(--surface); box-shadow: 0 0 0 1px var(--line); }
}
</style>
