<template>
	<div class="min-h-screen w-full overflow-x-hidden text-white relative">
		<SiteHeader />
		<div class="flex">
			<SideNav />
			<main class="flex-1 pt-24 px-6 md:px-8 lg:ml-52 lg:px-10 xl:ml-56 xl:px-12">
				<ClientOnly>
					<BlurReveal
						:delay="0.1"
						:duration="0.75"
						class="posts-layout max-w-7xl"
					>
						<section class="posts-content">
							<!-- 搜索框 -->
							<div class="mb-6 relative z-50">
								<div class="relative">
									<input
										v-model="searchQuery"
										@input="handleSearchInput"
										@focus="showSearchResults = true"
										@blur="handleSearchBlur"
										type="text"
										placeholder="搜索文章标题、摘要或标签..."
										class="w-full rounded-xl border border-white/10 bg-white/5 px-4 py-3 pl-10 pr-10 text-white placeholder:text-white/40 focus:border-white/20 focus:outline-none focus:ring-2 focus:ring-white/10 transition-all"
									/>
									<svg
										v-if="!searchQuery"
										class="absolute left-3 top-1/2 h-5 w-5 -translate-y-1/2 text-white/40"
										fill="none"
										stroke="currentColor"
										viewBox="0 0 24 24"
									>
										<path
											stroke-linecap="round"
											stroke-linejoin="round"
											stroke-width="2"
											d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
										/>
									</svg>
									<button
										v-if="searchQuery"
										@click="clearSearch"
										class="absolute right-3 top-1/2 -translate-y-1/2 text-white/40 hover:text-white/60 transition-colors"
									>
										<svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
											<path
												stroke-linecap="round"
												stroke-linejoin="round"
												stroke-width="2"
												d="M6 18L18 6M6 6l12 12"
											/>
										</svg>
									</button>
								</div>
								
								<!-- 搜索结果下拉框 -->
								<div 
									v-if="showSearchResults && searchQuery" 
									class="search-dropdown absolute top-full left-0 right-0 mt-2 rounded-xl border border-white/10 bg-black/95 backdrop-blur-xl shadow-2xl max-h-[600px] overflow-hidden z-50"
								>
									<div v-if="loading" class="p-4 text-center text-white/60 text-sm">
										搜索中...
									</div>
									<div v-else-if="searchResults.length === 0" class="p-4 text-center text-white/60 text-sm">
										未找到相关文章
									</div>
									<div v-else class="max-h-[600px] overflow-y-auto">
										<div
											class="search-result-item border-b border-white/5 p-4 cursor-pointer transition-all hover:bg-white/5"
											v-for="post in searchResults"
											:key="post.id"
											:class="{ 'bg-white/5': selectedPost && selectedPost.id === post.id }"
											@mousedown.prevent="selectPost(post)"
										>
											<div class="search-result-title font-semibold text-white mb-1">{{ post.title }}</div>
											<div
												v-if="post.highlight"
												class="search-result-highlight text-sm text-white/80 mb-2 line-clamp-3"
												v-html="post.highlight"
											></div>
											<div v-else-if="post.excerpt" class="search-result-excerpt text-sm text-white/60 mb-2 line-clamp-2">
												{{ post.excerpt }}
											</div>
											<div class="flex items-center justify-between">
												<div class="text-xs text-white/50">{{ post.date || '未知日期' }}</div>
												<div class="search-result-tags">
													<span class="tag" v-for="tag in post.tags || []" :key="tag">{{ tag }}</span>
												</div>
											</div>
										</div>
									</div>
								</div>
							</div>
							<div
								v-if="errorMessage"
								class="mb-4 rounded-lg border border-red-500/40 bg-red-500/10 px-4 py-3 text-sm text-red-200"
							>
								{{ errorMessage }}
							</div>
							<div class="post-scroll-container">
								<div v-if="selectedPost" class="rounded-xl border border-white/10 bg-white/5 p-6 backdrop-blur post-content-card">
									<div class="post-header">
										<div class="post-title-wrapper">
											<h1 class="post-title">{{ selectedPost.title }}</h1>
											<div v-if="(selectedPost.tags || []).length" class="post-tags-inline">
												<span class="tag" v-for="tag in selectedPost.tags || []" :key="tag">{{ tag }}</span>
											</div>
										</div>
										<div class="post-meta text-white/70 text-sm">
											<span v-if="selectedPost.created_at">
												<span class="meta-label">创建时间：</span>{{ formatDate(selectedPost.created_at) }}
											</span>
											<span v-if="selectedPost.created_at && selectedPost.updated_at">·</span>
											<span v-if="selectedPost.updated_at">
												<span class="meta-label">更新时间：</span>{{ formatDate(selectedPost.updated_at) }}
											</span>
											<span v-if="selectedPost.updated_at && wordCount > 0">·</span>
											<span v-if="wordCount > 0">
												<span class="meta-label">字数：</span>{{ wordCount }} 字
											</span>
											<span v-if="wordCount > 0 && readingTime > 0">·</span>
											<span v-if="readingTime > 0">
												<span class="meta-label">预计阅读：</span>{{ readingTime }} 分钟
											</span>
										</div>
										<div v-if="selectedPost.summary || selectedPost.excerpt" class="post-summary mt-4">
											<div class="post-summary-content">
												{{ selectedPost.summary || selectedPost.excerpt }}
											</div>
										</div>
									</div>
									<div class="post-body prose prose-invert max-w-none w-full" v-html="renderedContent"></div>
								</div>
								<div v-else class="rounded-xl border border-white/10 bg-white/5 p-6 backdrop-blur post-content-card post-placeholder">
									<div class="placeholder-content">
										<p>暂无文章，请稍后重试。</p>
									</div>
								</div>
							</div>
						</section>

						<aside class="posts-rightbar">
							<div class="rounded-xl border border-white/10 bg-white/5 p-4 backdrop-blur toc-container">
								<h4 class="m-0 mb-3">文章目录</h4>
								<div v-if="allPosts.length === 0" class="text-center py-4 text-white/60 text-sm">
									暂无文章
								</div>
								<div v-else class="post-list">
									<div
										class="post-item"
										v-for="post in allPosts"
										:key="post.id"
										:class="{ active: selectedPost && selectedPost.id === post.id }"
										@click="selectPost(post)"
									>
										<div class="post-item-title">{{ post.title }}</div>
										<div class="post-item-meta">{{ post.date || '未知日期' }}</div>
										<div class="post-item-tags">
											<span class="tag" v-for="tag in post.tags || []" :key="tag">{{ tag }}</span>
										</div>
									</div>
								</div>
							</div>
						</aside>
					</BlurReveal>
				</ClientOnly>
			</main>
		</div>
	</div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onBeforeUnmount } from 'vue';
