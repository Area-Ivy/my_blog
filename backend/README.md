# FastAPI Backend

This backend provides article APIs using FastAPI with SQLAlchemy ORM. It supports SQLite (default) and MySQL (e.g., LAS).

## Setup

1. Create a virtual environment (recommended):
   - Windows (cmd):
     ```
     python -m venv .venv
     .venv\Scripts\activate
     ```
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Run

Development (auto-reload):
```
D:\code\blog\backend\.venv\Scripts\activate
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```
docker build -t myblog-backend:latest .
docker save -o myblog-backend.tar myblog-backend:latest

sudo docker rmi myblog-backend:latest
sudo docker rmi -f myblog-backend:latest
sudo docker load -i myblog-backend.tar
sudo docker run -d -p 8000:8000 --name myblog-backend myblog-backend

Or:
```
python backend/main.py
```

API docs will be available at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Configuration (.env)

Database config is read from environment variables using `python-dotenv`. You can place a `.env` file in the project root or in `backend/`:

- `DATABASE_URL` (optional; default: `sqlite:///./backend/blog.db`)
  - MySQL example (LAS): `mysql+pymysql://user:password@host:3306/db?charset=utf8mb4`
- Optional MySQL SSL variables (if your LAS instance enforces SSL):
  - `DB_SSL_CA` — absolute path to CA file
  - `DB_SSL_CERT` — absolute path to client cert
  - `DB_SSL_KEY` — absolute path to client key

Examples (Windows cmd):
```
set DATABASE_URL=mysql+pymysql://blog_user:StrongPass123@las-mysql.example.com:3306/blog?charset=utf8mb4
uvicorn backend.main:app --reload
```

Or create a `.env` file:
```
DATABASE_URL=mysql+pymysql://blog_user:StrongPass123@las-mysql.example.com:3306/blog?charset=utf8mb4
# DB_SSL_CA=C:\certs\ca.pem
# DB_SSL_CERT=C:\certs\client-cert.pem
# DB_SSL_KEY=C:\certs\client-key.pem
```

### OpenSearch/Bonsai configuration

To enable full-text search via Bonsai OpenSearch:

- `ES_URL` — Required. Full connection URL from Bonsai, e.g. `https://user:pass@my-cluster-123.bonsaisearch.net:443`.
- `ES_ARTICLES_INDEX` — Optional. Target index name (default `articles`).
- `ES_VERIFY_CERTS` — Optional (`true`/`false`). Defaults to `true`.
- `ES_ASSERT_HOSTNAME` — Optional. Set to `true` only if your cert SAN matches the hostname.
- `ES_CA_CERT` — Optional path to a CA bundle if Bonsai requires a custom chain.

**中文分词器配置说明：**

后端使用内置的 `ngram` 分词器进行中文文本分析，**无需安装任何插件**，适用于 Bonsai 等托管云服务。

**默认配置（适用于 Bonsai 等云服务）：**

- **索引分析器**：使用 `ngram` 分词器（2-3 字符长度），将中文文本切分成 2-3 个字符的子串
- **搜索分析器**：使用 `standard` 分词器，按标准方式分词

这种配置的优势：
- ✅ 无需安装插件，适用于所有 OpenSearch/Elasticsearch 服务（包括 Bonsai）
- ✅ 对中文有一定的支持，能匹配部分中文词汇
- ✅ 配置简单，开箱即用

**注意**：如果您的服务支持安装插件，可以使用 IK 分词器获得更好的中文分词效果（详见下方安装说明）。

#### 方式一：本地 Elasticsearch 安装

1. **查看 Elasticsearch 版本**：
   ```bash
   # 方法1：查看安装目录
   cat elasticsearch-*/config/elasticsearch.yml | grep cluster.name
   
   # 方法2：通过 API 查询
   curl http://localhost:9200
   ```

2. **根据版本安装 IK 插件**：
   ```bash
   # 进入 Elasticsearch 安装目录
   cd /path/to/elasticsearch
   
   # 方式A：在线安装（推荐，自动匹配版本）
   bin/elasticsearch-plugin install https://github.com/medcl/elasticsearch-analysis-ik/releases/download/v8.11.0/elasticsearch-analysis-ik-8.11.0.zip
   
   # 注意：请将 8.11.0 替换为您实际的 Elasticsearch 版本号
   # 查看可用版本：https://github.com/medcl/elasticsearch-analysis-ik/releases
   
   # 方式B：离线安装（如果无法访问外网）
   # 1. 先下载对应版本的插件 ZIP 文件
   # 2. 然后执行：
   bin/elasticsearch-plugin install file:///path/to/elasticsearch-analysis-ik-8.11.0.zip
   ```

3. **重启 Elasticsearch**：
   ```bash
   # 停止服务
   # 然后启动
   bin/elasticsearch
   ```

4. **验证安装**：
   ```bash
   # 查看已安装的插件
   bin/elasticsearch-plugin list
   
   # 应该能看到：analysis-ik
   
   # 或者通过 API 测试分词
   curl -X POST "localhost:9200/_analyze" -H 'Content-Type: application/json' -d'
   {
     "analyzer": "ik_max_word",
     "text": "中华人民共和国"
   }'
   ```

