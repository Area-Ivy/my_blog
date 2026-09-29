<template>
  <div class="site-page">
    <SiteHeader />
    <main class="page-main">
      <section class="home-hero">
        <div>
          <p class="page-kicker">Developer · Builder · Explorer</p>
          <h1 class="page-title">把复杂的问题，写成清晰的答案。</h1>
          <p class="page-lead">这里记录工程实践、系统设计，以及沿途值得留下的技术与生活片段。</p>
          <div class="home-actions">
            <RouterLink class="primary-button" to="/posts">开始阅读 <span aria-hidden="true">→</span></RouterLink>
            <RouterLink class="secondary-button" to="/about">了解我</RouterLink>
          </div>
        </div>
        <div class="hero-note surface">
          <span class="hero-note__dot" aria-hidden="true"></span>
          <p>最近更新</p>
          <strong>{{ stats.lastUpdate }}</strong>
          <span>{{ stats.articles }} 篇文章 · {{ stats.footprints }} 段足迹</span>
        </div>
      </section>

      <section class="section">
        <div class="section-heading">
          <div><p class="page-kicker">Featured writing</p><h2>最近的文章</h2></div>
          <RouterLink class="text-link" to="/posts">查看全部文章 →</RouterLink>
        </div>
        <div class="article-grid">
          <article v-for="(article, index) in recommendedArticles" :key="article.id" class="article-card surface card-link" @click="goToArticle(article.id)">
            <button type="button" :aria-label="`阅读《${article.title}》`">
              <div class="article-card__number">0{{ index + 1 }}</div>
              <div>
                <p class="article-card__date">{{ article.date }}</p>
                <h3>{{ article.title }}</h3>
                <p>{{ article.excerpt || '一篇关于工程与思考的记录。' }}</p>
              </div>
              <span class="article-card__arrow" aria-hidden="true">↗</span>
            </button>
          </article>
        </div>
      </section>

      <section class="section explore-section">
        <div class="section-heading"><div><p class="page-kicker">Explore</p><h2>不止是代码</h2></div></div>
        <div class="explore-grid">
          <RouterLink to="/tools" class="explore-card explore-card--orange card-link">
            <span class="explore-card__eyebrow">{{ stats.tools }} 个收藏</span><h3>工具箱</h3><p>经过筛选的开发工具、组件库与云平台。</p><span>探索工具 →</span>
          </RouterLink>
          <RouterLink to="/footprints" class="explore-card explore-card--ink card-link">
            <span class="explore-card__eyebrow">{{ stats.footprints }} 段记录</span><h3>足迹</h3><p>旅行、现场，以及那些值得被记住的瞬间。</p><span>查看足迹 →</span>
          </RouterLink>
          <RouterLink to="/about" class="explore-card explore-card--paper card-link">
            <span class="explore-card__eyebrow">About</span><h3>关于我</h3><p>后端工程、开源、学习，以及正在探索的方向。</p><span>继续了解 →</span>
          </RouterLink>
        </div>
      </section>

      <footer class="home-footer"><span>Area—Ivy © {{ new Date().getFullYear() }}</span><a href="https://github.com/Area-Ivy" target="_blank" rel="noopener noreferrer">GitHub ↗</a></footer>
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import SiteHeader from '@/components/SiteHeader.vue';
import { articles, tools, footprints } from '@/lib/content';

const router = useRouter();
const goToArticle = (articleId) => router.push({ path: '/posts', query: { id: articleId } });
const stats = ref({ articles: articles.length, tools: tools.length, footprints: footprints.length, lastUpdate: articles[0]?.date || '--' });
const recommendedArticles = ref(articles.slice(0, 3));
</script>

<style scoped>
.home-hero { display: grid; grid-template-columns: minmax(0, 1fr) 280px; gap: 64px; align-items: end; padding: 48px 0 64px; border-bottom: 1px solid var(--line); }
.home-actions { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 32px; }
.hero-note { padding: 24px; }
.hero-note__dot { display: block; width: 10px; height: 10px; margin-bottom: 32px; background: var(--accent); border-radius: 50%; box-shadow: 0 0 0 7px var(--accent-soft); }
.hero-note p, .hero-note span { display: block; margin: 0; color: var(--ink-muted); font-size: 13px; }
.hero-note strong { display: block; margin: 4px 0 14px; font-size: 22px; letter-spacing: -.03em; }
.article-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; }
.article-card { overflow: hidden; }
.article-card button { position: relative; width: 100%; min-height: 320px; padding: 24px; display: flex; flex-direction: column; justify-content: space-between; text-align: left; color: inherit; background: transparent; border: 0; }
.article-card__number { color: var(--accent-dark); font-size: 13px; font-weight: 750; letter-spacing: .08em; }
.article-card__date { margin: 0 0 10px; color: var(--ink-muted); font-size: 13px; }
.article-card h3 { margin: 0; font-size: 23px; line-height: 1.3; letter-spacing: -.025em; }
.article-card p:last-child { margin: 14px 0 0; color: var(--ink-soft); font-size: 14px; line-height: 1.65; }
.article-card__arrow { position: absolute; top: 22px; right: 22px; color: var(--ink-muted); font-size: 20px; }
.explore-grid { display: grid; grid-template-columns: 1.2fr 1fr 1fr; gap: 16px; }
.explore-card { min-height: 300px; padding: 28px; display: flex; flex-direction: column; justify-content: flex-end; border: 1px solid transparent; border-radius: var(--radius-lg); }
.explore-card__eyebrow { margin-bottom: auto; font-size: 12px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; opacity: .65; }
.explore-card h3 { margin: 0 0 10px; font-size: 30px; letter-spacing: -.035em; }
.explore-card p { max-width: 320px; margin: 0 0 24px; opacity: .72; }
.explore-card > span:last-child { font-weight: 650; }
.explore-card--orange { color: #44210b; background: #f8b36f; }
.explore-card--ink { color: #fff; background: #18212f; }
.explore-card--paper { color: var(--ink); background: var(--surface); border-color: var(--line); }
.home-footer { display: flex; justify-content: space-between; margin-top: 100px; padding-top: 24px; color: var(--ink-muted); border-top: 1px solid var(--line); font-size: 13px; }
@media (max-width: 900px) { .home-hero { grid-template-columns: 1fr; } .hero-note { max-width: 380px; } .article-grid, .explore-grid { grid-template-columns: 1fr; } .article-card button { min-height: 250px; } .explore-card { min-height: 260px; } }
@media (max-width: 520px) { .home-hero { gap: 36px; padding-top: 28px; } .hero-note { width: 100%; } }
</style>
