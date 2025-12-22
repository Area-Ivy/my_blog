<template>
	<div class="min-h-screen w-full bg-[#050505] text-white">
		<SiteHeader />
		<main class="mx-auto max-w-6xl pt-24 pb-10 px-4 md:px-8">
			<section class="mb-8">
				<h1 class="text-2xl font-semibold mb-2">控制台</h1>
				<p class="text-sm text-white/70">管理文章，支持创建、编辑与删除操作。</p>
			</section>
			<div class="grid gap-6 lg:grid-cols-[1.2fr,0.8fr]">
				<section class="rounded-2xl border border-white/10 bg-white/5 backdrop-blur">
					<div class="flex items-center justify-between border-b border-white/10 px-6 py-4">
						<div>
							<h2 class="text-lg font-semibold">文章列表</h2>
							<p class="text-xs text-white/60">最近 50 条文章，按创建时间倒序</p>
						</div>
						<button
							class="rounded-full border border-white/20 px-4 py-2 text-sm font-medium text-white/80 transition hover:border-white/40 hover:text-white"
							@click="resetForm"
						>
							新增文章
						</button>
					</div>
					<div class="p-6 space-y-4 max-h-[70vh] overflow-y-auto custom-scrollbar">
						<div v-if="listLoading" class="text-center text-white/60 text-sm py-6">正在加载文章...</div>
						<div v-else-if="listError" class="rounded-lg border border-red-500/40 bg-red-500/10 px-4 py-3 text-sm text-red-200">
							{{ listError }}
						</div>
						<div v-else-if="articles.length === 0" class="text-center text-white/60 text-sm py-6">暂无文章</div>
						<div
							v-else
							v-for="article in articles"
							:key="article.id"
							class="rounded-xl border border-white/10 bg-black/20 p-4 transition hover:border-white/30"
						>
							<div class="flex items-start justify-between gap-4">
								<div>
									<div class="flex items-center gap-2">
										<h3 class="text-base font-semibold">{{ article.title }}</h3>
										<span class="rounded-full border border-white/20 px-2 py-0.5 text-xs text-white/60">
											ID: {{ article.id }}
										</span>
									</div>
									<p class="text-xs text-white/50 mt-1">{{ article.slug }}</p>
								</div>
								<div class="flex items-center gap-2">
									<button
										class="rounded-full border border-white/20 px-3 py-1.5 text-xs text-white/80 transition hover:border-white/40 hover:text-white"
										@click="startEdit(article.id)"
										:disabled="detailLoadingId === article.id"
									>
										{{ detailLoadingId === article.id ? '加载中...' : '编辑' }}
									</button>
									<button
										class="rounded-full border border-red-500/40 px-3 py-1.5 text-xs text-red-300 transition hover:border-red-400"
										@click="confirmDelete(article.id)"
										:disabled="deletingId === article.id"
									>
										{{ deletingId === article.id ? '删除中...' : '删除' }}
									</button>
								</div>
							</div>
							<p v-if="article.summary" class="mt-3 text-sm text-white/70 line-clamp-2">
								{{ article.summary }}
							</p>
							<div class="mt-3 flex flex-wrap items-center gap-2 text-xs text-white/50">
								<span>创建：{{ formatDate(article.created_at) }}</span>
								<span>更新：{{ formatDate(article.updated_at) }}</span>
							</div>
							<div v-if="article.tagsArray.length" class="mt-2 flex flex-wrap gap-2">
								<span
									v-for="tag in article.tagsArray"
									:key="tag"
									class="rounded-full border border-white/20 px-2 py-0.5 text-xs text-white/70"
								>
									{{ tag }}
								</span>
							</div>
						</div>
					</div>
				</section>
				<section class="rounded-2xl border border-white/10 bg-white/5 backdrop-blur">
					<div class="border-b border-white/10 px-6 py-4">
						<h2 class="text-lg font-semibold">{{ isEditing ? '编辑文章' : '新增文章' }}</h2>
						<p class="text-xs text-white/60">
							{{ isEditing ? '更新当前文章，保存后自动刷新列表' : '填写信息后点击提交创建新文章' }}
						</p>
					</div>
					<form class="space-y-4 p-6" @submit.prevent="handleSubmit">
						<div v-if="formError" class="rounded-lg border border-red-500/40 bg-red-500/10 px-4 py-3 text-sm text-red-200">
							{{ formError }}
						</div>
						<div v-if="formSuccess" class="rounded-lg border border-emerald-500/40 bg-emerald-500/10 px-4 py-3 text-sm text-emerald-200">
							{{ formSuccess }}
						</div>
						<label class="block text-sm">
							<span class="mb-1 inline-block text-white/70">标题</span>
							<input
								v-model="form.title"
								type="text"
								required
								class="w-full rounded-xl border border-white/15 bg-black/30 px-3 py-2 text-white placeholder:text-white/40 focus:border-white/40 focus:outline-none"
							/>
						</label>
						<label class="block text-sm">
							<span class="mb-1 inline-block text-white/70">Slug（唯一路径）</span>
							<input
								v-model="form.slug"
								type="text"
								required
								class="w-full rounded-xl border border-white/15 bg-black/30 px-3 py-2 text-white placeholder:text-white/40 focus:border-white/40 focus:outline-none"
							/>
						</label>
						<label class="block text-sm">
							<span class="mb-1 inline-block text-white/70">摘要</span>
							<textarea
								v-model="form.summary"
								rows="2"
								class="w-full rounded-xl border border-white/15 bg-black/30 px-3 py-2 text-white placeholder:text-white/40 focus:border-white/40 focus:outline-none"
							></textarea>
						</label>
						<label class="block text-sm">
							<span class="mb-1 inline-block text-white/70">标签（使用逗号分隔）</span>
							<input
								v-model="form.tags"
								type="text"
								placeholder="例如：AI, 随想"
								class="w-full rounded-xl border border-white/15 bg-black/30 px-3 py-2 text-white placeholder:text-white/40 focus:border-white/40 focus:outline-none"
							/>
						</label>
						<label class="block text-sm">
							<span class="mb-1 inline-block text-white/70">分类 ID（可选）</span>
							<input
								v-model="form.categoryId"
								type="number"
								min="0"
								class="w-full rounded-xl border border-white/15 bg-black/30 px-3 py-2 text-white placeholder:text-white/40 focus:border-white/40 focus:outline-none"
							/>
						</label>
						<label class="block text-sm">
							<span class="mb-1 inline-block text-white/70">正文内容</span>
							<textarea
								v-model="form.content"
								required
								rows="8"
								class="w-full rounded-xl border border-white/15 bg-black/30 px-3 py-2 text-white placeholder:text-white/40 focus:border-white/40 focus:outline-none"
							></textarea>
						</label>
						<div class="flex items-center gap-3 pt-2">
							<button
								type="submit"
								class="flex-1 rounded-xl bg-white/90 px-4 py-2 text-sm font-semibold text-black transition hover:bg-white"
								:disabled="saving"
							>
								{{ saving ? '提交中...' : isEditing ? '保存修改' : '创建文章' }}
							</button>
							<button
								type="button"
								class="rounded-xl border border-white/20 px-4 py-2 text-sm text-white/80 transition hover:border-white/40 hover:text-white"
								@click="resetForm"
								:disabled="saving"
							>
								重置
							</button>
						</div>
					</form>
				</section>
			</div>
		</main>
	</div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue';
