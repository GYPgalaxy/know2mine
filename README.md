# 🧠 Smart Knowledge Hub

Smart Knowledge Hub is a lightweight, intelligent knowledge management web application designed to help you capture, organize, and retrieve your thoughts effortlessly. 

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
