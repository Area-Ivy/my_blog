<template>
	<div class="min-h-screen w-full overflow-hidden text-white relative">
		<SiteHeader />
		<div class="flex min-h-screen pt-[2.75rem] md:pt-[3.75rem]">
			<SideNav />
			<main
				class="home-scroll flex-1 px-6 pt-6 pb-10 md:px-8 lg:ml-52 lg:px-10 xl:ml-56 xl:px-12 h-[calc(100vh-2.75rem)] md:h-[calc(100vh-3.75rem)] overflow-y-auto"
			>
				<ClientOnly>
					<BlurReveal
						:delay="0.1"
						:duration="0.75"
						class="flex flex-col gap-8"
					>
						<section>
							<div class="max-w-5xl">
								<h1 class="text-2xl font-bold md:text-4xl">欢迎来到我的博客</h1>
								<p class="mt-3 text-white/80 md:text-base">
									探索这里的主要版块：文章、足迹、工具和关于。每个部分都呈现我正在做的事与思考。
								</p>
							</div>
						</section>

						<section>
							<div class="mb-8 max-w-6xl">
								<div class="grid grid-cols-2 gap-4 md:grid-cols-4">
									<div class="rounded-xl border border-white/10 bg-white/5 p-4 backdrop-blur">
										<div class="flex items-center gap-3">
											<img src="/post.png" alt="文章" class="w-8 h-8 opacity-80" />
											<div>
												<div class="text-2xl font-bold">{{ stats.articles }}</div>
												<div class="text-sm text-white/60">文章</div>
											</div>
										</div>
									</div>
									<div class="rounded-xl border border-white/10 bg-white/5 p-4 backdrop-blur">
										<div class="flex items-center gap-3">
											<img src="/tool.png" alt="工具" class="w-8 h-8 opacity-80" />
											<div>
												<div class="text-2xl font-bold">{{ stats.tools }}</div>
												<div class="text-sm text-white/60">工具</div>
											</div>
										</div>
									</div>
									<div class="rounded-xl border border-white/10 bg-white/5 p-4 backdrop-blur">
										<div class="flex items-center gap-3">
											<img src="/footprint.png" alt="足迹" class="w-8 h-8 opacity-80" />
											<div>
												<div class="text-2xl font-bold">{{ stats.footprints }}</div>
												<div class="text-sm text-white/60">足迹</div>
											</div>
										</div>
									</div>
									<div class="rounded-xl border border-white/10 bg-white/5 p-4 backdrop-blur">
										<div class="flex items-center gap-3">
											<img src="/about.png" alt="更新" class="w-8 h-8 opacity-80" />
											<div>
												<div class="text-2xl font-bold">{{ stats.lastUpdate }}</div>
												<div class="text-sm text-white/60">最近更新</div>
											</div>
										</div>
									</div>
								</div>
							</div>

							<div class="mb-6 max-w-6xl">
								<h2 class="text-xl font-semibold text-white/90">快速导航</h2>
							</div>

							<div class="grid max-w-6xl grid-cols-1 gap-4 md:grid-cols-2">
								<div class="nav-card rounded-xl border border-white/10 bg-white/5 p-5 backdrop-blur transition-all duration-300 cursor-pointer">
									<img src="/post.png" alt="文章" class="w-10 h-10 mb-3 transition-transform duration-300" />
									<h3 class="text-lg font-semibold">文章</h3>
									<p class="mt-2 text-white/70">记录工程实践、系统设计、个人学习笔记与思考。</p>
									<InteractiveHoverButton
										class="mt-4"
										text="进入文章"
										@click="goTo('/posts')"
									/>
								</div>
								<div class="nav-card rounded-xl border border-white/10 bg-white/5 p-5 backdrop-blur transition-all duration-300 cursor-pointer">
									<img src="/tool.png" alt="工具" class="w-10 h-10 mb-3 transition-transform duration-300" />
									<h3 class="text-lg font-semibold">工具</h3>
									<p class="mt-2 text-white/70">整理常用的在线工具、组件库或云平台，提升效率。</p>
									<InteractiveHoverButton
										class="mt-4"
										text="探索工具"
										@click="goTo('/tools')"
									/>
								</div>
								<div class="nav-card rounded-xl border border-white/10 bg-white/5 p-5 backdrop-blur transition-all duration-300 cursor-pointer">
									<img src="/footprint.png" alt="足迹" class="w-10 h-10 mb-3 transition-transform duration-300" />
									<h3 class="text-lg font-semibold">足迹</h3>
									<p class="mt-2 text-white/70">查看时间轴，记录里程碑与生活片段。</p>
									<InteractiveHoverButton
										class="mt-4"
										text="查看足迹"
										@click="goTo('/footprints')"
									/>
								</div>
								<div class="nav-card rounded-xl border border-white/10 bg-white/5 p-5 backdrop-blur transition-all duration-300 cursor-pointer">
									<img src="/about.png" alt="关于" class="w-10 h-10 mb-3 transition-transform duration-300" />
									<h3 class="text-lg font-semibold">关于</h3>
									<p class="mt-2 text-white/70">了解我的背景、擅长领域、创作理念和联系方式。</p>
									<InteractiveHoverButton
										class="mt-4"
										text="更多关于我"
										@click="goTo('/about')"
									/>
								</div>
							</div>
						</section>

						<section>
							<div class="mb-6 max-w-6xl">
								<h2 class="text-xl font-semibold text-white/90">文章推荐</h2>
							</div>
							<div v-if="recommendedArticles.length > 0" class="grid max-w-6xl grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
								<div
									v-for="article in recommendedArticles"
									:key="article.id"
									class="article-card rounded-xl border border-white/10 bg-white/5 p-5 backdrop-blur transition-all duration-300 cursor-pointer"
									@click="goToArticle(article.id)"
								>
									<h3 class="text-lg font-semibold line-clamp-2 mb-2">{{ article.title }}</h3>
									<p class="text-sm text-white/60 mb-3">{{ article.date }}</p>
									<p class="text-sm text-white/70 line-clamp-2 mb-4">{{ article.excerpt || '暂无摘要' }}</p>
									<div v-if="article.tags && article.tags.length > 0" class="flex flex-wrap gap-2">
										<span
											v-for="tag in article.tags.slice(0, 3)"
											:key="tag"
											class="text-xs px-2 py-1 rounded-full bg-white/10 text-white/70"
										>
											{{ tag }}
										</span>
									</div>
								</div>
							</div>
							<div v-else class="max-w-6xl rounded-xl border border-white/10 bg-white/5 p-8 backdrop-blur text-center">
								<p class="text-white/60">暂无推荐文章</p>
							</div>
						</section>

						<section>
							<div class="mb-6 max-w-6xl">
								<h2 class="text-xl font-semibold text-white/90">关于博客</h2>
							</div>
							
							<!-- 架构概览 -->
							<div class="mb-6 max-w-6xl">
								<div class="tech-card rounded-xl border border-white/10 bg-gradient-to-br from-white/5 to-white/[0.02] p-6 backdrop-blur">
									<div class="flex items-center gap-3 mb-4">
										<div class="w-10 h-10 rounded-lg bg-gradient-to-br from-blue-500/20 to-purple-500/20 flex items-center justify-center">
											<svg class="w-6 h-6 text-blue-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
												<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path>
											</svg>
										</div>
										<h3 class="text-lg font-semibold">架构设计</h3>
									</div>
									<p class="text-white/70 text-sm leading-relaxed">
										采用 Vue 3 + Vite 构建纯静态单页应用。文章以 Markdown 保存，工具、足迹和播放列表使用 JSON 管理，
										搜索直接在浏览器中完成，并由 Cloudflare Pages 自动构建和发布，无需常驻服务器与数据库。
									</p>
								</div>
							</div>

							<!-- 技术栈展示 -->
							<div class="grid max-w-6xl grid-cols-1 gap-4 md:grid-cols-2">
								<!-- 前端技术栈 -->
								<div class="tech-card rounded-xl border border-white/10 bg-white/5 p-5 backdrop-blur transition-all duration-300">
									<div class="flex items-center gap-3 mb-4">
										<div class="w-10 h-10 rounded-lg bg-gradient-to-br from-green-500/20 to-emerald-500/20 flex items-center justify-center">
											<svg class="w-6 h-6 text-green-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
												<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
											</svg>
										</div>
										<h3 class="text-lg font-semibold">前端技术栈</h3>
									</div>
									<div class="space-y-3">
										<div class="flex items-center gap-2">
											<span class="text-xs px-2 py-1 rounded-md bg-green-500/10 text-green-400 border border-green-500/20">Vue 3</span>
											<span class="text-xs px-2 py-1 rounded-md bg-green-500/10 text-green-400 border border-green-500/20">Vite</span>
											<span class="text-xs px-2 py-1 rounded-md bg-green-500/10 text-green-400 border border-green-500/20">Vue Router</span>
										</div>
										<div class="flex items-center gap-2 flex-wrap">
											<span class="text-xs px-2 py-1 rounded-md bg-blue-500/10 text-blue-400 border border-blue-500/20">Tailwind CSS</span>
											<span class="text-xs px-2 py-1 rounded-md bg-blue-500/10 text-blue-400 border border-blue-500/20">Marked</span>
											<span class="text-xs px-2 py-1 rounded-md bg-blue-500/10 text-blue-400 border border-blue-500/20">Motion-v</span>
										</div>
										<div class="flex items-center gap-2 flex-wrap">
											<span class="text-xs px-2 py-1 rounded-md bg-purple-500/10 text-purple-400 border border-purple-500/20">VueUse</span>
											<span class="text-xs px-2 py-1 rounded-md bg-purple-500/10 text-purple-400 border border-purple-500/20">Number Flow</span>
										</div>
									</div>
								</div>

								<!-- 后端技术栈 -->
								<div class="tech-card rounded-xl border border-white/10 bg-white/5 p-5 backdrop-blur transition-all duration-300">
									<div class="flex items-center gap-3 mb-4">
										<div class="w-10 h-10 rounded-lg bg-gradient-to-br from-orange-500/20 to-red-500/20 flex items-center justify-center">
											<svg class="w-6 h-6 text-orange-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
												<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 12h14M5 12a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v4a2 2 0 01-2 2M5 12a2 2 0 00-2 2v4a2 2 0 002 2h14a2 2 0 002-2v-4a2 2 0 00-2-2m-2-4h.01M17 16h.01"></path>
											</svg>
										</div>
									<h3 class="text-lg font-semibold">内容管理</h3>
									</div>
									<div class="space-y-3">
										<div class="flex items-center gap-2 flex-wrap">
											<span class="text-xs px-2 py-1 rounded-md bg-orange-500/10 text-orange-400 border border-orange-500/20">Markdown</span>
											<span class="text-xs px-2 py-1 rounded-md bg-orange-500/10 text-orange-400 border border-orange-500/20">JSON</span>
											<span class="text-xs px-2 py-1 rounded-md bg-orange-500/10 text-orange-400 border border-orange-500/20">Git</span>
										</div>
										<div class="flex items-center gap-2 flex-wrap">
											<span class="text-xs px-2 py-1 rounded-md bg-red-500/10 text-red-400 border border-red-500/20">Frontmatter</span>
											<span class="text-xs px-2 py-1 rounded-md bg-red-500/10 text-red-400 border border-red-500/20">Marked</span>
										</div>
										<div class="flex items-center gap-2 flex-wrap">
											<span class="text-xs px-2 py-1 rounded-md bg-yellow-500/10 text-yellow-400 border border-yellow-500/20">浏览器端搜索</span>
										</div>
									</div>
								</div>

								<!-- 数据库与存储 -->
								<div class="tech-card rounded-xl border border-white/10 bg-white/5 p-5 backdrop-blur transition-all duration-300">
									<div class="flex items-center gap-3 mb-4">
										<div class="w-10 h-10 rounded-lg bg-gradient-to-br from-cyan-500/20 to-blue-500/20 flex items-center justify-center">
											<svg class="w-6 h-6 text-cyan-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
												<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 7v10c0 2.21 3.582 4 8 4s8-1.79 8-4V7M4 7c0 2.21 3.582 4 8 4s8-1.79 8-4M4 7c0-2.21 3.582-4 8-4s8 1.79 8 4m0 5c0 2.21-3.582 4-8 4s-8-1.79-8-4"></path>
											</svg>
										</div>
										<h3 class="text-lg font-semibold">数据存储</h3>
									</div>
									<div class="space-y-2">
										<div class="flex items-center gap-2">
											<span class="text-xs px-2 py-1 rounded-md bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">GitHub</span>
											<span class="text-white/60 text-xs">版本管理文章、工具、足迹和静态资源</span>
										</div>
										<div class="flex items-center gap-2">
											<span class="text-xs px-2 py-1 rounded-md bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">静态资源</span>
											<span class="text-white/60 text-xs">随构建产物发布，无需独立数据库和对象存储</span>
										</div>
									</div>
								</div>

								<!-- 部署与运维 -->
								<div class="tech-card rounded-xl border border-white/10 bg-white/5 p-5 backdrop-blur transition-all duration-300">
									<div class="flex items-center gap-3 mb-4">
										<div class="w-10 h-10 rounded-lg bg-gradient-to-br from-indigo-500/20 to-violet-500/20 flex items-center justify-center">
											<svg class="w-6 h-6 text-indigo-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
												<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path>
											</svg>
										</div>
										<h3 class="text-lg font-semibold">部署与运维</h3>
									</div>
									<div class="space-y-2">
										<div class="flex items-center gap-2">
											<span class="text-xs px-2 py-1 rounded-md bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">Cloudflare Pages</span>
											<span class="text-white/60 text-xs">Git 推送后自动构建并部署到全球网络</span>
										</div>
										<div class="flex items-center gap-2">
											<span class="text-xs px-2 py-1 rounded-md bg-indigo-500/10 text-indigo-400 border border-indigo-500/20">自动 HTTPS</span>
											<span class="text-white/60 text-xs">自定义域名、证书与 CDN 均由平台托管</span>
										</div>
									</div>
								</div>
							</div>
						</section>

						<section>
							<div class="mb-6 max-w-6xl">
								<h2 class="text-xl font-semibold text-white/90">了解更多</h2>
							</div>
							
							<div class="grid max-w-6xl grid-cols-1 gap-4 md:grid-cols-2">
								<!-- GitHub -->
								<a 
									href="https://github.com/Area-Ivy" 
									target="_blank" 
									rel="noopener noreferrer"
									class="link-card rounded-xl border border-white/10 bg-white/5 p-5 backdrop-blur transition-all duration-300 cursor-pointer group"
								>
									<div class="flex items-center gap-3 mb-3">
										<div class="w-10 h-10 rounded-lg bg-gradient-to-br from-gray-500/20 to-slate-500/20 flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
											<svg class="w-6 h-6 text-gray-300" fill="currentColor" viewBox="0 0 24 24">
												<path fill-rule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z" clip-rule="evenodd"></path>
											</svg>
										</div>
										<h3 class="text-lg font-semibold text-white">GitHub</h3>
									</div>
									<p class="text-white/60 text-sm">查看我的开源项目和代码仓库</p>
									<div class="mt-3 flex items-center text-xs text-white/50 group-hover:text-white/70 transition-colors">
										<span>访问主页</span>
										<svg class="w-4 h-4 ml-1 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
											<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
										</svg>
									</div>
								</a>

								<!-- 邮箱 -->
								<a 
									href="mailto:chenyiming12500@gmail.com" 
									class="link-card rounded-xl border border-white/10 bg-white/5 p-5 backdrop-blur transition-all duration-300 cursor-pointer group"
								>
									<div class="flex items-center gap-3 mb-3">
										<div class="w-10 h-10 rounded-lg bg-gradient-to-br from-gray-500/20 to-slate-500/20 flex items-center justify-center group-hover:scale-110 transition-transform duration-300">
											<svg class="w-6 h-6 text-white/80" fill="none" stroke="currentColor" viewBox="0 0 24 24">
												<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path>
											</svg>
										</div>
										<h3 class="text-lg font-semibold text-white">邮箱联系</h3>
									</div>
									<p class="text-white/60 text-sm">通过邮件与我取得联系</p>
									<div class="mt-3 flex items-center text-xs text-white/50 group-hover:text-white/70 transition-colors">
										<span>发送邮件</span>
										<svg class="w-4 h-4 ml-1 group-hover:translate-x-1 transition-transform" fill="none" stroke="currentColor" viewBox="0 0 24 24">
											<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7"></path>
										</svg>
									</div>
								</a>
								<br>
							</div>
						</section>


					</BlurReveal>
				</ClientOnly>
			</main>
		</div>
	</div>
