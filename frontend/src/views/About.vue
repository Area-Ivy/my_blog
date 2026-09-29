<template>
	<div class="min-h-screen w-full overflow-x-hidden text-white relative">
		<SiteHeader />
		<div class="flex pt-[2.75rem] md:pt-[3.75rem]">
			<SideNav />
			<main class="home-scroll flex-1 pt-8 px-6 md:px-8 lg:ml-52 lg:px-10 xl:ml-56 xl:px-12 h-[calc(100vh-2.75rem)] md:h-[calc(100vh-3.75rem)] overflow-y-auto">
				<ClientOnly>
					<div class="flex flex-col gap-6 max-w-6xl w-full pb-12">
						<!-- 顶部头像和信息区域 (GitHub 风格) -->
						<BlurReveal
							:delay="0.1"
							:duration="0.75"
							class="w-full"
						>
							<div class="flex flex-col sm:flex-row items-start gap-6 pb-6 border-b border-white/10">
								<!-- 头像 -->
								<div class="relative flex-shrink-0 avatar-wrapper">
									<div class="avatar-glow"></div>
									<div class="avatar-ring"></div>
									<div class="avatar-orbit avatar-orbit-1"></div>
									<div class="avatar-orbit avatar-orbit-2"></div>
									<div
										class="relative h-32 w-32 rounded-full overflow-hidden border-2 border-white/20 transition-transform duration-300 hover:scale-105 bg-black/20"
										>
											<div
												class="absolute inset-0 bg-[url('/avatar.png')] bg-cover bg-center"
											></div>
									</div>
								</div>
								
								<!-- 基本信息 -->
								<div class="flex-1 space-y-3">
									<div>
										<h1 class="text-2xl md:text-3xl font-bold text-white mb-1">
											Hi there!👋
											</h1>
										<p class="text-base text-white/70">
											后端工程师，嘎啦给木领域大神
										</p>
									</div>
									
									<!-- 年份进度条 -->
									<div class="rounded-lg border border-white/10 bg-white/5 p-4 backdrop-blur-sm">
										<div class="flex items-center gap-2 text-sm text-white/80 mb-2">
											<span>⏳</span>
											<span>年度进度 {{ progressBarOfThisYear }} {{ progressPercentage }}%</span>
										</div>
										<div class="text-xs text-white/50">
											⏰ 更新于 {{ lastUpdateTime }}
										</div>
									</div>
								</div>
							</div>
						</BlurReveal>

						<!-- About Me -->
						<BlurReveal
							:delay="0.2"
							:duration="0.75"
							class="w-full"
						>
							<div class="rounded-xl border border-white/10 bg-white/5 p-6 backdrop-blur-sm">
								<h2 class="text-xl font-bold text-white mb-4 flex items-center gap-2">
									<span>👨‍💻</span>
									<span>关于我</span>
								</h2>
								<ul class="space-y-3 text-white/80 text-sm leading-relaxed">
									<li class="flex items-start gap-2">
										<span class="text-white/60">•</span>
										<span>🚀 <a href="https://www.tongji.edu.cn" target="_blank" class="text-sky-400 hover:underline">同济大学</a>计算机科学与技术学院，软件工程专业。</span>
									</li>
									<li class="flex items-start gap-2">
										<span class="text-white/60">•</span>
										<span>🌱 专注于后端开发、算法学习和开源贡献。</span>
									</li>
									<li class="flex items-start gap-2">
										<span class="text-white/60">•</span>
										<span>🔭 始终热衷于学习新技术，并乐于接受具有挑战性的项目。</span>
									</li>
									<li class="flex items-start gap-2">
										<span class="text-white/60">•</span>
										<span>📫 邮箱：<a href="mailto:chenyiming12500@gmail.com" class="text-sky-400 hover:underline">chenyiming12500@gmail.com</a></span>
									</li>
									<li class="flex items-start gap-2">
										<span class="text-white/60">•</span>
										<span>💡 GitHub：<a href="https://github.com/Area-Ivy" target="_blank" class="text-sky-400 hover:underline">https://github.com/Area-Ivy</a></span>
									</li>
								</ul>
							</div>
						</BlurReveal>

						<!-- Timeline -->
						<BlurReveal
							:delay="0.5"
							:duration="0.75"
							class="w-full"
						>
							<div class="rounded-xl border border-white/10 bg-white/5 p-6 backdrop-blur-sm">
								<h2 class="text-xl font-bold text-white mb-6 flex items-center gap-2">
									<span>📅</span>
									<span>时间轴</span>
								</h2>
								<div class="timeline-container relative space-y-6">
									<!-- Timeline Item 1 -->
									<div class="timeline-item group/item relative pl-6">
										<div
											class="absolute left-0 top-2 h-3 w-3 rounded-full bg-emerald-400 border-2 border-white/20 transition-all duration-300 group-hover/item:scale-125 group-hover/item:bg-emerald-300"
										></div>
										<div class="space-y-1">
											<p class="text-xs uppercase tracking-wider text-emerald-400/70 font-semibold">
												2018 - 开始
											</p>
											<p class="text-base font-semibold text-white/95">
												踏入编程世界
											</p>
											<p class="text-sm text-white/70 leading-relaxed">
												开始学习编程，对计算机产生浓厚兴趣。
											</p>
										</div>
									</div>

									<!-- Timeline Item 2 -->
									<div class="timeline-item group/item relative pl-6">
										<div
											class="absolute left-0 top-2 h-3 w-3 rounded-full bg-sky-400 border-2 border-white/20 transition-all duration-300 group-hover/item:scale-125 group-hover/item:bg-sky-300"
										></div>
										<div class="space-y-1">
											<p class="text-xs uppercase tracking-wider text-sky-400/70 font-semibold">
												2024 - 成长
											</p>
											<p class="text-base font-semibold text-white/95">
												深入学习Web开发
											</p>
											<p class="text-sm text-white/70 leading-relaxed">
												开始系统学习前端和后端技术，完成多个个人与团队项目。
											</p>
										</div>
									</div>

									<!-- Timeline Item 3 -->
									<div class="timeline-item group/item relative pl-6">
										<div
											class="absolute left-0 top-2 h-3 w-3 rounded-full bg-violet-400 border-2 border-white/20 transition-all duration-300 group-hover/item:scale-125 group-hover/item:bg-violet-300"
										></div>
										<div class="space-y-1">
											<p class="text-xs uppercase tracking-wider text-violet-400/70 font-semibold">
												2025 - 现在
											</p>
											<p class="text-base font-semibold text-white/95">
												探索高性能架构与AI Agent
											</p>
											<p class="text-sm text-white/70 leading-relaxed">
												专注系统设计和工程实践，通过博客分享技术思考。
											</p>
										</div>
									</div>
								</div>
							</div>
						</BlurReveal>

					</div>
				</ClientOnly>
			</main>
		</div>
	</div>
