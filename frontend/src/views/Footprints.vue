<template>
	<div class="min-h-screen w-full overflow-x-hidden text-white relative">
		<SiteHeader />
		<div class="flex pt-[2.75rem] md:pt-[3.75rem]">
			<SideNav />
			<main class="flex-1 pt-6 px-6 md:px-8 lg:ml-52 lg:px-10 xl:ml-56 xl:px-12 h-[calc(100vh-2.75rem)] md:h-[calc(100vh-3.75rem)] overflow-y-auto footprints-scroll">
				<ClientOnly>
					<BlurReveal
						:delay="0.1"
						:duration="0.75"
						class="flex flex-col gap-10 max-w-6xl"
					>
						<section>
							<div class="flex flex-col gap-3">
								<h1 class="text-2xl font-bold md:text-4xl">足迹</h1>
								<p class="text-white/75 md:text-base">
									记录那些值得纪念的瞬间。
								</p>
							</div>
						</section>

						<section v-if="loading" class="space-y-10">
							<div class="rounded-xl border border-white/10 bg-white/5 p-8 backdrop-blur text-center">
								<p class="text-white/60">加载中...</p>
							</div>
						</section>

						<section v-else-if="errorMessage" class="space-y-10">
							<div class="rounded-xl border border-white/10 bg-white/5 p-8 backdrop-blur text-center">
								<p class="text-white/60">{{ errorMessage }}</p>
							</div>
						</section>

						<section v-else-if="timeline.length === 0" class="space-y-10">
							<div class="rounded-xl border border-white/10 bg-white/5 p-8 backdrop-blur text-center">
								<p class="text-white/60">暂无足迹记录</p>
							</div>
						</section>

						<section v-else class="space-y-10">
							<div
								v-for="yearGroup in timeline"
								:key="yearGroup.year"
								class="space-y-5"
							>
								<div class="flex items-center gap-3">
									<h2 class="text-3xl font-bold text-white/90 tracking-wide">
										{{ yearGroup.year }}
									</h2>
									<div class="h-px flex-1 bg-white/10"></div>
								</div>
								<article
										v-for="item in yearGroup.items"
										:key="item.id"
										class="rounded-xl border border-white/10 bg-white/5 p-6 backdrop-blur transition hover:border-white/20 hover:bg-white/8"
									>
										<div class="flex flex-wrap items-center gap-3 text-sm text-white/60">
											<span class="rounded-full border border-white/15 px-3 py-1">{{ item.date }}</span>
											<span v-if="item.location" class="flex items-center gap-1">
												<span class="i-lucide-map-pin h-4 w-4 text-white/50"></span>
												{{ item.location }}
											</span>
											<span v-if="item.type" class="rounded-full bg-white/10 px-3 py-1 text-white/70">
												{{ item.type }}
											</span>
										</div>
										<h2 class="mt-4 flex items-center gap-2 text-xl font-semibold text-white">
											<svg
												v-if="item.showTitleLogo"
												class="w-6 h-6 flex-shrink-0"
												viewBox="1 2 23 22"
											>
												<path
													d="M12 22c3.5-4.5 6-8.19 6-11.25A6 6 0 0012 4a6 6 0 00-6 6.75C6 13.81 8.5 17.5 12 22z"
													fill="#fff"
													stroke="#000"
													stroke-linecap="round"
													stroke-linejoin="round"
													stroke-width="1.6"
												/>
												<circle
													cx="12"
													cy="10.5"
													r="2.8"
													fill="#fff"
													stroke="#000"
													stroke-width="1.6"
												/>
											</svg>
											<span>{{ item.title }}</span>
										</h2>
										<p class="mt-2 text-sm leading-6 text-white/70">
											{{ item.description }}
										</p>
										<ul
											v-if="item.highlights?.length"
											class="mt-4 space-y-2 text-sm text-white/65"
										>
											<li
												v-for="highlight in item.highlights"
												:key="highlight"
												class="flex items-start gap-2"
											>
												<span class="mt-1 h-1.5 w-1.5 rounded-full bg-blue-400/80"></span>
												<span>{{ highlight }}</span>
											</li>
										</ul>
										<div
											v-if="item.images?.length"
											class="mt-4"
										>
											<ExpandableGallery
												:images="item.images"
												:onImageClick="(image, index, allImages) => openImageModal(image, allImages)"
												:should-load="shouldLoadItem(item.id)"
												@images-loaded="() => handleGalleryLoaded(item.id)"
												class="h-32 md:h-40"
											/>
										</div>
									</article>
							</div>
						</section>
						<br>

					</BlurReveal>
				</ClientOnly>
			</main>
		</div>

		<!-- 图片预览模态框 -->
		<Transition name="fade">
			<div
				v-if="imageModal.visible"
				class="fixed inset-0 z-50 flex items-center justify-center bg-black/90 backdrop-blur-sm"
				@click="closeImageModal"
			>
				<div class="relative max-w-7xl max-h-[90vh] w-full h-full flex items-center justify-center p-4">
					<button
						@click="closeImageModal"
						class="absolute top-4 right-4 z-10 rounded-full bg-white/10 p-2 hover:bg-white/20 transition-colors"
						aria-label="关闭"
					>
						<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
						</svg>
					</button>
					<button
						v-if="imageModal.currentIndex > 0"
						@click.stop="prevImage"
						class="absolute left-4 z-10 rounded-full bg-white/10 p-3 hover:bg-white/20 transition-colors"
						aria-label="上一张"
					>
						<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
						</svg>
					</button>
					<button
						v-if="imageModal.currentIndex < imageModal.allImages.length - 1"
						@click.stop="nextImage"
						class="absolute right-4 z-10 rounded-full bg-white/10 p-3 hover:bg-white/20 transition-colors"
						aria-label="下一张"
					>
						<svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
							<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
						</svg>
					</button>
					<img
						:src="imageModal.currentImage"
						alt="预览图片"
						class="max-w-full max-h-full object-contain"
						@click.stop
					/>
					<div
						v-if="imageModal.allImages.length > 1"
						class="absolute bottom-4 left-1/2 transform -translate-x-1/2 bg-black/50 px-4 py-2 rounded-full text-sm text-white/80"
					>
						{{ imageModal.currentIndex + 1 }} / {{ imageModal.allImages.length }}
					</div>
				</div>
			</div>
		</Transition>
	</div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed, watch } from 'vue';