</template>

<script setup>
import { ref } from 'vue';
import SiteHeader from '@/components/SiteHeader.vue';
import SideNav from '@/components/SideNav.vue';
import ClientOnly from '@/components/ClientOnly.vue';
import BlurReveal from '@/components/BlurReveal.vue';
import InteractiveHoverButton from '@/components/InteractiveHoverButton.vue';
import { useRouter } from 'vue-router';
import { articles, tools, footprints } from '@/lib/content';

const router = useRouter();
const goTo = (path) => {
	router.push(path);
};

const goToArticle = (articleId) => {
	router.push({
		path: '/posts',
		query: { id: articleId }
	});
};

const stats = ref({
	articles: articles.length,
	tools: tools.length,
	footprints: footprints.length,
	lastUpdate: articles[0]?.date || '--'
});

const recommendedArticles = ref(articles.slice(0, 3));
</script>

<style scoped>
.nav-card {
	transition: all 0.3s ease;
}

.nav-card:hover {
	background: rgba(255, 255, 255, 0.08);
	border-color: rgba(255, 255, 255, 0.2);
	transform: translateY(-4px);
	box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
}

.nav-card:hover img {
	transform: scale(1.1);
}

.article-card {
	transition: all 0.3s ease;
}

.article-card:hover {
	background: rgba(255, 255, 255, 0.08);
	border-color: rgba(255, 255, 255, 0.2);
	transform: translateY(-4px);
	box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
}

.tech-card {
	transition: all 0.3s ease;
}

.tech-card:hover {
	background: rgba(255, 255, 255, 0.08);
	border-color: rgba(255, 255, 255, 0.2);
	transform: translateY(-4px);
	box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
}

.link-card {
	transition: all 0.3s ease;
	text-decoration: none;
}

.link-card:hover {
	background: rgba(255, 255, 255, 0.08);
	border-color: rgba(255, 255, 255, 0.2);
	transform: translateY(-4px);
	box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
}

.line-clamp-2 {
	display: -webkit-box;
	-webkit-line-clamp: 2;
	line-clamp: 2;
	-webkit-box-orient: vertical;
	overflow: hidden;
}
</style>