import SiteHeader from '@/components/SiteHeader.vue';
import { API_BASE } from '@/lib/utils';

interface ArticleSummary {
	id: number;
	title: string;
	slug: string;
	summary?: string | null;
	created_at: string;
	updated_at: string;
	tags?: string | null;
	tagsArray: string[];
}

interface ArticleDetailResponse extends ArticleSummary {
	content: string;
	category_id?: number | null;
}

const articles = ref<ArticleSummary[]>([]);
const listLoading = ref(false);
const listError = ref('');
const saving = ref(false);
const deletingId = ref<number | null>(null);
const detailLoadingId = ref<number | null>(null);
const editingId = ref<number | null>(null);
const formError = ref('');
const formSuccess = ref('');

const form = reactive({
	title: '',
	slug: '',
	summary: '',
	tags: '',
	content: '',
	categoryId: '',
});

const isEditing = computed(() => editingId.value !== null);

function formatDate(value: string) {
	try {
		return new Date(value).toLocaleString();
	} catch {
		return value;
	}
}

function normalizeTags(value?: string | null) {
	if (!value) return [];
	return value.split(',').map((tag) => tag.trim()).filter(Boolean);
}

function resetForm() {
	editingId.value = null;
	form.title = '';
	form.slug = '';
	form.summary = '';
	form.tags = '';
	form.content = '';
	form.categoryId = '';
	formError.value = '';
	formSuccess.value = '';
}

