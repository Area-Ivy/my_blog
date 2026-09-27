import toolsData from '@/content/tools.json';
import footprintsData from '@/content/footprints.json';
import songsData from '@/content/songs.json';

const articleFiles = import.meta.glob('../content/articles/*.md', {
	eager: true,
	query: '?raw',
	import: 'default',
});

function parseValue(value) {
	try {
		return JSON.parse(value);
	} catch {
		return value;
	}
}

function parseArticle(source, sourcePath) {
	const match = source.match(/^---\s*\n([\s\S]*?)\n---\s*\n?/);
	if (!match) throw new Error(`文章缺少 frontmatter: ${sourcePath}`);

	const metadata = {};
	for (const line of match[1].split('\n')) {
		const separator = line.indexOf(':');
		if (separator === -1) continue;
		metadata[line.slice(0, separator).trim()] = parseValue(line.slice(separator + 1).trim());
	}

	return {
		...metadata,
		id: metadata.id ?? metadata.slug,
		title: metadata.title || '未命名文章',
		slug: metadata.slug || '',
		summary: metadata.summary || '',
		excerpt: metadata.summary || '',
		tags: Array.isArray(metadata.tags) ? metadata.tags : [],
		date: String(metadata.updated_at || metadata.created_at || '').slice(0, 10),
		content: source.slice(match[0].length).trim(),
	};
}

export const articles = Object.entries(articleFiles)
	.map(([sourcePath, source]) => parseArticle(source, sourcePath))
	.sort((a, b) => new Date(b.updated_at || 0) - new Date(a.updated_at || 0));

export const tools = toolsData;
export const footprints = footprintsData;
export const songs = songsData;

export function searchArticles(query) {
	const terms = String(query || '').trim().toLocaleLowerCase().split(/\s+/).filter(Boolean);
	if (!terms.length) return [];

	return articles.filter((article) => {
		const searchable = [article.title, article.summary, article.content, ...(article.tags || [])]
			.join('\n')
			.toLocaleLowerCase();
		return terms.every((term) => searchable.includes(term));
	});
}