</template>

<script setup>
import { computed } from 'vue';
import SiteHeader from '@/components/SiteHeader.vue';
import SideNav from '@/components/SideNav.vue';
import ClientOnly from '@/components/ClientOnly.vue';
import BlurReveal from '@/components/BlurReveal.vue';

// 年份进度条
const thisYear = new Date().getFullYear();
const startTimeOfThisYear = new Date(`${thisYear}-01-01T00:00:00+00:00`).getTime();
const endTimeOfThisYear = new Date(`${thisYear}-12-31T23:59:59+00:00`).getTime();
const progressOfThisYear = computed(() => {
	return (Date.now() - startTimeOfThisYear) / (endTimeOfThisYear - startTimeOfThisYear);
});

const progressBarOfThisYear = computed(() => {
	const progressBarCapacity = 30;
	const passedProgressBarIndex = parseInt(progressOfThisYear.value * progressBarCapacity);
	const progressBar = '▇'.repeat(passedProgressBarIndex) + '▁'.repeat(progressBarCapacity - passedProgressBarIndex);
	return `[ ${progressBar} ]`;
});

const progressPercentage = computed(() => {
	return (progressOfThisYear.value * 100).toFixed(2);
});

const lastUpdateTime = computed(() => {
	const date = new Date();
	const year = date.getFullYear();
	const month = String(date.getMonth() + 1).padStart(2, '0');
	const day = String(date.getDate()).padStart(2, '0');
	const hours = String(date.getHours()).padStart(2, '0');
	const minutes = String(date.getMinutes()).padStart(2, '0');
	return `${year}年${month}月${day}日 ${hours}:${minutes}`;
});
</script>

<style scoped>
/* 径向渐变背景 */
.bg-gradient-radial {
	background: radial-gradient(circle, var(--tw-gradient-stops));
}

/* 时间轴容器 */
.timeline-container::before {
	content: '';
	position: absolute;
	left: 5px;
	top: 8px;
	bottom: 8px;
	width: 2px;
	background: linear-gradient(
		to bottom,
		rgba(16, 185, 129, 0.5),
		rgba(56, 189, 248, 0.5),
		rgba(129, 140, 248, 0.5)
	);
	border-radius: 2px;
}


/* 平滑过渡效果 */
@keyframes fadeIn {
	from {
		opacity: 0;
		transform: translateY(10px);
	}
	to {
		opacity: 1;
		transform: translateY(0);
	}
}

/* 增强卡片悬停效果 */
.group:hover .group-hover\:opacity-100 {
	opacity: 1;
}

/* 平滑的光晕效果 */
@keyframes glow {
	0%, 100% {
		opacity: 0.5;
	}
	50% {
		opacity: 0.8;
	}
}

/* 确保渐变文字显示正确 */
.bg-clip-text {
	-webkit-background-clip: text;
	background-clip: text;
}

/* 头像装饰 */
.avatar-wrapper {
	width: 8.5rem;
	height: 8.5rem;
	display: flex;
	align-items: center;
	justify-content: center;
	position: relative;
}

.avatar-glow {
	position: absolute;
	inset: -20%;
	background: radial-gradient(circle, rgba(56, 189, 248, 0.4), rgba(99, 102, 241, 0.15));
	filter: blur(20px);
	animation: pulseGlow 6s ease-in-out infinite;
}

.avatar-ring {
	position: absolute;
	inset: -10px;
	border-radius: 9999px;
	border: 2px dashed rgba(255, 255, 255, 0.25);
	animation: spinSlow 14s linear infinite;
}

.avatar-orbit {
	position: absolute;
	width: 10px;
	height: 10px;
	border-radius: 9999px;
	background: linear-gradient(135deg, #34d399, #22d3ee);
	box-shadow: 0 0 12px rgba(34, 211, 238, 0.6);
	animation: orbit 9s linear infinite;
}

.avatar-orbit-1 {
	top: -6px;
	left: 50%;
	transform-origin: -20px 40px;
}

.avatar-orbit-2 {
	bottom: 0;
	right: -8px;
	width: 12px;
	height: 12px;
	transform-origin: 20px -30px;
	animation-duration: 12s;
	background: linear-gradient(135deg, #a855f7, #38bdf8);
}

@keyframes spinSlow {
	from {
		transform: rotate(0deg);
	}
	to {
		transform: rotate(360deg);
	}
}

@keyframes orbit {
	from {
		transform: rotate(0deg);
	}
	to {
		transform: rotate(360deg);
	}
}

@keyframes pulseGlow {
	0%, 100% {
		opacity: 0.4;
	}
	50% {
		opacity: 0.9;
	}
}
</style>


