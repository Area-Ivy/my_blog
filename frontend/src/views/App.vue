<template>
	<div class="min-h-screen w-full overflow-x-hidden text-white relative">
		<SiteHeader />
		<div class="pt-24 px-4 md:px-8 lg:px-12">
			<div class="mx-auto max-w-3xl text-center">
				<h1 class="text-2xl font-bold md:text-4xl">页面已重构为路由式文档/文章/关于</h1>
				<p class="mt-3 text-white/80">我们已将原有的标签页拆分为独立页面。</p>
				<div class="mt-6 flex items-center justify-center gap-3">
					<RouterLink to="/home" class="rounded-md bg-blue-600 px-4 py-2 text-sm font-medium text-white hover:bg-blue-700">前往主页</RouterLink>
					<RouterLink to="/posts" class="rounded-md bg-white px-4 py-2 text-sm font-medium text-black hover:bg-gray-100">查看文章</RouterLink>
					<RouterLink to="/about" class="rounded-md border border-white/20 px-4 py-2 text-sm font-medium text-white hover:border-white/40">关于页面</RouterLink>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';
import SiteHeader from '@/components/SiteHeader.vue';

const router = useRouter();
onMounted(() => {
	// 直接跳转到主页
	router.replace('/home');
});
</script>

<style scoped>
</style>