import { useRoute } from 'vue-router';
import { marked } from 'marked';
import SiteHeader from '@/components/SiteHeader.vue';
import SideNav from '@/components/SideNav.vue';
import ClientOnly from '@/components/ClientOnly.vue';
import BlurReveal from '@/components/BlurReveal.vue';
import { articles, searchArticles as searchLocalArticles } from '@/lib/content';

const route = useRoute();

const allPosts = ref([]);
const searchResults = ref([]);
const errorMessage = ref('');
const searchQuery = ref('');
const loading = ref(false);
const showSearchResults = ref(false);
let searchTimeout = null;

// 加载所有文章（用于右侧目录）
function loadAllArticles() {
	allPosts.value = articles;
	checkAndSelectArticle();
}

// 搜索文章
function searchArticles(query = '') {
	if (!query || !query.trim()) {
		searchResults.value = [];
		return;
	}
	
	loading.value = true;
	errorMessage.value = '';
	searchResults.value = searchLocalArticles(query);
	loading.value = false;
}

// 处理搜索输入（防抖）
function handleSearchInput() {
	if (searchTimeout) {
		clearTimeout(searchTimeout);
	}
	searchTimeout = setTimeout(() => {
		searchArticles(searchQuery.value);
	}, 300); // 300ms 防抖
}