#### 方式二：本地 OpenSearch 安装

1. **安装 IK 插件**：
   ```bash
   # 进入 OpenSearch 安装目录
   cd /path/to/opensearch
   
   # 在线安装
   bin/opensearch-plugin install analysis-ik
   
   # 或者指定版本（如果需要特定版本）
   bin/opensearch-plugin install https://github.com/aparo/opensearch-analysis-ik/releases/download/v1.3.0/opensearch-analysis-ik-1.3.0.zip
   ```

2. **重启 OpenSearch**：
   ```bash
   bin/opensearch
   ```

3. **验证安装**：
   ```bash
   bin/opensearch-plugin list
   ```

#### 方式三：托管服务（Bonsai、阿里云等）

**重要**：当前的默认配置使用 `ngram` 分词器，**无需安装插件**，可直接用于 Bonsai 等云服务。

如果您使用的是托管服务（如 Bonsai、阿里云 Elasticsearch、腾讯云等）：

1. **Bonsai（推荐使用默认配置）**：
   - 当前默认配置使用 `ngram` 分词器，**无需安装任何插件**，可直接使用
   - 如果您需要更好的中文分词效果，可以：
     - 联系 Bonsai 支持团队，询问是否可以预装 IK 插件
     - 或者考虑升级到支持自定义插件的计划（如果可用）
   - **大多数情况下，使用默认的 `ngram` 配置即可满足需求**

2. **阿里云 Elasticsearch**：
   - 登录阿里云控制台
   - 进入 Elasticsearch 服务
   - 在"插件配置"页面搜索并安装 `analysis-ik` 插件
   - 插件安装后需要重启集群才能生效

3. **腾讯云 Elasticsearch**：
   - 登录腾讯云控制台
   - 进入 Elasticsearch 服务实例
   - 在"插件管理"中安装 `analysis-ik` 插件

#### Docker 环境安装

如果您使用 Docker 运行 Elasticsearch/OpenSearch：

1. **方法一：使用预装 IK 插件的镜像**：
   ```bash
   # 使用 medcl/elasticsearch-ik 镜像
   docker run -d -p 9200:9200 medcl/elasticsearch-ik:latest
   ```

2. **方法二：自定义 Dockerfile**：
   ```dockerfile
   FROM elasticsearch:8.11.0
   RUN bin/elasticsearch-plugin install https://github.com/medcl/elasticsearch-analysis-ik/releases/download/v8.11.0/elasticsearch-analysis-ik-8.11.0.zip
   ```

3. **方法三：在运行中安装（不推荐，重启后失效）**：
   ```bash
   docker exec -it <container_id> bin/elasticsearch-plugin install https://github.com/medcl/elasticsearch-analysis-ik/releases/download/v8.11.0/elasticsearch-analysis-ik-8.11.0.zip
   docker restart <container_id>
   ```

#### 常见问题

1. **版本不匹配错误**：
   - 确保 IK 插件版本与 Elasticsearch/OpenSearch 版本完全匹配
   - 查看 https://github.com/medcl/elasticsearch-analysis-ik/releases 找到对应版本

2. **权限问题**：
   - 确保有足够的文件系统权限安装插件
   - Linux/Mac 可能需要使用 `sudo`（不推荐，建议修改文件权限）

3. **网络问题**：
   - 如果无法访问 GitHub，可以使用镜像站点或离线安装
   - 某些企业网络可能需要配置代理

4. **验证插件是否生效**：
   ```bash
   # 测试 IK 分词器
   curl -X POST "http://localhost:9200/_analyze" -H 'Content-Type: application/json' -d'
   {
     "analyzer": "ik_max_word",
     "text": "这是一个测试"
   }'
   ```
   如果返回分词结果，说明安装成功。

#### 安装完成后的操作

安装完成后，后端会在启动时自动创建使用中文分词器的索引（前提是已设置 `ES_URL` 环境变量）。

**如果您使用的是 Bonsai 等云服务**：无需任何额外配置，后端会自动使用内置的 `ngram` 分词器，可直接使用。

**重要提示**：如果您的 Elasticsearch 集群之前已经存在 `articles` 索引，需要删除旧索引并重建，才能应用新的中文分词器配置。重建索引的步骤如下：

1. **删除旧索引**（可选，后端会自动处理）：
   ```bash
   # 通过 API 删除
   curl -X DELETE "http://localhost:9200/articles"
   ```

2. **重建索引**：
   ```bash
   # 重新索引所有文章数据
   python -m backend.reindex_articles --batch-size 200
   ```

   或者如果后端正在运行，只需重启后端服务，然后执行重建命令即可。

**注意**：每当您需要重建索引时（例如修改了分词器配置），都需要重新运行上述命令。

## Endpoints

- `GET /api/health` — health check
- `GET /api/articles` — list articles
  - Query params:
    - `page` (default 1)
    - `page_size` (default 10, max 100)
    - `q` — optional search in title/summary/tags
- `GET /api/articles/{id}` — get one article by id

## CORS

CORS is enabled for `http://localhost:5173` (Vite default) and a few common local ports.



