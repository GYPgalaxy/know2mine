# 🧠 Smart Knowledge Hub

[English](#english) | [中文](#chinese)

<a name="english"></a>

**Smart Knowledge Hub** is a lightweight, intelligent knowledge management web application designed to help you capture, organize, and retrieve your thoughts effortlessly. 

Built with **Streamlit** and powered by **AI**, it allows for quick text entry, automatic classification, and semantic search, ensuring you can always find what you need, when you need it.

## ✨ Features

*   **📝 Quick Capture**: Rapidly log your thoughts and notes via a simple, responsive interface.
*   **🤖 AI-Powered Organization**:
    *   **Auto-Classification**: Automatically categorizes your notes.
    *   **Smart Tagging**: Generates relevant tags for better organization.
    *   **Vector Embeddings**: Converts text to vectors for semantic understanding.
*   **🔍 Semantic Search**: Search by meaning, not just keywords. Find "that note about database design" even if you didn't use those exact words.
*   **⚡ Async Processing**: Heavy AI tasks run in the background using Redis & RQ, keeping the UI snappy.
*   **🗑️ Recycle Bin**: Safely delete notes with a soft-delete mechanism. Auto-cleans items older than 30 days.
*   **📱 Responsive UI**: Optimized for both PC and Mobile browsers.

## 🛠️ Tech Stack

*   **Frontend**: [Streamlit](https://streamlit.io/)
*   **Backend**: Python
*   **Database**: MySQL (Data storage), Redis (Task Queue & Cache)
*   **AI/ML**: OpenAI API (Embeddings & Completion) / Compatible with local LLMs
*   **Task Queue**: RQ (Redis Queue)
*   **Deployment**: Docker & Docker Compose

## 🚀 Getting Started

### Prerequisites

*   Docker & Docker Compose (Recommended)
*   **Or** Python 3.9+, MySQL Server, and Redis Server installed locally.

### 🐳 Method 1: Docker (Recommended)

1.  **Clone the repository**
    ```bash
    git clone https://github.com/yourusername/knowledge_manage.git
    cd knowledge_manage
    ```

2.  **Configure Environment**
    Copy the example environment file and fill in your details (especially `OPENAI_API_KEY`).
    ```bash
    cp .env.example .env
    ```

3.  **Start Services**
    ```bash
    docker-compose up -d --build
    ```
    This will start:
    *   `knowledge_web`: The Streamlit app (Port 8501)
    *   `knowledge_worker`: Background AI processor
    *   `knowledge_db`: MySQL database
    *   `knowledge_redis`: Redis server

4.  **Access the App**
    Open [http://localhost:8501](http://localhost:8501) in your browser.

### 🐍 Method 2: Local Installation

1.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Setup Configuration**
    Create a `.env` file (see `.env.example`) and configure your local MySQL and Redis credentials.

3.  **Initialize Database**
    ```bash
    python init_db.py
    ```

4.  **Run Background Worker** (in a separate terminal)
    ```bash
    python worker.py
    ```

5.  **Run the App**
    ```bash
    streamlit run app.py
    ```

## 📂 Project Structure

```
├── services/           # Business logic
│   ├── note_service.py # CRUD & DB operations
│   └── ai_service.py   # AI integration (OpenAI)
├── app.py              # Main Streamlit application
├── worker.py           # RQ Worker for background tasks
├── models.py           # SQLAlchemy Database Models
├── database.py         # Database connection setup
├── config.py           # Configuration management
├── init_db.py          # Database initialization script
├── docker-compose.yml  # Container orchestration
└── Dockerfile          # App container definition
```

## 🛡️ License

This project is licensed under the MIT License.

---

<a name="chinese"></a>

# 🧠 智能知识库 (Smart Knowledge Hub)

**智能知识库** 是一个轻量级、智能化的知识管理 Web 应用，旨在帮助您轻松捕捉、整理和检索想法。

基于 **Streamlit** 构建并由 **AI** 驱动，它支持快速文本录入、自动分类和语义搜索，确保您随时随地都能找到所需内容。

## ✨ 功能特性

*   **📝 快速捕捉**：通过简洁响应式的界面快速记录您的想法和笔记。
*   **🤖 AI 智能整理**：
    *   **自动分类**：自动对您的笔记进行分类。
    *   **智能标签**：生成相关标签以便更好地组织内容。
    *   **向量嵌入**：将文本转换为向量以进行语义理解。
*   **🔍 语义搜索**：按含义而非仅按关键词搜索。即使不记得确切的词，也能找到“关于数据库设计的那条笔记”。
*   **⚡ 异步处理**：繁重的 AI 任务通过 Redis 和 RQ 在后台运行，保持界面流畅。
*   **🗑️ 回收站**：提供软删除机制，安全删除笔记。自动清理超过 30 天的项目。
*   **📱 响应式 UI**：针对 PC 和移动端浏览器进行了优化。

## 🛠️ 技术栈

*   **前端**：[Streamlit](https://streamlit.io/)
*   **后端**：Python
*   **数据库**：MySQL (数据存储), Redis (任务队列 & 缓存)
*   **AI/ML**：OpenAI API (Embeddings & Completion) / 兼容本地 LLM
*   **任务队列**：RQ (Redis Queue)
*   **部署**：Docker & Docker Compose

## 🚀 快速开始

### 前置要求

*   Docker & Docker Compose (推荐)
*   **或者** 本地安装 Python 3.9+, MySQL Server, 和 Redis Server。

### 🐳 方法 1: Docker (推荐)

1.  **克隆仓库**
    ```bash
    git clone https://github.com/yourusername/knowledge_manage.git
    cd knowledge_manage
    ```

2.  **配置环境**
    复制示例环境文件并填写您的详细信息（特别是 `OPENAI_API_KEY`）。
    ```bash
    cp .env.example .env
    ```

3.  **启动服务**
    ```bash
    docker-compose up -d --build
    ```
    这将启动：
    *   `knowledge_web`: Streamlit 应用 (端口 8501)
    *   `knowledge_worker`: 后台 AI 处理器
    *   `knowledge_db`: MySQL 数据库
    *   `knowledge_redis`: Redis 服务器

4.  **访问应用**
    在浏览器中打开 [http://localhost:8501](http://localhost:8501)。

### 🐍 方法 2: 本地安装

1.  **安装依赖**
    ```bash
    pip install -r requirements.txt
    ```

2.  **设置配置**
    创建一个 `.env` 文件（参考 `.env.example`）并配置您的本地 MySQL 和 Redis 凭据。

3.  **初始化数据库**
    ```bash
    python init_db.py
    ```

4.  **运行后台 Worker** (在单独的终端中)
    ```bash
    python worker.py
    ```

5.  **运行应用**
    ```bash
    streamlit run app.py
    ```

## 📂 项目结构

```
├── services/           # 业务逻辑
│   ├── note_service.py # CRUD & 数据库操作
│   └── ai_service.py   # AI 集成 (OpenAI)
├── app.py              # Streamlit 主程序
├── worker.py           # 后台任务 RQ Worker
├── models.py           # SQLAlchemy 数据库模型
├── database.py         # 数据库连接设置
├── config.py           # 配置管理
├── init_db.py          # 数据库初始化脚本
├── docker-compose.yml  # 容器编排
└── Dockerfile          # 应用容器定义
```

## 🛡️ 许可证

本项目采用 MIT 许可证。
