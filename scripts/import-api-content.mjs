#!/usr/bin/env node

import { mkdir, writeFile } from 'node:fs/promises';
import { basename, extname, join } from 'node:path';

const apiBase = (process.argv[2] || process.env.BLOG_API_BASE || '').replace(/\/$/, '');
const assetBase = (process.argv[3] || process.env.BLOG_ASSET_BASE || apiBase).replace(/\/$/, '');

if (!apiBase) {
	console.error('用法: node scripts/import-api-content.mjs <API 地址> [静态资源地址]');
	process.exit(1);
}

const projectRoot = new URL('../', import.meta.url);
const contentDir = new URL('frontend/src/content/', projectRoot);
const articlesDir = new URL('articles/', contentDir);
const publicDir = new URL('frontend/public/media/', projectRoot);

await Promise.all([
	mkdir(articlesDir, { recursive: true }),
	mkdir(publicDir, { recursive: true }),
]);

async function getJson(endpoint) {
	const response = await fetch(`${apiBase}${endpoint}`);
	if (!response.ok) throw new Error(`${endpoint}: HTTP ${response.status}`);
	return response.json();
}

function safeName(value) {
	return String(value || 'item')
		.normalize('NFKD')
		.replace(/[^\w.-]+/g, '-')
		.replace(/^-+|-+$/g, '')
		.toLowerCase() || 'item';
}

async function localizeAsset(url, group, fallbackName) {
	if (!url || !/^https?:\/\//i.test(url)) return url || '';
	const parsed = new URL(url);
	const extension = extname(parsed.pathname) || '';
	const fileName = `${safeName(fallbackName || basename(parsed.pathname, extension))}${extension}`;
	const targetDir = new URL(`${group}/`, publicDir);
	await mkdir(targetDir, { recursive: true });

	const response = await fetch(url);
	if (!response.ok) {
		console.warn(`跳过资源 ${url}: HTTP ${response.status}`);
		return url;
	}
	await writeFile(new URL(fileName, targetDir), Buffer.from(await response.arrayBuffer()));
	return `/media/${group}/${fileName}`;
}

function frontmatter(article) {
	const fields = {
		id: article.id,
		title: article.title,
		slug: article.slug,
		summary: article.summary || '',
		tags: String(article.tags || '').split(',').map((tag) => tag.trim()).filter(Boolean),
		created_at: article.created_at,
		updated_at: article.updated_at,
	};
	return `---\n${Object.entries(fields).map(([key, value]) => `${key}: ${JSON.stringify(value)}`).join('\n')}\n---\n\n`;
}

const articleList = await getJson('/api/articles?page=1&page_size=100');
for (const summary of articleList) {
	const article = await getJson(`/api/articles/${summary.id}`);
	const fileName = `${safeName(article.slug || article.id)}.md`;
	await writeFile(new URL(fileName, articlesDir), `${frontmatter(article)}${article.content.trim()}\n`);
}

const tools = await getJson('/api/tools');
for (const tool of tools) {
	tool.logo = await localizeAsset(tool.logo, 'tools', tool.id);
}

let footprints = [];
try {
	footprints = await getJson('/api/footprints');
	for (const footprint of footprints) {
		footprint.images = await Promise.all((footprint.images || []).map((url, index) =>
			localizeAsset(url, `footprints/${footprint.id}`, String(index + 1)),
		));
	}
} catch (error) {
	console.warn(`足迹导入失败：${error.message}`);
}

const songs = await getJson('/api/songs');
for (const song of songs) {
	song.url = await localizeAsset(song.url, 'music', `${song.id}-audio`);
	song.cover = await localizeAsset(song.cover, 'music', `${song.id}-cover`);
}

await Promise.all([
	writeFile(new URL('tools.json', contentDir), `${JSON.stringify(tools, null, 2)}\n`),
	writeFile(new URL('footprints.json', contentDir), `${JSON.stringify(footprints, null, 2)}\n`),
	writeFile(new URL('songs.json', contentDir), `${JSON.stringify(songs, null, 2)}\n`),
]);

console.log(`导入完成：${articleList.length} 篇文章、${tools.length} 个工具、${footprints.length} 条足迹、${songs.length} 首音乐。`);