import SiteHeader from '@/components/SiteHeader.vue';
import SideNav from '@/components/SideNav.vue';
import ClientOnly from '@/components/ClientOnly.vue';
import BlurReveal from '@/components/BlurReveal.vue';
import ExpandableGallery from '@/components/ExpandableGallery.vue';
import { footprints as staticFootprints } from '@/lib/content';

const footprints = ref(staticFootprints);
const loading = ref(false);
const errorMessage = ref('');
const imageModal = ref({
	visible: false,
	currentImage: '',
	allImages: [],
	currentIndex: 0,
});

// 将足迹数据按年份分组
const timeline = computed(() => {
	const grouped = {};
	let orderCounter = 0;
	
	footprints.value.forEach((item) => {
		const date = new Date(item.date);
		const year = date.getFullYear().toString();
		const month = String(date.getMonth() + 1).padStart(2, '0');
		const day = String(date.getDate()).padStart(2, '0');
		
		if (!grouped[year]) {
			grouped[year] = [];
		}
		
		const rawTitle = item.title || '';
		const trimmedTitle = typeof rawTitle === 'string' ? rawTitle.trimStart() : '';
		const showTitleLogo = trimmedTitle.startsWith('-');
		const normalizedTitle = showTitleLogo ? trimmedTitle.slice(1).trimStart() : rawTitle;
		const itemId = `${year}-${month}-${day}-${orderCounter}`;
		orderCounter++;
		
		grouped[year].push({
			id: itemId,
			date: `${year}-${month}-${day}`,
			title: normalizedTitle,
			showTitleLogo,
			description: item.description || '',
			type: item.type || null,
			location: item.location || null,
			highlights: item.highlights || [],
			images: item.images || [],
		});
	});
	
	// 转换为数组格式，按年份降序排列
	return Object.keys(grouped)
		.sort((a, b) => parseInt(b) - parseInt(a))
		.map((year) => ({
			year,
			items: grouped[year],
		}));
});

const completedItemIds = ref([]);
const orderedItemIds = computed(() =>
	timeline.value.flatMap((group) =>
		group.items
			.filter((item) => item.images?.length)
			.map((item) => item.id),
	),
);

const shouldLoadItem = (itemId) => {
	const order = orderedItemIds.value;
	if (!order.length) return true;
	const targetIndex = order.indexOf(itemId);
	if (targetIndex === -1) return true;
	return targetIndex <= completedItemIds.value.length;
};

function handleGalleryLoaded(itemId) {
	if (!completedItemIds.value.includes(itemId)) {
		completedItemIds.value = [...completedItemIds.value, itemId];
	}
}

watch(orderedItemIds, () => {
	completedItemIds.value = [];
});

function openImageModal(image, allImages) {
	imageModal.value.currentImage = image;
	imageModal.value.allImages = allImages;
	imageModal.value.currentIndex = allImages.indexOf(image);
	imageModal.value.visible = true;
	document.body.style.overflow = 'hidden';
}

function closeImageModal() {
	imageModal.value.visible = false;
	document.body.style.overflow = '';
}

function nextImage() {
	if (imageModal.value.currentIndex < imageModal.value.allImages.length - 1) {
		imageModal.value.currentIndex++;
		imageModal.value.currentImage = imageModal.value.allImages[imageModal.value.currentIndex];
	}
}

function prevImage() {
	if (imageModal.value.currentIndex > 0) {
		imageModal.value.currentIndex--;
		imageModal.value.currentImage = imageModal.value.allImages[imageModal.value.currentIndex];
	}
}

function handleKeydown(e) {
	if (!imageModal.value.visible) return;
	if (e.key === 'Escape') {
		closeImageModal();
	} else if (e.key === 'ArrowRight') {
		nextImage();
	} else if (e.key === 'ArrowLeft') {
		prevImage();
	}
}

onMounted(() => {
	window.addEventListener('keydown', handleKeydown);
});

onUnmounted(() => {
	window.removeEventListener('keydown', handleKeydown);
});
</script>

<style scoped>
.i-lucide-map-pin::before {
	content: '📍';
	display: inline-block;
}

.fade-enter-active,
.fade-leave-active {
	transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
	opacity: 0;
}

.footprints-scroll::-webkit-scrollbar {
	width: 6px;
}

.footprints-scroll::-webkit-scrollbar-track {
	background: rgba(255, 255, 255, 0.05);
	border-radius: 3px;
}

.footprints-scroll::-webkit-scrollbar-thumb {
	background: rgba(255, 255, 255, 0.2);
	border-radius: 3px;
}

.footprints-scroll::-webkit-scrollbar-thumb:hover {
	background: rgba(255, 255, 255, 0.3);
}
</style>

