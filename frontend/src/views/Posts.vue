<template>
  <div class="site-page">
    <SiteHeader />
    <main class="page-main posts-page">
      <header class="posts-intro">
        <div><p class="page-kicker">Writing</p><h1 class="page-title page-title--small">文章与笔记</h1><p class="page-lead">记录工程实践，也整理那些值得反复推敲的问题。</p></div>
        <div class="search-wrap">
          <label for="article-search">搜索文章</label>
          <div class="search-field">
            <svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-4-4"/></svg>
            <input id="article-search" v-model="searchQuery" type="search" placeholder="标题、摘要或标签" @input="handleSearchInput" @focus="showSearchResults = true" @blur="handleSearchBlur" />
          </div>
          <div v-if="showSearchResults && searchQuery" class="search-results surface">
            <p v-if="loading">搜索中…</p><p v-else-if="!searchResults.length">没有找到相关文章</p>
            <button v-for="post in searchResults" v-else :key="post.id" type="button" @mousedown.prevent="selectSearchResult(post)">
              <strong>{{ post.title }}</strong><span>{{ post.date || '未标注日期' }}</span>
            </button>
          </div>
        </div>
      </header>

      <div class="posts-layout">
        <aside class="article-index" aria-label="文章目录">
          <p class="article-index__label">全部文章 · {{ allPosts.length }}</p>
          <button v-for="post in allPosts" :key="post.id" type="button" :class="{ active: selectedPost?.id === post.id }" @click="selectPost(post)">
            <span>{{ post.title }}</span><time>{{ post.date || '未标注日期' }}</time>
          </button>
        </aside>

        <article v-if="selectedPost" class="article surface">
          <header class="article-header">
            <div class="article-tags"><span v-for="tag in selectedPost.tags || []" :key="tag" class="pill">{{ tag }}</span></div>
            <h1>{{ selectedPost.title }}</h1>
            <p v-if="selectedPost.summary || selectedPost.excerpt" class="article-summary">{{ selectedPost.summary || selectedPost.excerpt }}</p>
            <div class="article-meta">
              <span v-if="selectedPost.updated_at">更新于 {{ formatDate(selectedPost.updated_at) }}</span>
              <span>{{ wordCount }} 字</span><span>约 {{ readingTime }} 分钟</span>
            </div>
          </header>
          <div class="post-body" v-html="renderedContent"></div>
        </article>
        <div v-else class="article surface empty-state">暂无文章</div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onBeforeUnmount } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { marked } from 'marked';
import SiteHeader from '@/components/SiteHeader.vue';
import { articles, searchArticles as searchLocalArticles } from '@/lib/content';

const route = useRoute();
const router = useRouter();
const allPosts = ref([]);
const selectedPost = ref(null);
const searchResults = ref([]);
const searchQuery = ref('');
const loading = ref(false);
const showSearchResults = ref(false);
let searchTimeout;