async function fetchArticles() {
	listLoading.value = true;
	listError.value = '';
	try {
		const url = new URL('/api/articles', API_BASE);
		url.searchParams.set('page', '1');
		url.searchParams.set('page_size', '50');
		const res = await fetch(url.toString());
		if (!res.ok) throw new Error('获取文章列表失败');
		const data = await res.json();
		articles.value = data.map((article: ArticleSummary) => ({
			...article,
			tagsArray: normalizeTags(article.tags),
		}));
	} catch (error) {
		console.error(error);
		listError.value = (error as Error).message || '加载文章时出错';
	} finally {
		listLoading.value = false;
	}
}

async function startEdit(articleId: number) {
	detailLoadingId.value = articleId;
	formError.value = '';
	formSuccess.value = '';
	try {
		const url = new URL(`/api/articles/${articleId}`, API_BASE);
		const res = await fetch(url.toString());
		if (!res.ok) throw new Error('获取文章详情失败');
		const article: ArticleDetailResponse = await res.json();
		editingId.value = article.id;
		form.title = article.title;
		form.slug = article.slug;
		form.summary = article.summary || '';
		form.tags = normalizeTags(article.tags).join(', ');
		form.content = article.content;
		form.categoryId = article.category_id ? String(article.category_id) : '';
	} catch (error) {
		console.error(error);
		formError.value = (error as Error).message || '加载详情时出错';
	} finally {
		detailLoadingId.value = null;
	}
}

async function handleSubmit() {
	if (!form.title.trim() || !form.slug.trim() || !form.content.trim()) {
		formError.value = '标题、Slug 和正文不能为空';
		return;
	}
	formError.value = '';
	formSuccess.value = '';
	saving.value = true;
	const payload = {
		title: form.title.trim(),
		slug: form.slug.trim(),
		summary: form.summary.trim() || null,
		content: form.content,
		category_id: form.categoryId ? Number(form.categoryId) : null,
		tags: form.tags
			.split(',')
			.map((tag) => tag.trim())
			.filter(Boolean),
	};
	try {
		const isUpdate = editingId.value !== null;
		const url = new URL(isUpdate ? `/api/articles/${editingId.value}` : '/api/articles', API_BASE);
		const res = await fetch(url.toString(), {
			method: isUpdate ? 'PUT' : 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify(payload),
		});
		if (!res.ok) {
			const data = await res.json().catch(() => ({}));
			throw new Error(data.detail || '提交失败');
		}
		formSuccess.value = isUpdate ? '文章已更新' : '文章已创建';
		await fetchArticles();
		if (!isUpdate) {
			resetForm();
		}
	} catch (error) {
		console.error(error);
		formError.value = (error as Error).message || '提交失败';
	} finally {
		saving.value = false;
	}
}

async function confirmDelete(articleId: number) {
	if (!window.confirm('确认删除该文章？此操作不可撤销。')) {
		return;
	}
	deletingId.value = articleId;
	formSuccess.value = '';
	formError.value = '';
	try {
		const url = new URL(`/api/articles/${articleId}`, API_BASE);
		const res = await fetch(url.toString(), { method: 'DELETE' });
		if (!res.ok) {
			const data = await res.json().catch(() => ({}));
			throw new Error(data.detail || '删除失败');
		}
		if (editingId.value === articleId) {
			resetForm();
		}
		await fetchArticles();
		formSuccess.value = '文章已删除';
	} catch (error) {
		console.error(error);
		formError.value = (error as Error).message || '删除失败';
	} finally {
		deletingId.value = null;
	}
}

onMounted(() => {
	fetchArticles();
});
</script>

<style scoped>
.custom-scrollbar {
	scrollbar-width: thin;
	scrollbar-color: rgba(255, 255, 255, 0.2) transparent;
}

.custom-scrollbar::-webkit-scrollbar {
	width: 6px;
}

.custom-scrollbar::-webkit-scrollbar-track {
	background: transparent;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
	background: rgba(255, 255, 255, 0.2);
	border-radius: 999px;
}
</style>

