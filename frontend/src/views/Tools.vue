<template>
  <div class="site-page">
    <SiteHeader />
    <main class="page-main">
      <header class="page-header">
        <p class="page-kicker">Curated stack</p>
        <h1 class="page-title page-title--small">工具，不必多，但要顺手。</h1>
        <p class="page-lead">我在开发和创作中持续使用的工具、组件库与云服务。</p>
      </header>

      <section class="tools-grid" aria-label="工具列表">
        <button v-for="(tool, index) in tools" :key="tool.id" type="button" class="tool-card surface card-link" @click="handleNavigate(tool.link)">
          <div class="tool-card__top">
            <div class="tool-logo">
              <img v-if="tool.logo" :src="tool.logo" :alt="`${tool.name} 标志`" loading="lazy" />
              <span v-else>{{ tool.name[0] }}</span>
            </div>
            <span class="tool-index">{{ String(index + 1).padStart(2, '0') }}</span>
          </div>
          <div>
            <h2>{{ tool.name }}</h2>
            <p>{{ tool.description }}</p>
            <div class="tool-tags"><span v-for="tag in tool.tags" :key="tag" class="pill">{{ tag }}</span></div>
          </div>
          <span class="tool-link">访问网站 <span aria-hidden="true">↗</span></span>
        </button>
      </section>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import SiteHeader from '@/components/SiteHeader.vue';
import { tools as staticTools } from '@/lib/content';

const parseTags = (value) => Array.isArray(value) ? value : (value || '').split(',').map(tag => tag.trim()).filter(Boolean);
const tools = ref(staticTools.map(tool => ({ ...tool, tags: parseTags(tool.tags) })));
const handleNavigate = (link) => { if (link) window.open(link, '_blank', 'noopener,noreferrer'); };
</script>

<style scoped>
.page-header { padding-bottom: 56px; border-bottom: 1px solid var(--line); }
.tools-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-top: 40px; }
.tool-card { min-height: 360px; padding: 24px; display: flex; flex-direction: column; justify-content: space-between; color: var(--ink); text-align: left; }
.tool-card__top { display: flex; justify-content: space-between; align-items: start; }
.tool-logo { display: grid; width: 58px; height: 58px; place-items: center; overflow: hidden; color: #fff; background: var(--ink); border-radius: 15px; font-size: 22px; font-weight: 700; }
.tool-logo img { width: 100%; height: 100%; object-fit: cover; }
.tool-index { color: var(--ink-muted); font-size: 12px; font-weight: 700; letter-spacing: .08em; }
.tool-card h2 { margin: 36px 0 10px; font-size: 24px; letter-spacing: -.03em; }
.tool-card p { margin: 0; color: var(--ink-soft); font-size: 14px; line-height: 1.65; }
.tool-tags { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 18px; }
.tool-link { margin-top: 28px; color: var(--accent-dark); font-size: 14px; font-weight: 650; }
@media (max-width: 900px) { .tools-grid { grid-template-columns: repeat(2, 1fr); } }
@media (max-width: 600px) { .tools-grid { grid-template-columns: 1fr; } .tool-card { min-height: 320px; } }
</style>
