<template>
	<header class="fixed inset-x-0 top-0 z-20 border-b border-white/20 bg-black/80 backdrop-blur-md shadow-lg shadow-black/30">
		<div class="relative flex min-h-[2.75rem] w-full max-w-none items-center gap-4 pl-2 pr-0 py-2 md:min-h-[3.75rem] md:pl-6 md:pr-0 md:py-3">
			<RouterLink to="/" class="flex items-center gap-2 text-white font-bold text-sm md:text-base">
				<img
					src="/logo.png"
					alt="Area-Ivy logo"
					class="h-7 w-auto object-contain md:h-8"
				/>
				<span>Area-Ivy's Blog</span>
			</RouterLink>
			<nav class="hidden md:flex absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 items-center justify-center gap-6 lg:gap-10">
				<RouterLink class="text-white font-bold" to="/home">主页</RouterLink>
				<RouterLink class="text-white font-bold" to="/posts">文章</RouterLink>
				<RouterLink class="text-white font-bold" to="/tools">工具</RouterLink>
				<RouterLink class="text-white font-bold" to="/footprints">足迹</RouterLink>
				<RouterLink class="text-white font-bold" to="/about">关于</RouterLink>
			</nav>
			<div class="ml-auto mr-4 flex items-center gap-2 text-xs md:text-sm">
				<!--
				<RouterLink
					class="inline-flex rounded-full border border-emerald-400/40 px-3 py-1.5 text-emerald-200 transition hover:border-emerald-300 hover:text-white"
					to="/console"
				>
					控制台
				</RouterLink>
				-->
				<a
					class="hidden rounded-full border border-white/20 px-3 py-1.5 text-white/80 transition hover:border-white/40 hover:text-white md:inline-flex"
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

<style scoped>
</style>
