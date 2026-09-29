<template>
  <div class="site-page">
    <SiteHeader />
    <main class="page-main">
      <section class="about-hero">
        <div class="about-photo"><img src="/avatar.png" alt="Area-Ivy 的头像" /></div>
        <div>
          <p class="page-kicker">About me</p>
          <h1 class="page-title page-title--small">你好，我是 Area—Ivy。</h1>
          <p class="page-lead">同济大学软件工程专业，关注后端开发、系统设计与 AI Agent。也会在这里记录音乐、旅行和持续学习的过程。</p>
          <div class="about-actions">
            <a class="primary-button" href="mailto:chenyiming12500@gmail.com">邮件联系</a>
            <a class="secondary-button" href="https://github.com/Area-Ivy" target="_blank" rel="noopener noreferrer">GitHub ↗</a>
          </div>
        </div>
      </section>

      <section class="about-grid section">
        <article class="about-card surface about-card--wide">
          <p class="page-kicker">Now</p>
          <h2>正在做什么</h2>
          <p>深入工程实践和高性能架构，持续研究 AI Agent，并把可复用的经验整理成文章。</p>
          <div class="year-progress" role="progressbar" :aria-valuenow="Number(progressPercentage)" aria-valuemin="0" aria-valuemax="100" aria-label="本年度进度">
            <div :style="{ width: `${progressPercentage}%` }"></div>
          </div>
          <span class="progress-label">{{ thisYear }} 已过去 {{ progressPercentage }}%</span>
        </article>
        <article class="about-card surface"><p class="page-kicker">Focus</p><h2>关注方向</h2><ul><li>后端与系统设计</li><li>算法与工程效率</li><li>开源和 AI Agent</li></ul></article>
        <article class="about-card surface"><p class="page-kicker">Elsewhere</p><h2>代码之外</h2><ul><li>音乐与现场</li><li>旅行与摄影</li><li>视觉与产品体验</li></ul></article>
      </section>

      <section class="section journey">
        <div class="section-heading"><div><p class="page-kicker">Journey</p><h2>持续向前</h2></div></div>
        <ol>
          <li><time>2018</time><div><h3>踏入编程世界</h3><p>开始学习编程，对计算机和创造软件产生兴趣。</p></div></li>
          <li><time>2024</time><div><h3>深入 Web 开发</h3><p>系统学习前后端技术，完成个人与团队项目。</p></div></li>
          <li><time>2025 — Now</time><div><h3>探索架构与 AI</h3><p>专注系统设计和工程实践，通过博客分享持续思考。</p></div></li>
        </ol>
      </section>
    </main>
  </div>
</template>

<script setup>
import { computed } from 'vue';
import SiteHeader from '@/components/SiteHeader.vue';

const thisYear = new Date().getFullYear();
const start = new Date(`${thisYear}-01-01T00:00:00`).getTime();
const end = new Date(`${thisYear}-12-31T23:59:59`).getTime();
const progressPercentage = computed(() => Math.min(100, Math.max(0, ((Date.now() - start) / (end - start)) * 100)).toFixed(1));
</script>

<style scoped>
.about-hero { display: grid; grid-template-columns: 220px minmax(0, 1fr); gap: 64px; align-items: center; padding-bottom: 64px; border-bottom: 1px solid var(--line); }
.about-photo { aspect-ratio: 1; overflow: hidden; background: var(--surface-soft); border-radius: 32px; box-shadow: var(--shadow-md); transform: rotate(-2deg); }
.about-photo img { width: 100%; height: 100%; object-fit: cover; }
.about-actions { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 30px; }
.about-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 16px; }
.about-card { min-height: 250px; padding: 28px; }
.about-card--wide { grid-column: 1 / -1; min-height: 300px; }
.about-card h2 { margin: 0 0 14px; font-size: 28px; letter-spacing: -.03em; }
.about-card p, .about-card li { color: var(--ink-soft); }
.about-card ul { margin: 20px 0 0; padding: 0; list-style: none; }
.about-card li { padding: 9px 0; border-bottom: 1px solid var(--line); }
.year-progress { height: 8px; margin-top: 52px; overflow: hidden; background: var(--surface-soft); border-radius: 999px; }
.year-progress div { height: 100%; background: var(--accent); border-radius: inherit; }
.progress-label { display: block; margin-top: 10px; color: var(--ink-muted); font-size: 12px; }
.journey ol { margin: 0; padding: 0; list-style: none; border-top: 1px solid var(--line); }
.journey li { display: grid; grid-template-columns: 180px 1fr; gap: 24px; padding: 28px 0; border-bottom: 1px solid var(--line); }
.journey time { color: var(--accent-dark); font-size: 13px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; }
.journey h3 { margin: 0 0 8px; font-size: 21px; }
.journey p { margin: 0; color: var(--ink-soft); }
@media (max-width: 720px) { .about-hero { grid-template-columns: 1fr; gap: 36px; } .about-photo { width: 150px; border-radius: 24px; } .about-grid { grid-template-columns: 1fr; } .about-card--wide { grid-column: auto; } .journey li { grid-template-columns: 1fr; gap: 8px; } }
</style>
