<template>
	<header class="site-header fixed inset-x-0 top-0 z-20 border-b backdrop-blur-md shadow-lg">
		<div class="relative flex min-h-[2.75rem] w-full max-w-none items-center gap-4 pl-2 pr-0 py-2 md:min-h-[3.75rem] md:pl-6 md:pr-0 md:py-3">
			<RouterLink to="/" class="site-header__brand flex items-center gap-2 font-bold text-sm md:text-base">
				<img
					src="/logo.png"
					alt="Area-Ivy logo"
					class="h-7 w-auto object-contain md:h-8"
				/>
				<span>Area-Ivy's Blog</span>
			</RouterLink>
			<nav class="hidden md:flex absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 items-center justify-center gap-6 lg:gap-10">
				<RouterLink class="site-header__nav-link font-bold" to="/home">主页</RouterLink>
				<RouterLink class="site-header__nav-link font-bold" to="/posts">文章</RouterLink>
				<RouterLink class="site-header__nav-link font-bold" to="/tools">工具</RouterLink>
				<RouterLink class="site-header__nav-link font-bold" to="/footprints">足迹</RouterLink>
				<RouterLink class="site-header__nav-link font-bold" to="/about">关于</RouterLink>
			</nav>
			<div class="ml-auto mr-4 flex items-center gap-2 text-xs md:text-sm">
				<button
					type="button"
					class="theme-toggle"
					:aria-label="theme === 'dark' ? '切换到白天模式' : '切换到夜间模式'"
					:title="theme === 'dark' ? '切换到白天模式' : '切换到夜间模式'"
					@click="toggleTheme"
				>
					<svg v-if="theme === 'dark'" viewBox="0 0 24 24" aria-hidden="true">
						<circle cx="12" cy="12" r="4" />
						<path d="M12 2v2M12 20v2M4.93 4.93l1.42 1.42M17.66 17.66l1.41 1.41M2 12h2M20 12h2M4.93 19.07l1.42-1.42M17.66 6.34l1.41-1.41" />
					</svg>
					<svg v-else viewBox="0 0 24 24" aria-hidden="true">
						<path d="M20.5 14.2A8.5 8.5 0 0 1 9.8 3.5 8.5 8.5 0 1 0 20.5 14.2Z" />
					</svg>
				</button>
				<!--
				<RouterLink
					class="inline-flex rounded-full border border-emerald-400/40 px-3 py-1.5 text-emerald-200 transition hover:border-emerald-300 hover:text-white"
					to="/console"
				>
					控制台
				</RouterLink>
				-->
				<a
					class="site-header__action hidden rounded-full border px-3 py-1.5 transition md:inline-flex"
					href="https://github.com/Area-Ivy"
					target="_blank"
					rel="noopener noreferrer"
				>
					GitHub
				</a>
				<button class="inline-flex items-center rounded-full border border-white/20 px-3 py-1.5 text-white/80 transition hover:border-white/40 hover:text-white md:hidden">
					菜单
				</button>
			</div>
		</div>
	</header>
</template>

<script setup>
import { ref } from 'vue';

const theme = ref(document.documentElement.dataset.theme || 'dark');

function toggleTheme() {
	theme.value = theme.value === 'dark' ? 'light' : 'dark';
	document.documentElement.dataset.theme = theme.value;
	document.documentElement.style.colorScheme = theme.value;
	localStorage.setItem('blog-theme', theme.value);
}
</script>

<style scoped>
.site-header {
	color: var(--theme-text);
	background: var(--theme-header);
	border-color: var(--theme-border);
	box-shadow: 0 8px 28px var(--theme-shadow);
}

.site-header__brand,
.site-header__nav-link {
	color: var(--theme-text);
}

.site-header__nav-link {
	padding: 0.35rem 0.15rem;
	text-decoration: none;
}

.site-header__nav-link.router-link-active {
	color: var(--theme-accent);
}

.site-header__action {
	color: var(--theme-text-muted);
	border-color: var(--theme-border-strong);
}

.site-header__action:hover {
	color: var(--theme-text);
	border-color: var(--theme-text-muted);
	text-decoration: none;
}

.theme-toggle {
	display: inline-flex;
	width: 2.25rem;
	height: 2.25rem;
	align-items: center;
	justify-content: center;
	color: var(--theme-text-muted);
	background: var(--theme-surface);
	border: 1px solid var(--theme-border-strong);
	border-radius: 999px;
	cursor: pointer;
	transition: color .2s ease, background .2s ease, border-color .2s ease, transform .2s ease;
}

.theme-toggle:hover {
	color: var(--theme-text);
	border-color: var(--theme-text-muted);
	transform: translateY(-1px);
}

.theme-toggle svg {
	width: 1.1rem;
	height: 1.1rem;
	fill: none;
	stroke: currentColor;
	stroke-width: 1.8;
	stroke-linecap: round;
	stroke-linejoin: round;
}
</style>
