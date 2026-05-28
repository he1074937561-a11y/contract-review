# AI Contract Review - AI 合同审查助手

面向政府机关和事业单位的轻量化智能合同审查工具，帮助非专业人士也能快速识别合同风险、规范审查流程。

## 项目简介

AI Contract Review 是一款 **AI 原生** 的合同审查系统，以 DeepSeek 大语言模型为核心驱动，支持合同上传、自动风险审查、报告生成和历史管理。

### 核心功能

- **合同上传与解析** — 支持 PDF、Word 文档上传，自动提取文本内容
- **AI 风险审查** — 基于 DeepSeek 大模型对合同进行多维度风险分析
- **审查工作台** — 合同原文与风险标注同屏对照，逐条审阅
- **审查报告** — 自动生成结构化审查报告，支持归档和追溯
- **审查历史** — 完整的审查记录管理，审计留痕
- **模板管理** — 自定义审查模板和审查要点（管理员）
- **AI 对话** — 针对单份合同进行追问和深度分析
- **用户管理** — 基于 JWT 的认证与角色权限控制

### 技术栈

| 层级 | 技术选型 |
|------|----------|
| 前端 | Vue 3 + TypeScript + Vite + Naive UI + Pinia + Vue Router |
| 后端 | Python FastAPI + SQLAlchemy (异步) + Alembic |
| AI | DeepSeek API (OpenAI 兼容接口) |
| 数据库 | SQLite (开发) / MySQL (生产) |
| 认证 | JWT (python-jose) |

## 快速开始

### 前置要求

- Python 3.11+
- Node.js 18+
- DeepSeek API Key（或兼容的 OpenAI API Key）

### 1. 克隆项目

```bash
git clone https://github.com/<your-username>/contract-review.git
cd contract-review
```

### 2. 后端启动

```bash
# 进入后端目录
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env，填入你的 LLM_API_KEY

# 启动服务
uvicorn app.main:app --reload --port 8000
```

后端运行在 http://localhost:8000，API 文档访问 http://localhost:8000/docs。

### 3. 前端启动

```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端运行在 http://localhost:5173。

### 4. 访问系统

打开浏览器访问 http://localhost:5173，注册账号后即可使用。

## 生产部署

### 使用 Docker Compose（MySQL + 后端 + 前端）

```bash
docker-compose up -d
```

> 注意：生产环境需要配置 MySQL 连接串和安全的 SECRET_KEY。

### 环境变量说明

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `DATABASE_URL` | 数据库连接串 | `sqlite+aiosqlite:///./contract_review.db` |
| `SECRET_KEY` | JWT 签名密钥 | `dev-secret-key` |
| `LLM_API_KEY` | DeepSeek / OpenAI API Key | — |
| `LLM_MODEL` | 模型名称 | `deepseek-chat` |
| `LLM_BASE_URL` | API 地址 | `https://api.deepseek.com` |
| `CORS_ORIGINS` | 允许的前端域名 | `http://localhost:5173` |
| `UPLOAD_DIR` | 合同文件上传目录 | `uploads` |

## 项目结构

```
contract-review/
├── backend/
│   ├── app/
│   │   ├── core/          # 配置、数据库、依赖注入
│   │   ├── llm/           # AI 审查引擎
│   │   ├── modules/       # 业务模块
│   │   │   ├── auth/      # 认证
│   │   │   ├── contracts/ # 合同管理
│   │   │   ├── risks/     # 风险审查
│   │   │   ├── reports/   # 报告管理
│   │   │   ├── chat/      # AI 对话
│   │   │   └── admin/     # 后台管理
│   │   └── main.py        # FastAPI 入口
│   ├── alembic/           # 数据库迁移
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/           # API 请求层
│   │   ├── components/    # 公共组件
│   │   ├── stores/        # Pinia 状态管理
│   │   ├── views/         # 页面组件
│   │   └── router/        # 路由配置
│   └── package.json
├── docs/                  # 项目文档
└── docker-compose.yml
```

## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| POST | `/api/auth/register` | 用户注册 |
| POST | `/api/auth/login` | 用户登录 |
| POST | `/api/contracts/upload` | 上传合同 |
| GET | `/api/contracts/` | 合同列表 |
| POST | `/api/risks/review` | AI 审查合同 |
| GET | `/api/reports/{id}` | 获取审查报告 |
| POST | `/api/chat/ask` | AI 对话 |
| GET | `/api/admin/templates` | 审查模板管理 |
| GET | `/api/health` | 健康检查 |

## 开源协议

[MIT](LICENSE)

---

> 欢迎提交 Issue 和 PR。