// 清除搜索
function clearSearch() {
	searchQuery.value = '';
	searchResults.value = [];
	showSearchResults.value = false;
}

// 处理搜索框失焦
function handleSearchBlur() {
	// 延迟关闭，以便点击搜索结果时能触发
	setTimeout(() => {
		showSearchResults.value = false;
	}, 200);
}


// 配置marked选项
marked.setOptions({
	breaks: true, // 支持换行
	gfm: true, // 支持GitHub风格的markdown
});

// 将markdown内容转换为HTML
const renderedContent = computed(() => {
	if (!selectedPost.value || !selectedPost.value.content) {
		return '';
	}
	try {
		// 使用marked将markdown转换为HTML
		return marked.parse(selectedPost.value.content);
	} catch (error) {
		console.error('Markdown渲染错误:', error);
		return '<p>内容渲染失败</p>';
	}
});

// 计算文章字数（去除markdown语法，只计算纯文本）
function calculateWordCount(content) {
	if (!content) return 0;
	// 移除markdown代码块
	let text = content.replace(/```[\s\S]*?```/g, '');
	// 移除行内代码
	text = text.replace(/`[^`]*`/g, '');
	// 移除markdown链接 [text](url)
	text = text.replace(/\[([^\]]*)\]\([^\)]*\)/g, '$1');
	// 移除markdown图片 ![alt](url)
	text = text.replace(/!\[([^\]]*)\]\([^\)]*\)/g, '');
	// 移除markdown标题标记
	text = text.replace(/^#{1,6}\s+/gm, '');
	// 移除markdown列表标记
	text = text.replace(/^[\*\-\+]\s+/gm, '');
	text = text.replace(/^\d+\.\s+/gm, '');
	// 移除markdown粗体和斜体标记
	text = text.replace(/\*\*([^\*]*)\*\*/g, '$1');
	text = text.replace(/\*([^\*]*)\*/g, '$1');
	text = text.replace(/__([^_]*)__/g, '$1');
	text = text.replace(/_([^_]*)_/g, '$1');
	// 移除markdown引用标记
	text = text.replace(/^>\s+/gm, '');
	// 移除markdown水平线
	text = text.replace(/^---+/gm, '');
	// 移除HTML标签（如果有）
	text = text.replace(/<[^>]*>/g, '');
	// 移除多余空白字符，只保留一个空格
	text = text.replace(/\s+/g, ' ').trim();
	// 计算中文字符数（包括中文标点）
	const chineseChars = text.match(/[\u4e00-\u9fa5]/g) || [];
	// 计算其他字符（英文、数字等）
	const otherChars = text.replace(/[\u4e00-\u9fa5\s]/g, '').length;
	// 中文字符按1个字符计算，其他字符按0.5个计算（粗略估算）
	return chineseChars.length + Math.ceil(otherChars * 0.5);
}

// 计算预计阅读时间（分钟）
function calculateReadingTime(wordCount) {
	// 中文阅读速度约为每分钟300字
	const wordsPerMinute = 300;
	return Math.max(1, Math.ceil(wordCount / wordsPerMinute));
}

// 格式化日期
function formatDate(dateString) {
	if (!dateString) return '';
	const date = new Date(dateString);
	const year = date.getFullYear();
	const month = String(date.getMonth() + 1).padStart(2, '0');
	const day = String(date.getDate()).padStart(2, '0');
	return `${year}-${month}-${day}`;
}

// 计算属性：文章字数
const wordCount = computed(() => {
	if (!selectedPost.value || !selectedPost.value.content) return 0;
	return calculateWordCount(selectedPost.value.content);
});

// 计算属性：预计阅读时间
const readingTime = computed(() => {
	return calculateReadingTime(wordCount.value);
});

const selectedPost = ref(null);
const selectPost = (post) => {
	selectedPost.value = { ...post };
};

// 检查并选择文章
function checkAndSelectArticle() {
	if (allPosts.value.length === 0) {
		selectedPost.value = null;
		return;
	}
	
	const articleId = route.query.id;
	if (articleId) {
		// 尝试多种类型匹配（字符串或数字）
		const articleIdNum = typeof articleId === 'string' ? parseInt(articleId, 10) : articleId;
		const targetPost = allPosts.value.find(p => {
			const postId = typeof p.id === 'string' ? parseInt(p.id, 10) : p.id;
			return postId === articleIdNum || String(p.id) === String(articleId);
		});
		if (targetPost) {
			selectPost(targetPost);
			return;
		}
	}
	
	// 如果没有指定ID或找不到对应文章，选择第一篇
	if (allPosts.value.length > 0 && !selectedPost.value) {
		selectPost(allPosts.value[0]);
	}
}

// 监听路由变化
watch(() => route.query.id, (newId, oldId) => {
	// 只有当ID真正变化时才重新选择
	if (newId !== oldId && allPosts.value.length > 0) {
		checkAndSelectArticle();
	}
}, { immediate: false });

onMounted(() => {
	loadAllArticles();
});

// 组件卸载前清理定时器
onBeforeUnmount(() => {
	if (searchTimeout) {
		clearTimeout(searchTimeout);
	}
});
</script>

<style scoped>
.posts-layout {
	display: grid;
	grid-template-columns: minmax(0, 1fr);
	gap: 16px;
	align-items: flex-start;
}
.posts-content {
	min-width: 0;
}
@media (min-width: 1024px) {
	.posts-content {
		display: flex;
		flex-direction: column;
		min-height: 0;
		max-height: calc(100vh - 6rem);
	}
	.posts-content > * {
		flex-shrink: 0;
	}
}
.posts-rightbar {
	width: 100%;
}
@media (min-width: 1024px) {
	.posts-layout {
		grid-template-columns: minmax(0, 1fr) 13rem;
	}
	.posts-rightbar {
		max-width: none;
		margin: 0;
	}
}
@media (min-width: 1280px) {
	.posts-layout {
		grid-template-columns: minmax(0, 1fr) 14rem;
	}
}
@media (max-width: 1100px) {
	.posts-rightbar {
		width: 100%;
		margin: 24px 0 0;
	}
	.toc-container {
		max-height: none;
	}
}
@media (max-width: 980px) {
	.posts-layout {
		display: block;
	}
}
.post-item {
	border-radius: 10px;
	padding: 10px;
	cursor: pointer;
	transition: background 0.2s ease;
}
.post-item:hover {
	background: rgba(255,255,255,0.04);
}
.post-item.active {
	background: rgba(59,130,246,0.12);
	border: 1px solid rgba(59,130,246,0.3);
}
.post-item-title {
	font-weight: 600;
}
.post-item-meta {
	font-size: 12px;
	color: rgba(255,255,255,0.6);
	margin-top: 2px;
}
.tag {
	display: inline-block;
	font-size: 12px;
	padding: 2px 8px;
	border-radius: 999px;
	background: rgba(255,255,255,0.08);
	margin-right: 6px;
	margin-top: 6px;
}
.post-content-card {
	min-height: 300px;
	width: 100%;
	max-width: 100%;
}
.post-scroll-container {
	min-height: 0;
}
@media (min-width: 768px) {
	.post-scroll-container {
		overflow-y: auto;
		scrollbar-width: thin;
		scrollbar-color: rgba(255, 255, 255, 0.15) transparent;
		padding-right: 4px;
		flex: 1;
	}
}
.post-scroll-container::-webkit-scrollbar {
	width: 6px;
}
.post-scroll-container::-webkit-scrollbar-track {
	background: transparent;
}
.post-scroll-container::-webkit-scrollbar-thumb {
	background: rgba(255, 255, 255, 0.2);
	border-radius: 3px;
}
.post-scroll-container::-webkit-scrollbar-thumb:hover {
	background: rgba(255, 255, 255, 0.3);
}
.post-header {
	margin-bottom: 24px;
	padding-bottom: 20px;
	border-bottom: 1px solid rgba(255, 255, 255, 0.06);
}
.post-title-wrapper {
	display: flex;
	align-items: center;
	flex-wrap: wrap;
	gap: 12px;
	margin-bottom: 16px;
}
.post-title {
	font-size: 32px;
	font-weight: 700;
	margin: 0;
	line-height: 1.3;
	color: #e6eef6;
}
.post-tags-inline {
	display: flex;
	flex-wrap: wrap;
	gap: 6px;
	align-items: center;
}
.post-summary {
	margin-top: 16px;
}
.post-summary-content {
	font-size: 15px;
	line-height: 1.8;
	color: rgba(255, 255, 255, 0.8);
	padding: 16px 20px;
	border-left: 3px solid rgba(96, 165, 250, 0.6);
	background: rgba(96, 165, 250, 0.08);
	border-radius: 6px;
	font-style: italic;
	position: relative;
	backdrop-filter: blur(4px);
}
.post-meta {
	display: flex;
	align-items: center;
	gap: 8px;
	font-size: 14px;
	color: rgba(255, 255, 255, 0.7);
	flex-wrap: wrap;
	line-height: 1.6;
}
.post-meta .meta-label {
	color: rgba(255, 255, 255, 0.5);
	font-weight: 500;
}
.post-tags {
	display: flex;
	flex-wrap: wrap;
	gap: 6px;
	align-items: center;
	margin-top: 12px;
}
.toc-container {
	max-height: calc(100vh - 8rem);
	display: flex;
	flex-direction: column;
}
.post-list {
	max-height: calc(100vh - 12rem);
	overflow-y: auto;
	overflow-x: hidden;
	padding-right: 4px;
}
.post-list::-webkit-scrollbar {
	width: 6px;
}
.post-list::-webkit-scrollbar-track {
	background: rgba(255, 255, 255, 0.05);
	border-radius: 3px;
}
.post-list::-webkit-scrollbar-thumb {
	background: rgba(255, 255, 255, 0.2);
	border-radius: 3px;
}
.post-list::-webkit-scrollbar-thumb:hover {
	background: rgba(255, 255, 255, 0.3);
}

/* Markdown 内容样式 */
.post-body {
	width: 100%;
	max-width: 100%;
}

.post-body :deep(.prose) {
	max-width: 100% !important;
	width: 100%;
}

.post-body.prose {
	max-width: 100% !important;
	width: 100%;
}

.post-body :deep(h1),
.post-body :deep(h2),
.post-body :deep(h3),
.post-body :deep(h4),
.post-body :deep(h5),
.post-body :deep(h6) {
	color: #e6eef6;
	margin-top: 1.5em;
	margin-bottom: 0.5em;
	font-weight: 600;
	line-height: 1.25;
}

.post-body :deep(h1) {
	font-size: 2em;
	border-bottom: 1px solid rgba(255, 255, 255, 0.1);
	padding-bottom: 0.3em;
}

.post-body :deep(h2) {
	font-size: 1.5em;
	border-bottom: 1px solid rgba(255, 255, 255, 0.1);
	padding-bottom: 0.3em;
}

.post-body :deep(p) {
	margin: 1em 0;
	line-height: 1.8;
	color: rgba(255, 255, 255, 0.8);
}

.post-body :deep(strong) {
	font-weight: 600;
	color: #e6eef6;
}

.post-body :deep(em) {
	font-style: italic;
}

.post-body :deep(code) {
	background: rgba(255, 255, 255, 0.1);
	padding: 0.2em 0.4em;
	border-radius: 3px;
	font-size: 0.9em;
	font-family: 'Courier New', monospace;
	color: #60a5fa;
}

.post-body :deep(pre) {
	background: rgba(0, 0, 0, 0.3);
	border: 1px solid rgba(255, 255, 255, 0.1);
	border-radius: 8px;
	padding: 1em;
	overflow-x: auto;
	margin: 1.5em 0;
}

.post-body :deep(pre code) {
	background: transparent;
	padding: 0;
	color: #e6eef6;
	font-size: 0.9em;
}

.post-body :deep(blockquote) {
	border-left: 4px solid rgba(96, 165, 250, 0.5);
	padding-left: 1em;
	margin: 1.5em 0;
	color: rgba(255, 255, 255, 0.7);
	font-style: italic;
	background: rgba(255, 255, 255, 0.02);
	padding: 1em;
	border-radius: 4px;
}

.post-body :deep(ul),
.post-body :deep(ol) {
	margin: 1em 0;
	padding-left: 2em;
}

.post-body :deep(ul) {
	list-style-type: disc;
}

.post-body :deep(ol) {
	list-style-type: decimal;
}

.post-body :deep(li) {
	margin: 0.5em 0;
	line-height: 1.8;
	color: rgba(255, 255, 255, 0.8);
	display: list-item;
}

.post-body :deep(a) {
	color: #60a5fa;
	text-decoration: underline;
	transition: opacity 0.2s;
}

.post-body :deep(a:hover) {
	opacity: 0.8;
}

.post-body :deep(img) {
	max-width: 100%;
	height: auto;
	border-radius: 8px;
	margin: 1.5em 0;
}

.post-body :deep(table) {
	width: 100%;
	border-collapse: collapse;
	margin: 1.5em 0;
	border: 1px solid rgba(255, 255, 255, 0.1);
}

.post-body :deep(th),
.post-body :deep(td) {
	border: 1px solid rgba(255, 255, 255, 0.1);
	padding: 0.75em;
	text-align: left;
}

.post-body :deep(th) {
	background: rgba(255, 255, 255, 0.05);
	font-weight: 600;
	color: #e6eef6;
}

.post-body :deep(hr) {
	border: none;
	border-top: 1px solid rgba(255, 255, 255, 0.1);
	margin: 2em 0;
}

/* 搜索结果下拉框样式 */
.search-dropdown {
	box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.5), 0 10px 10px -5px rgba(0, 0, 0, 0.2);
}

.search-dropdown::-webkit-scrollbar {
	width: 8px;
}

.search-dropdown::-webkit-scrollbar-track {
	background: rgba(255, 255, 255, 0.05);
	border-radius: 4px;
}

.search-dropdown::-webkit-scrollbar-thumb {
	background: rgba(255, 255, 255, 0.2);
	border-radius: 4px;
}

.search-dropdown::-webkit-scrollbar-thumb:hover {
	background: rgba(255, 255, 255, 0.3);
}

.search-result-item {
	transition: background-color 0.15s ease;
}

.search-result-item:last-child {
	border-bottom: none;
}

.search-result-title {
	font-size: 15px;
	line-height: 1.4;
}

.search-result-highlight {
	color: rgba(255, 255, 255, 0.85);
	line-height: 1.6;
	display: -webkit-box;
	-webkit-line-clamp: 3;
	line-clamp: 3;
	-webkit-box-orient: vertical;
	overflow: hidden;
}

.search-result-highlight :deep(em) {
	color: #7dd3fc;
	font-style: normal;
}

.search-result-excerpt {
	color: rgba(255, 255, 255, 0.7);
	line-height: 1.5;
	display: -webkit-box;
	-webkit-line-clamp: 2;
	line-clamp: 2;
	-webkit-box-orient: vertical;
	overflow: hidden;
}

.search-result-tags {
	display: flex;
	flex-wrap: wrap;
	gap: 4px;
}
</style>
