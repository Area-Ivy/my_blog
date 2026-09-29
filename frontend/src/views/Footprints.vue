<template>
  <div class="site-page">
    <SiteHeader />
    <main class="page-main">
      <header class="footprints-intro">
        <div><p class="page-kicker">Places & moments</p><h1 class="page-title page-title--small">走过的地方，<br />留住的片刻。</h1></div>
        <p>有些记忆适合用文字解释，有些只需要一张照片和当时的日期。</p>
      </header>

      <section class="timeline" aria-label="足迹时间轴">
        <div v-for="yearGroup in timeline" :key="yearGroup.year" class="year-group">
          <div class="year-label"><span>{{ yearGroup.year }}</span><small>{{ yearGroup.items.length }} entries</small></div>
          <div class="year-items">
            <article v-for="item in yearGroup.items" :key="item.id" class="footprint-card surface">
              <header><time>{{ item.date }}</time><span v-if="item.type" class="pill">{{ item.type }}</span></header>
              <h2>{{ item.title }}</h2>
              <p v-if="item.location" class="location">{{ item.location }}</p>
              <p v-if="item.description" class="description">{{ item.description }}</p>
              <ul v-if="item.highlights?.length"><li v-for="highlight in item.highlights" :key="highlight">{{ highlight }}</li></ul>
              <ExpandableGallery v-if="item.images?.length" :images="item.images" :onImageClick="(image, index, allImages) => openImageModal(image, allImages)" :should-load="shouldLoadItem(item.id)" @images-loaded="() => handleGalleryLoaded(item.id)" class="gallery" />
            </article>
          </div>
        </div>
      </section>
    </main>

    <Transition name="fade">
      <div v-if="imageModal.visible" class="lightbox" role="dialog" aria-modal="true" aria-label="图片预览" @click="closeImageModal">
        <button class="lightbox__close" type="button" aria-label="关闭预览" @click="closeImageModal">×</button>
        <button v-if="imageModal.currentIndex > 0" class="lightbox__nav lightbox__nav--prev" type="button" aria-label="上一张" @click.stop="prevImage">←</button>
        <img :src="imageModal.currentImage" alt="足迹照片预览" @click.stop />
        <button v-if="imageModal.currentIndex < imageModal.allImages.length - 1" class="lightbox__nav lightbox__nav--next" type="button" aria-label="下一张" @click.stop="nextImage">→</button>
        <span class="lightbox__count">{{ imageModal.currentIndex + 1 }} / {{ imageModal.allImages.length }}</span>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed, watch } from 'vue';
import SiteHeader from '@/components/SiteHeader.vue';
import ExpandableGallery from '@/components/ExpandableGallery.vue';
import { footprints as staticFootprints } from '@/lib/content';

