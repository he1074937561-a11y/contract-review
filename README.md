<p align="center">
  <img src="https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi" alt="FastAPI">
  <img src="https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vuedotjs" alt="Vue.js">
  <img src="https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript" alt="TypeScript">
  <img src="https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite" alt="SQLite">
  <img src="https://img.shields.io/badge/license-MIT-blue?style=for-the-badge" alt="MIT">
</p>

<br>

<div align="center">

# 智审通

### AI 原生合同审查助手 — 让每份合同都经得起推敲

**面向政府机关和事业单位的轻量化智能合同审查工具，帮助非专业人士也能快速识别合同风险、规范审查流程。**

<br>

[快速开始](#快速开始) • [功能一览](#核心功能) • [技术栈](#技术栈) • [项目文档](#项目文档) • [API 文档](#api-接口) • [部署](#生产部署)

</div>

<br>

---

## 产品概览

AI Contract Review 以 **DeepSeek 大模型**为核心驱动，实现合同审查全流程智能化：

```
上传合同 → AI 多维度审查 → 风险标注与评分 → 自动生成报告 → 归档追溯
```

> 项目配套完整的[产品文档](./docs)，涵盖市场分析、用户研究、产品方案、PRD、技术方案、提示词工程、测试方案及运营推广策略，欢迎查阅。

---

## 核心功能

<table>
  <tr>
    <td width="200" align="center">
      <b>📄 合同上传与解析</b>
    </td>
    <td>支持 PDF、Word 文档上传，自动提取文本内容</td>
  </tr>
  <tr>
    <td align="center"><b>🤖 AI 风险审查</b></td>
    <td>DeepSeek 多维度分析：权利义务对等性、违约责任、争议解决、支付条款、质量验收、法律时效</td>
  </tr>
  <tr>
    <td align="center"><b>🔍 审查工作台</b></td>
    <td>合同原文与 AI 风险标注同屏对照，逐条审阅确认</td>
  </tr>
  <tr>
    <td align="center"><b>📊 审查报告</b></td>
    <td>自动生成结构化审查报告，含合规评分、风险分级、法律依据和修改建议</td>
  </tr>
  <tr>
    <td align="center"><b>📚 审查历史</b></td>
    <td>完整的审查记录管理，审计留痕，支持追溯查阅</td>
  </tr>
  <tr>
    <td align="center"><b>💬 AI 对话</b></td>
    <td>针对单份合同进行追问和深度分析，像和律师对话一样</td>
  </tr>
  <tr>
    <td align="center"><b>📋 模板管理</b></td>
    <td>自定义审查模板和审查要点，适配不同合同类型（管理员）</td>
  </tr>
  <tr>
    <td align="center"><b>🔐 用户管理</b></td>
    <td>JWT 认证 + 角色权限控制，保障数据安全</td>
  </tr>
</table>

---

## 技术栈

| 层级 | 技术选型 |
|------|----------|
| **前端** | Vue 3 + TypeScript + Vite + Naive UI + Pinia + Vue Router |
| **后端** | Python FastAPI + SQLAlchemy（异步）+ Alembic |
| **AI** | DeepSeek API（兼容 OpenAI 接口协议） |
| **数据库** | SQLite（开发）/ MySQL（生产） |
| **认证** | JWT（python-jose）+ bcrypt 密码加密 |

---

## 快速开始

### 前置要求

- Python 3.11+
- Node.js 18+
- DeepSeek API Key（或任意兼容 OpenAI 接口的 API Key）

### 1. 克隆项目

```bash
git clone https://github.com/he1074937561-a11y/contract-review.git
cd contract-review
```

### 2. 启动后端

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate      # Linux / macOS
# venv\Scripts\activate       # Windows

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env，填入你的 LLM_API_KEY

# 启动后端服务
uvicorn app.main:app --reload --port 8000
```

> 后端运行在 http://localhost:8000，自动生成 API 文档：http://localhost:8000/docs

### 3. 启动前端

```bash
cd frontend

npm install
npm run dev
```

> 前端运行在 http://localhost:5173

### 4. 访问系统

打开浏览器访问 **http://localhost:5173**，注册账号后即可使用。

---

## 生产部署

### 使用 Docker Compose

```bash
docker-compose up -d
```

将启动 MySQL + 后端 + 前端完整服务栈。

> **注意**：生产环境请务必修改 `SECRET_KEY` 并配置 MySQL 连接串。

### 环境变量

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `DATABASE_URL` | 数据库连接串 | `sqlite+aiosqlite:///./contract_review.db` |
| `SECRET_KEY` | JWT 签名密钥 | `dev-secret-key` |
| `LLM_API_KEY` | DeepSeek / OpenAI API Key | — |
| `LLM_MODEL` | 模型名称 | `deepseek-chat` |
| `LLM_BASE_URL` | API 地址 | `https://api.deepseek.com` |
| `CORS_ORIGINS` | 允许的前端域名 | `http://localhost:5173` |
| `UPLOAD_DIR` | 合同文件上传目录 | `uploads` |

---

## 项目文档

本项目完整开源了全套产品文档，位于 [`docs/`](./docs) 目录：

| 文档 | 说明 |
|------|------|
| [01-市场分析文档](./docs/01-市场分析文档.md) | 目标市场、竞品分析、SWOT 分析 |
| [02-用户研究文档](./docs/02-用户研究文档.md) | 用户画像、需求分析、使用场景 |
| [03-产品方案文档](./docs/03-产品方案文档.md) | 产品定位、功能规划、路线图 |
| [04-PRD-原型设计文档](./docs/04-PRD-原型设计文档.md) | 详细功能需求、页面流程图、交互原型 |
| [05-技术方案文档](./docs/05-技术方案文档.md) | 系统架构、技术选型、数据库设计 |
| [06-提示词工程文档](./docs/06-提示词工程文档.md) | 审查提示词设计、调优策略 |
| [07-测试方案文档](./docs/07-测试方案文档.md) | 测试策略、用例设计、验收标准 |
| [08-运营推广方案](./docs/08-运营推广方案.md) | 运营策略、推广渠道、效果评估 |

另有交互原型位于 [`docs/prototype/`](./docs/prototype/)。

---

## 项目结构

```
contract-review/
├── backend/
│   ├── app/
│   │   ├── core/              # 配置 / 数据库 / 依赖注入
│   │   ├── llm/               # AI 审查引擎（DeepSeek）
│   │   ├── modules/
│   │   │   ├── auth/          # 认证模块
│   │   │   ├── contracts/     # 合同管理
│   │   │   ├── risks/         # 风险审查
│   │   │   ├── reports/       # 报告管理
│   │   │   ├── chat/          # AI 对话
│   │   │   └── admin/         # 后台管理
│   │   └── main.py            # FastAPI 入口
│   ├── alembic/               # 数据库迁移
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/               # API 请求层
│   │   ├── components/        # 公共组件
│   │   ├── stores/            # Pinia 状态管理
│   │   ├── views/             # 页面组件
│   │   └── router/            # 路由配置
│   └── package.json
├── docs/                      # 项目文档（已开源）
│   ├── 01-市场分析文档.md
│   ├── 02-用户研究文档.md
│   ├── ...
│   └── prototype/             # 交互原型
└── docker-compose.yml
```

---

## API 接口

| 方法 | 路径 | 说明 |
|------|------|------|
| `POST` | `/api/auth/register` | 用户注册 |
| `POST` | `/api/auth/login` | 用户登录 |
| `POST` | `/api/contracts/upload` | 上传合同 |
| `GET` | `/api/contracts/` | 合同列表 |
| `POST` | `/api/risks/review` | AI 审查合同 |
| `GET` | `/api/reports/{id}` | 获取审查报告 |
| `POST` | `/api/chat/ask` | AI 对话 |
| `GET` | `/api/health` | 健康检查 |

完整 API 文档请访问运行后的 `/docs` 端点。

---

## 开源协议

[MIT](LICENSE)

---

<p align="center">
  欢迎提交 <a href="https://github.com/he1074937561-a11y/contract-review/issues">Issue</a> 和 <a href="https://github.com/he1074937561-a11y/contract-review/pulls">PR</a>
  <br>
  Made with ❤️
</p>
