<template>
  <div :class="containerClass">
    <div
      v-for="(image, index) in images"
      :key="image"
      :class="itemClass"
      :style="getItemStyle(index)"
	  role="button"
	  tabindex="0"
	  :aria-label="`查看第 ${index + 1} 张图片`"
      @click="handleImageClick(image, index)"
	  @keydown.enter="handleImageClick(image, index)"
	  @keydown.space.prevent="handleImageClick(image, index)"
      @mouseenter="hoveredIndex = index"
      @mouseleave="hoveredIndex = -1"
    >
      <img
        v-if="loadedImages.has(image)"
        class="relative h-full w-full object-cover"
        :src="image"
		:alt="`足迹照片 ${index + 1}`"
		loading="lazy"
      />
      <div
        v-else
        class="relative h-full w-full bg-white/5 flex items-center justify-center"
      >
        <div class="text-white/30 text-sm">加载中...</div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import type { HTMLAttributes } from "vue";
import { computed, ref, onMounted, onUnmounted, watch } from "vue";
import { cn } from "../lib/utils";

interface Props {
  images: string[];
  class?: HTMLAttributes["class"];
  onImageClick?: (image: string, index: number, allImages: string[]) => void;
  batchSize?: number; // 每批加载的图片数量
}

const props = withDefaults(defineProps<Props>(), {
  batchSize: 3, // 默认每次加载3张图片
});

const hoveredIndex = ref(-1);
const isCompact = computed(() => props.images.length <= 3);
const loadedImages = ref(new Set<string>());
const loadingImages = ref(new Set<string>()); // 正在加载的图片
let currentIndex = 0; // 当前加载到的图片索引
let isLoading = false; // 是否正在加载批次

const containerClass = computed(() =>
  cn(
    "flex gap-2 h-96",
    isCompact.value ? "w-auto" : "w-full",
    props.class
  )
);

const itemClass = computed(() =>
  cn(
    "relative flex h-full cursor-pointer overflow-hidden rounded-xl transition-all duration-500 ease-in-out",
    isCompact.value ? "flex-none" : "flex-1"
  )
);

const compactBaseWidth = "min(14rem, 60vw)";
const compactExpandedWidth = "min(20rem, 80vw)";
const expandedMaxWidth = "min(28rem, 45vw)";

const getItemStyle = (index: number) => {
  if (isCompact.value) {
    return {
      width: hoveredIndex.value === index ? compactExpandedWidth : compactBaseWidth,
    };
  }

  if (hoveredIndex.value === index) {
    return {
      flex: "2",
      maxWidth: expandedMaxWidth,
    };
  }

  return {
    flex: "1",
    maxWidth: "20rem",
  };
};

const handleImageClick = (image: string, index: number) => {
  if (props.onImageClick) {
    props.onImageClick(image, index, props.images);
  }
};

// 加载单张图片，返回 Promise
const loadImage = (imageSrc: string): Promise<void> => {
  return new Promise((resolve) => {
    // 如果已经加载过或正在加载，直接返回
    if (loadedImages.value.has(imageSrc) || loadingImages.value.has(imageSrc)) {
      resolve();
      return;
    }

    // 标记为正在加载
    loadingImages.value.add(imageSrc);

    const img = new Image();
    img.onload = () => {
      loadedImages.value.add(imageSrc);
      loadingImages.value.delete(imageSrc);
      resolve();
    };
    img.onerror = () => {
      // 即使加载失败也标记为已加载，避免重复尝试
      loadedImages.value.add(imageSrc);
      loadingImages.value.delete(imageSrc);
      resolve();
    };
    img.src = imageSrc;
  });
};

// 加载一批图片
const loadBatch = async () => {
  if (isLoading || currentIndex >= props.images.length) {
    return;
  }

  isLoading = true;

  // 获取当前批次要加载的图片
  const batch = props.images.slice(currentIndex, currentIndex + props.batchSize);
  
  // 并行加载这一批图片
  const loadPromises = batch.map(imageSrc => loadImage(imageSrc));
  
  try {
    // 等待这一批图片全部加载完成
    await Promise.all(loadPromises);
    
    // 更新索引，准备加载下一批
    currentIndex += props.batchSize;
    
    // 如果还有图片未加载，继续加载下一批
    if (currentIndex < props.images.length) {
      // 使用 setTimeout 给浏览器一个喘息的机会，避免阻塞 UI
      setTimeout(() => {
        isLoading = false;
        loadBatch();
      }, 100);
    } else {
      isLoading = false;
    }
  } catch (error) {
    console.error('加载图片批次失败:', error);
    isLoading = false;
  }
};

onMounted(() => {
  // 开始加载第一批图片
  if (props.images.length > 0) {
    loadBatch();
  }
});

// 监听 images 变化，重新开始加载
watch(() => props.images, () => {
  // 重置状态
  loadedImages.value.clear();
  loadingImages.value.clear();
  currentIndex = 0;
  isLoading = false;
  
  // 重新开始加载
  if (props.images.length > 0) {
    loadBatch();
  }
}, { deep: true });

onUnmounted(() => {
  // 清理状态
  isLoading = false;
});
</script>