marked.setOptions({ breaks: true, gfm: true });
const renderedContent = computed(() => selectedPost.value?.content ? marked.parse(selectedPost.value.content) : '');
const plainContent = computed(() => (selectedPost.value?.content || '').replace(/```[\s\S]*?```/g, '').replace(/<[^>]*>|[#*_`>\[\]()!-]/g, ' ').replace(/\s+/g, ' ').trim());
const wordCount = computed(() => {
  const text = plainContent.value;
  const chinese = text.match(/[\u4e00-\u9fa5]/g)?.length || 0;
  return chinese + Math.ceil(text.replace(/[\u4e00-\u9fa5\s]/g, '').length * .5);
});
const readingTime = computed(() => Math.max(1, Math.ceil(wordCount.value / 300)));

function formatDate(value) {
  if (!value) return '';
  const date = new Date(value);
  return `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
}
function selectPost(post, updateUrl = true) {
  selectedPost.value = { ...post };
  showSearchResults.value = false;
  if (updateUrl) router.replace({ path: '/posts', query: { id: post.id } });
  window.scrollTo({ top: 0, behavior: 'smooth' });
}
function selectSearchResult(post) { searchQuery.value = ''; selectPost(post); }
function chooseFromRoute() {
  const match = allPosts.value.find(post => String(post.id) === String(route.query.id));
  selectPost(match || allPosts.value[0], false);
}
function handleSearchInput() {
  clearTimeout(searchTimeout);
  loading.value = true;
  searchTimeout = setTimeout(() => { searchResults.value = searchLocalArticles(searchQuery.value); loading.value = false; }, 220);
}
function handleSearchBlur() { setTimeout(() => { showSearchResults.value = false; }, 180); }

watch(() => route.query.id, chooseFromRoute);
onMounted(() => { allPosts.value = articles; chooseFromRoute(); });
onBeforeUnmount(() => clearTimeout(searchTimeout));
</script>

<style scoped>
.posts-page { padding-top: 56px; }
.posts-intro { display: grid; grid-template-columns: 1fr 360px; gap: 64px; align-items: end; padding-bottom: 48px; border-bottom: 1px solid var(--line); }
.search-wrap { position: relative; z-index: 10; }
.search-wrap > label { display: block; margin-bottom: 8px; color: var(--ink-soft); font-size: 13px; font-weight: 650; }
.search-field { height: 50px; display: flex; align-items: center; gap: 10px; padding: 0 14px; color: var(--ink-muted); background: var(--surface); border: 1px solid var(--line-strong); border-radius: 13px; }
.search-field:focus-within { border-color: var(--accent); box-shadow: 0 0 0 3px var(--accent-soft); }
.search-field input { width: 100%; color: var(--ink); background: transparent; border: 0; outline: 0; }
.search-results { position: absolute; top: calc(100% + 10px); right: 0; left: 0; max-height: 360px; overflow: auto; padding: 8px; box-shadow: var(--shadow-md); }
.search-results > p { margin: 0; padding: 16px; color: var(--ink-muted); font-size: 14px; }
.search-results button { width: 100%; min-height: 64px; padding: 10px 12px; display: flex; flex-direction: column; align-items: start; color: var(--ink); background: transparent; border: 0; border-radius: 9px; text-align: left; }
.search-results button:hover { background: var(--surface-soft); }
.search-results span { color: var(--ink-muted); font-size: 12px; }
.posts-layout { display: grid; grid-template-columns: 250px minmax(0, 1fr); gap: 32px; align-items: start; margin-top: 40px; }
.article-index { position: sticky; top: 88px; max-height: calc(100vh - 120px); overflow: auto; padding-right: 10px; }
.article-index__label { margin: 0 0 12px; color: var(--ink-muted); font-size: 12px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; }
.article-index button { width: 100%; min-height: 66px; padding: 11px 12px; display: flex; flex-direction: column; align-items: start; justify-content: center; color: var(--ink-soft); background: transparent; border: 0; border-left: 2px solid var(--line); text-align: left; }
.article-index button:hover { color: var(--ink); background: rgba(255,255,255,.55); }
.article-index button.active { color: var(--ink); background: var(--surface); border-left-color: var(--accent); }
.article-index button span { font-size: 14px; font-weight: 650; line-height: 1.35; }
.article-index time { margin-top: 4px; color: var(--ink-muted); font-size: 11px; }
.article { min-width: 0; overflow: hidden; padding: clamp(28px, 6vw, 72px); }
.article-header { padding-bottom: 36px; border-bottom: 1px solid var(--line); }
.article-tags { display: flex; flex-wrap: wrap; gap: 6px; }
.article-header h1 { margin: 18px 0; font-size: clamp(34px, 5vw, 58px); line-height: 1.08; letter-spacing: -.045em; }
.article-summary { max-width: 720px; margin: 0; color: var(--ink-soft); font-size: 18px; line-height: 1.7; }
.article-meta { display: flex; flex-wrap: wrap; gap: 8px 18px; margin-top: 22px; color: var(--ink-muted); font-size: 12px; }
.post-body { min-width: 0; max-width: 760px; margin: 48px auto 0; overflow-wrap: anywhere; color: #303744; font-size: 17px; line-height: 1.85; }
.post-body :deep(h1), .post-body :deep(h2), .post-body :deep(h3), .post-body :deep(h4) { color: var(--ink); line-height: 1.25; letter-spacing: -.025em; scroll-margin-top: 90px; }
.post-body :deep(h1) { margin: 2em 0 .8em; font-size: 34px; }
.post-body :deep(h2) { margin: 2em 0 .75em; font-size: 28px; }
.post-body :deep(h3) { margin: 1.8em 0 .6em; font-size: 22px; }
.post-body :deep(p) { margin: 1.15em 0; }
.post-body :deep(a) { color: var(--accent-dark); text-decoration: underline; text-underline-offset: 3px; }
.post-body :deep(code) { padding: .15em .38em; color: #9a3412; background: #fff1e6; border-radius: 5px; font-family: "SFMono-Regular", Consolas, monospace; font-size: .88em; }
.post-body :deep(pre) { max-width: 100%; margin: 1.8em 0; padding: 20px; overflow: auto; color: #e5e7eb; background: #151b25; border-radius: 13px; overflow-wrap: normal; }
.post-body :deep(pre code) { padding: 0; color: inherit; background: transparent; }
.post-body :deep(blockquote) { margin: 1.8em 0; padding: 2px 0 2px 22px; color: var(--ink-soft); border-left: 3px solid var(--accent); }
.post-body :deep(img) { height: auto; margin: 2em auto; border-radius: 12px; }
.post-body :deep(table) { width: 100%; margin: 1.8em 0; border-collapse: collapse; font-size: 14px; }
.post-body :deep(th), .post-body :deep(td) { padding: 12px; border: 1px solid var(--line); text-align: left; }
.post-body :deep(th) { background: var(--surface-soft); }
.post-body :deep(ul), .post-body :deep(ol) { padding-left: 1.4em; }
.empty-state { min-height: 320px; display: grid; place-items: center; color: var(--ink-muted); }
@media (max-width: 900px) { .posts-intro { grid-template-columns: 1fr; gap: 36px; } .posts-layout { grid-template-columns: 1fr; } .article-index { position: static; max-height: 260px; } }
@media (max-width: 600px) { .article { padding: 24px 20px; } .post-body { font-size: 16px; } .article-header h1 { font-size: 36px; } }
</style>