const footprints = ref(staticFootprints);
const imageModal = ref({ visible: false, currentImage: '', allImages: [], currentIndex: 0 });
const timeline = computed(() => {
  const grouped = {};
  footprints.value.forEach((item, index) => {
    const date = new Date(item.date);
    const year = String(date.getFullYear());
    const formatted = `${year}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
    const rawTitle = String(item.title || '').trim();
    (grouped[year] ||= []).push({ ...item, id: `${year}-${index}`, date: formatted, title: rawTitle.startsWith('-') ? rawTitle.slice(1).trim() : rawTitle, highlights: item.highlights || [], images: item.images || [] });
  });
  return Object.keys(grouped).sort((a, b) => Number(b) - Number(a)).map(year => ({ year, items: grouped[year] }));
});
const completedItemIds = ref([]);
const orderedItemIds = computed(() => timeline.value.flatMap(group => group.items.filter(item => item.images?.length).map(item => item.id)));
const shouldLoadItem = (id) => { const index = orderedItemIds.value.indexOf(id); return index < 0 || index <= completedItemIds.value.length; };
function handleGalleryLoaded(id) { if (!completedItemIds.value.includes(id)) completedItemIds.value = [...completedItemIds.value, id]; }
watch(orderedItemIds, () => { completedItemIds.value = []; });

function openImageModal(image, allImages) { imageModal.value = { visible: true, currentImage: image, allImages, currentIndex: allImages.indexOf(image) }; document.body.style.overflow = 'hidden'; }
function closeImageModal() { imageModal.value.visible = false; document.body.style.overflow = ''; }
function nextImage() { const next = imageModal.value.currentIndex + 1; if (next < imageModal.value.allImages.length) { imageModal.value.currentIndex = next; imageModal.value.currentImage = imageModal.value.allImages[next]; } }
function prevImage() { const prev = imageModal.value.currentIndex - 1; if (prev >= 0) { imageModal.value.currentIndex = prev; imageModal.value.currentImage = imageModal.value.allImages[prev]; } }
function handleKeydown(event) { if (!imageModal.value.visible) return; if (event.key === 'Escape') closeImageModal(); if (event.key === 'ArrowRight') nextImage(); if (event.key === 'ArrowLeft') prevImage(); }
onMounted(() => window.addEventListener('keydown', handleKeydown));
onUnmounted(() => { window.removeEventListener('keydown', handleKeydown); document.body.style.overflow = ''; });
</script>

<style scoped>
.footprints-intro { display: grid; grid-template-columns: 1fr 360px; gap: 64px; align-items: end; padding-bottom: 56px; border-bottom: 1px solid var(--line); }
.footprints-intro > p { margin: 0; color: var(--ink-soft); font-size: 18px; line-height: 1.7; }
.timeline { margin-top: 48px; }
.year-group { display: grid; grid-template-columns: 150px minmax(0, 1fr); gap: 32px; padding: 40px 0; border-bottom: 1px solid var(--line); }
.year-label { position: sticky; top: 90px; height: fit-content; }
.year-label span { display: block; font-size: 36px; font-weight: 720; letter-spacing: -.045em; }
.year-label small { color: var(--ink-muted); font-size: 11px; letter-spacing: .1em; text-transform: uppercase; }
.year-items { display: grid; gap: 16px; }
.footprint-card { padding: 28px; }
.footprint-card header { display: flex; align-items: center; justify-content: space-between; gap: 12px; }
.footprint-card time { color: var(--accent-dark); font-size: 12px; font-weight: 700; letter-spacing: .08em; }
.footprint-card h2 { margin: 22px 0 4px; font-size: clamp(24px, 3vw, 34px); letter-spacing: -.035em; }
.location { margin: 0; color: var(--ink-muted); font-size: 13px; }
.description { max-width: 760px; margin: 18px 0 0; color: var(--ink-soft); }
.footprint-card ul { padding-left: 20px; color: var(--ink-soft); }
.gallery { height: 210px; margin-top: 24px; overflow: hidden; border-radius: 13px; }
.lightbox { position: fixed; inset: 0; z-index: 100; display: grid; place-items: center; padding: 64px; color: #fff; background: rgba(10,14,20,.94); backdrop-filter: blur(16px); }
.lightbox img { max-width: 100%; max-height: calc(100vh - 120px); object-fit: contain; border-radius: 10px; }
.lightbox button { position: absolute; display: grid; width: 48px; height: 48px; place-items: center; color: #fff; background: rgba(255,255,255,.12); border: 1px solid rgba(255,255,255,.15); border-radius: 50%; font-size: 22px; }
.lightbox__close { top: 22px; right: 22px; }.lightbox__nav { top: 50%; transform: translateY(-50%); }.lightbox__nav--prev { left: 22px; }.lightbox__nav--next { right: 22px; }
.lightbox__count { position: absolute; bottom: 22px; padding: 6px 12px; background: rgba(0,0,0,.35); border-radius: 999px; font-size: 12px; }
.fade-enter-active, .fade-leave-active { transition: opacity .2s ease; }.fade-enter-from, .fade-leave-to { opacity: 0; }
@media (max-width: 800px) { .footprints-intro { grid-template-columns: 1fr; gap: 24px; } .year-group { grid-template-columns: 1fr; gap: 18px; } .year-label { position: static; } .year-items { min-width: 0; } }
@media (max-width: 520px) { .footprint-card { padding: 20px; } .gallery { height: 150px; } .lightbox { padding: 70px 16px; } .lightbox__nav--prev { left: 8px; }.lightbox__nav--next { right: 8px; } }
</style>
