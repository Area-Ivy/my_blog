<template>
  <div class="welcome-page">
    <SiteHeader />
    <main>
      <div class="welcome-copy">
        <p class="page-kicker">Area—Ivy's personal space</p>
        <h1>思考，构建，<br />然后分享。</h1>
        <p>关于软件工程、系统设计与生活中值得记录的一切。</p>
        <RouterLink class="primary-button" to="/home">进入博客 <span aria-hidden="true">→</span></RouterLink>
      </div>
      <div class="welcome-visual" aria-hidden="true"><div class="orb"></div><span>BUILD / LEARN / SHARE</span></div>
    </main>
  </div>
</template>

<script setup>
import SiteHeader from '@/components/SiteHeader.vue';
</script>

<style scoped>
.welcome-page { min-height: 100dvh; background: #f7f7f5; }
.welcome-page main { width: min(1180px, calc(100% - 40px)); min-height: calc(100dvh - 65px); margin: 0 auto; display: grid; grid-template-columns: 1.15fr .85fr; align-items: center; gap: 64px; padding: 56px 0; }
.welcome-copy h1 { margin: 0; font-size: clamp(54px, 8vw, 104px); line-height: .96; letter-spacing: -.065em; }
.welcome-copy > p:not(.page-kicker) { max-width: 600px; margin: 28px 0 36px; color: var(--ink-soft); font-size: 20px; }
.welcome-visual { position: relative; aspect-ratio: 1; display: grid; place-items: center; overflow: hidden; color: rgba(255,255,255,.8); background: #18212f; border-radius: 48px; box-shadow: var(--shadow-md); }
.welcome-visual::before, .welcome-visual::after { content: ''; position: absolute; border: 1px solid rgba(255,255,255,.13); border-radius: 50%; }
.welcome-visual::before { inset: 13%; } .welcome-visual::after { inset: 28%; }
.orb { width: 26%; aspect-ratio: 1; background: var(--accent); border-radius: 50%; box-shadow: 0 0 90px rgba(244,129,32,.45); }
.welcome-visual span { position: absolute; bottom: 30px; font-size: 11px; font-weight: 700; letter-spacing: .18em; }
@media (max-width: 800px) { .welcome-page main { grid-template-columns: 1fr; padding-top: 72px; } .welcome-visual { width: min(100%, 480px); border-radius: 32px; } }
</style>
