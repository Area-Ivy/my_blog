# Area-Ivy's Blog

一个使用 Vue 3、Vite 和 Tailwind CSS 构建的纯静态个人博客。文章、工具、足迹和音乐均随 Git 仓库管理，不需要服务器或数据库。

## 本地运行

```bash
cd frontend
npm ci
npm run dev
```

生产构建：

```bash
cd frontend
npm run build
npm run preview
```

## 发布到 Cloudflare Pages

1. 登录 Cloudflare，进入 **Workers & Pages → Create application → Pages → Connect to Git**。
2. 选择 `Area-Ivy/my_blog` 仓库。
3. 使用以下构建配置：

   - Framework preset：`Vue`
   - Root directory：`frontend`
   - Build command：`npm run build`
   - Build output directory：`dist`

4. 部署完成后，在项目的 **Custom domains** 中添加 `area-ivy.cn`。
5. 确认新站点无误后，再停掉旧服务器。

`frontend/public/_redirects` 已处理 Vue Router 的页面刷新规则，不需要配置 Nginx。

## 发布文章

在 `frontend/src/content/articles/` 新建 Markdown 文件：

```markdown
---
id: "unique-id"
title: "文章标题"
slug: "article-slug"
summary: "文章摘要"
tags: ["Vue", "前端"]
created_at: "2026-09-27T10:00:00+08:00"
updated_at: "2026-09-27T10:00:00+08:00"
---

# 正文标题

这里使用 Markdown 编写正文。
```

提交并推送后，Cloudflare Pages 会自动重新构建。站内搜索会检索标题、摘要、标签和正文。

其他内容位于：

- `frontend/src/content/tools.json`
- `frontend/src/content/footprints.json`
- `frontend/src/content/songs.json`
- `frontend/public/media/`：图片和音频

## 从旧 API 重新导入

仓库保留了一次性迁移脚本。旧服务器仍可访问时，可以执行：

```bash
node scripts/import-api-content.mjs http://旧服务器:8000 http://旧服务器
```

脚本会导出文章并下载工具图片、足迹图片和音乐资源。再次运行可能覆盖同名内容，执行前请先提交当前修改。

## 目录说明

```text
frontend/
├── public/media/          # 随站点发布的静态资源
├── src/content/articles/ # Markdown 文章
├── src/content/*.json    # 工具、足迹和音乐数据
└── src/lib/content.js    # 内容加载与本地搜索
scripts/
└── import-api-content.mjs
backend/                  # 旧版 FastAPI，仅保留作迁移参考，部署不再使用
```
