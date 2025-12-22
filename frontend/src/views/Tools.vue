<template>
	<div class="min-h-screen w-full overflow-x-hidden text-white relative">
		<SiteHeader />
		<div class="flex pt-[2.75rem] md:pt-[3.75rem]">
			<SideNav />
			<main class="flex-1 pt-6 px-6 md:px-8 lg:ml-52 lg:px-10 xl:ml-56 xl:px-12 h-[calc(100vh-2.75rem)] md:h-[calc(100vh-3.75rem)] overflow-y-auto">
				<ClientOnly>
					<BlurReveal
						:delay="0.1"
						:duration="0.75"
						class="max-w-5xl"
					>
						<div>
							<h1 class="text-2xl font-bold md:text-4xl">工具</h1>
							<p class="mt-3 text-white/80 md:text-base">这里将收纳常用的在线工具、组件库和云平台。</p>
							<div class="mt-6 min-h-[200px]">
								<div
									v-if="loading"
									class="rounded-2xl border border-white/10 bg-white/5 p-6 text-center text-white/70"
								>
									正在加载工具...
								</div>
								<div
									v-else-if="errorMessage"
									class="rounded-2xl border border-red-500/30 bg-red-500/10 p-5 text-center text-sm text-red-200"
								>
									{{ errorMessage }}
								</div>
								<div
									v-else-if="tools.length === 0"
									class="rounded-2xl border border-white/10 bg-white/5 p-6 text-center text-white/60"
								>
									暂无工具，敬请期待。
								</div>
								<div v-else class="grid grid-cols-1 gap-4 md:grid-cols-2 lg:grid-cols-3">
									<button
										v-for="tool in tools"
										:key="tool.id"
										type="button"
										class="group flex flex-col gap-4 rounded-2xl border border-white/10 bg-white/5 p-5 text-left transition hover:-translate-y-1 hover:border-white/30 hover:bg-white/10 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-white/60"
										@click="handleNavigate(tool.link)"
									>
									<div class="flex items-center gap-3">
										<div class="relative flex h-14 w-14 shrink-0 items-center justify-center overflow-hidden rounded-xl bg-gradient-to-br from-white/10 to-white/5 shadow-lg ring-1 ring-white/10 transition-transform group-hover:scale-105">
											<img
												v-if="tool.logo"
												:src="tool.logo"
												:alt="tool.name"
												class="h-full w-full object-cover"
												loading="lazy"
											/>
											<span v-else class="text-xl font-semibold text-white/90">{{ tool.name[0] }}</span>
										</div>
										<div class="flex flex-col gap-2">
											<p class="text-lg font-semibold">{{ tool.name }}</p>
											<div class="flex flex-wrap gap-2">
												<span
													v-for="tag in tool.tags"
													:key="tag"
													class="rounded-full border border-white/15 bg-white/5 px-2 py-0.5 text-xs text-white/70"
												>
													{{ tag }}
												</span>
											</div>
										</div>
										</div>
										<p class="text-sm leading-relaxed text-white/70">
											{{ tool.description }}
										</p>
										<span class="text-sm font-medium text-white/70 transition group-hover:text-white">
											了解更多 →
										</span>
									</button>
								</div>
							</div>
						</div>
					</BlurReveal>
				</ClientOnly>
			</main>
		</div>
	</div>
</template>

<script setup>
import { onMounted, ref } from 'vue';
import SiteHeader from '@/components/SiteHeader.vue';
import SideNav from '@/components/SideNav.vue';
import ClientOnly from '@/components/ClientOnly.vue';
import BlurReveal from '@/components/BlurReveal.vue';
import { API_BASE } from '@/lib/utils';

const tools = ref([]);
const loading = ref(true);
const errorMessage = ref('');

const parseTags = value => {
	if (Array.isArray(value)) return value;
	return (value || '')
		.split(',')
		.map(tag => tag.trim())
		.filter(Boolean);
};

const fetchTools = async () => {
	loading.value = true;
	errorMessage.value = '';
	try {
		const url = new URL('/api/tools', API_BASE);
		const res = await fetch(url.toString());
		if (!res.ok) throw new Error('加载工具数据失败');
		const data = await res.json();
		tools.value = (data || []).map(tool => ({
			...tool,
			tags: parseTags(tool.tags),
		}));
	} catch (error) {
		console.error(error);
		errorMessage.value = error.message || '加载工具失败，请稍后重试。';
		tools.value = [];
	} finally {
		loading.value = false;
	}
};

onMounted(fetchTools);

const handleNavigate = (link) => {
	if (!link) return;
	window.open(link, '_blank', 'noreferrer');
};
</script>

<style scoped>
</style>


