# ⚽ Football Multi-Agent Analyst

> **A production-ready multi-agent football analysis system built with LangGraph, FastAPI, Streamlit, Docker, and deployed on Render.**

This project demonstrates a production-ready **Multi-Agent AI** application where a **Supervisor Agent** coordinates multiple specialized football agents running in parallel to answer user queries. The system combines **LangGraph** for orchestration, **FastAPI** for the backend, **Streamlit** for the frontend, and **Docker** for deployment.

---

# 🚀 Live Demo

🌐 **Application:** *(Render Deployment URL)*

📦 **GitHub Repository:** https://github.com/Innovatewithapple/Football-Multi-Agent-Analyst

---

# 🎯 Project Highlights

- ⚽ Multi-Agent architecture using LangGraph
- 🤖 Supervisor Agent coordinating specialized AI agents
- ⚡ Parallel execution of Match, Player, and News agents
- 🔄 Graph-based workflow orchestration
- 🌐 FastAPI REST API
- 💻 Interactive Streamlit interface
- 🐳 Dockerized deployment
- ☁️ Deployed on Render
- 🔀 Modular and extensible architecture

---

# 🏗️ System Architecture

```text
                User
                 │
                 ▼
        Streamlit Frontend
                 │
                 ▼
          FastAPI Backend
                 │
                 ▼
        LangGraph Workflow
                 │
                 ▼
         Supervisor Agent
                 │
      ┌──────────┼──────────┐
      │          │          │
      ▼          ▼          ▼
 Match Agent  Player Agent  News Agent
      │          │          │
      └──────────┼──────────┘
                 ▼
      Merge Agent Responses
                 │
                 ▼
       Final Football Analysis
```

The **Supervisor Agent** determines which specialized agents should execute for a given request. Independent agents run in parallel whenever applicable, and their outputs are combined into a single response returned to the user.

---

# ⚙️ Technology Stack

| Component | Technology |
|-----------|------------|
| Agent Framework | LangGraph |
| LLM Framework | LangChain |
| Backend | FastAPI |
| Frontend | Streamlit |
| API Documentation | Swagger / OpenAPI |
| Deployment | Render |
| Containerization | Docker |
| Language | Python |

---

# ✨ Features

- Multi-agent orchestration using LangGraph
- Supervisor-driven workflow execution
- Parallel execution of specialized agents
- Football match analysis
- Player comparison and insights
- Latest football news retrieval
- REST API for programmatic access
- Interactive Streamlit web interface
- Docker support for easy deployment
- Cloud deployment on Render
- Modular architecture for adding new agents

---

# 🚀 Getting Started

## Clone the Repository

```bash
git clone https://github.com/Innovatewithapple/Football-Multi-Agent-Analyst.git
cd Football-Multi-Agent-Analyst
```

## Create Environment Variables

Create a `.env` file in the project root.

```env
NVDIA_API_Key=your_nvidia_api_key
GROQAPI=your_groq_api_key
NEWSAPI_KEY=your_newsapi_key
```

## Build Docker Image

```bash
docker build -t football-multi-agent .
```

## Run the Application

```bash
docker run \
  -p 8000:8000 \
  -p 7860:7860 \
  --env-file .env \
  football-multi-agent
```

Once the container starts:

- 🌐 Streamlit UI → `http://localhost:7860`
- 📖 FastAPI Documentation → `http://localhost:8000/docs`
- ⚙️ FastAPI API → `http://localhost:8000`

---

# 📂 Repository Structure

```text
.
├── agents/
├── api/
├── app/
├── graph/
├── streamlit/
├── Dockerfile
├── start.sh
├── requirements.txt
└── README.md
```

---

# 💡 Example Queries

- Compare Lionel Messi and Cristiano Ronaldo.
- Analyze the latest Manchester City match.
- Show the latest football news.
- Compare two football clubs.
- Summarize a player's recent performances.
- Combine player analysis with the latest football news.

---

# 🔮 Future Improvements

- Live match statistics integration
- Additional specialized agents
- Multi-language support
- Conversation memory
- Historical performance analytics
- Match prediction workflows
- Interactive visualizations
