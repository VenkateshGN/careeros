# CareerOS 🚀

**AI-Powered Career Assistant with Intelligent Long-Term Memory**

CareerOS is an AI-powered career development platform designed to provide personalized, context-aware assistance throughout a user's career journey.

The platform combines **AI assistance, persistent agent memory, resume intelligence, job matching, interview preparation, career analytics, and secure user management** into a single career platform.

---

## 📌 Project Overview

Traditional career platforms generally provide isolated services such as job listings, resume builders, interview preparation, or career advice.

CareerOS brings these capabilities together and introduces an **intelligent memory layer** that allows the AI assistant to retain relevant career context across interactions.

For example, CareerOS can use previously stored information such as:

* User skills
* Career goals
* Resume information
* Job preferences
* Previous conversations
* Interview preparation history
* Career development context

This enables the AI assistant to provide more personalized recommendations instead of treating every interaction as a completely new conversation.

---

# 🎯 Vision

Build an AI career platform that continuously learns from user interactions and provides **personalized, context-aware, and explainable career guidance** throughout a user's professional journey.

---

# 🎯 Mission

Build a maintainable, scalable, secure, and explainable AI-powered career platform while following professional software engineering practices and a structured Software Development Life Cycle (SDLC).

---

# ✨ Key Features

## 🤖 AI Career Assistant

CareerOS provides an AI-powered career assistant capable of helping users with:

* Career guidance
* Skill recommendations
* Career planning
* Resume-related questions
* Interview preparation
* Job-related questions
* Personalized career advice

The AI service is implemented through a dedicated service layer to maintain **loose coupling between the application and AI provider**.

---

## 🧠 Persistent Agent Memory

One of the core features of CareerOS is its persistent agent-memory architecture.

Instead of treating every conversation as an isolated interaction, relevant career context can be stored and reused by the AI assistant.

The memory system can maintain information such as:

* Conversation context
* Technical skills
* Career goals
* Resume context
* Job preferences
* Interview preparation context
* Career coaching information

This enables CareerOS to move toward a more personalized and context-aware AI experience.

---

## 📄 Resume Management

Users can manage their resumes through the platform.

Capabilities include:

* Resume upload
* Resume management
* Resume-related AI assistance
* Resume information processing
* Resume storage integration

Uploaded files are treated as user-generated application data and are excluded from source control.

---

## ✍️ AI Cover Letter Generation

CareerOS provides AI-assisted cover letter functionality.

Users can generate personalized cover letters based on relevant career and job information.

The system includes dedicated:

* API routes
* Database models
* Pydantic schemas
* Service-layer functionality

---

## 💼 Job Discovery & Matching

CareerOS provides job-related functionality including:

* Job listings
* Job search
* Job information
* Job matching
* Application-related functionality
* Career-oriented recommendations

The architecture is designed so job data can be extended with additional matching and recommendation capabilities.

---

## 🎤 Interview Preparation

CareerOS includes an interview preparation module designed to help users improve their interview readiness.

Potential capabilities include:

* Interview preparation
* Interview questions
* Interview sessions
* AI-assisted interview guidance
* Interview history

---

## 📊 Career Analytics

The analytics layer provides a foundation for tracking career-related information and presenting meaningful insights through the dashboard.

The system includes:

* Analytics API
* Analytics database model
* Analytics schemas
* Dashboard integration

---

## 🔐 Authentication & Security

CareerOS includes authentication and security functionality such as:

* User registration
* User login
* Password hashing
* Authentication dependencies
* Password reset
* Secure API access
* Security-focused automated tests

Security-sensitive configuration such as API keys, database credentials, and secret keys is intentionally excluded from source control.

---

# 🏗️ System Architecture

CareerOS follows a layered architecture designed to keep application components modular and maintainable.

```text
                         ┌───────────────────────┐
                         │      React Frontend   │
                         │   TypeScript + Vite   │
                         └───────────┬───────────┘
                                     │
                                     │ HTTP / REST API
                                     ▼
                         ┌───────────────────────┐
                         │      FastAPI Backend  │
                         │       Python          │
                         └───────────┬───────────┘
                                     │
              ┌──────────────────────┼──────────────────────┐
              │                      │                      │
              ▼                      ▼                      ▼
       ┌──────────────┐      ┌──────────────┐      ┌──────────────┐
       │ API Routes   │      │   Services   │      │   Schemas    │
       │              │      │              │      │  Pydantic    │
       └──────┬───────┘      └──────┬───────┘      └──────────────┘
              │                     │
              │                     ├───────────────┐
              │                     │               │
              ▼                     ▼               ▼
       ┌──────────────┐      ┌──────────────┐ ┌──────────────┐
       │ SQLAlchemy   │      │ AI Service   │ │ Storage      │
       │ ORM / Models │      │    Layer     │ │   Service    │
       └──────┬───────┘      └──────────────┘ └──────────────┘
              │
              ▼
       ┌───────────────────────┐
       │   CockroachDB Cloud   │
       │    Primary Database   │
       └───────────────────────┘
```

---

# 🧠 Agent Memory Architecture

The persistent-memory architecture is an important component of CareerOS.

```text
User
 │
 ▼
React Frontend
 │
 ▼
FastAPI AI Endpoint
 │
 ▼
AI Service
 │
 ├──────────────► Retrieve relevant memory
 │
 ▼
AI Provider
 │
 ▼
Generate personalized response
 │
 ▼
Store relevant context
 │
 ▼
CockroachDB Cloud
```

The memory layer allows the application to maintain user-specific career context across multiple interactions.

---

# 🛠️ Technology Stack

## Frontend

| Technology | Purpose                        |
| ---------- | ------------------------------ |
| React      | User interface                 |
| TypeScript | Type-safe frontend development |
| Vite       | Frontend build tooling         |
| Zustand    | State management               |
| Vitest     | Frontend testing               |
| CSS        | UI styling                     |

---

## Backend

| Technology | Purpose                      |
| ---------- | ---------------------------- |
| Python     | Backend programming language |
| FastAPI    | REST API framework           |
| SQLAlchemy | ORM                          |
| Pydantic   | Data validation              |
| Pytest     | Backend testing              |
| Celery     | Background task foundation   |

---

## Database

### CockroachDB Cloud

CareerOS uses **CockroachDB Cloud** as its primary application database.

CockroachDB provides a distributed SQL database architecture while maintaining compatibility with the PostgreSQL ecosystem.

The database stores application data including:

* Users
* Jobs
* Applications
* Resumes
* Agent memories
* Interviews
* Cover letters
* Analytics
* Password-reset information

Database access is implemented through **SQLAlchemy**.

---

## AI Layer

CareerOS uses a dedicated AI service layer.

The architecture intentionally avoids tightly coupling application routes directly to a specific AI provider.

```text
API Route
    │
    ▼
AI Service
    │
    ▼
AI Provider
```

This design makes it easier to replace or introduce different AI providers without rewriting the application's core business logic.

---

## DevOps & Infrastructure

* Git
* GitHub
* GitHub Actions
* Docker
* Docker Compose
* CI/CD
* CockroachDB Cloud

---

# 📁 Project Structure

```text
careeros/
│
├── .github/
│   └── workflows/
│       └── ci-cd.yml
│
├── backend/
│   │
│   ├── app/
│   │   ├── api/
│   │   │   ├── dependencies.py
│   │   │   └── routes/
│   │   │       ├── ai.py
│   │   │       ├── analytics.py
│   │   │       ├── auth.py
│   │   │       ├── cover_letters.py
│   │   │       ├── dashboard.py
│   │   │       ├── interviews.py
│   │   │       ├── jobs.py
│   │   │       ├── resumes.py
│   │   │       └── users.py
│   │   │
│   │   ├── core/
│   │   │   ├── cache.py
│   │   │   ├── celery_app.py
│   │   │   └── database.py
│   │   │
│   │   ├── models/
│   │   │   ├── agent_memory.py
│   │   │   ├── analytics.py
│   │   │   ├── cover_letter.py
│   │   │   ├── interview.py
│   │   │   ├── job.py
│   │   │   ├── password_reset.py
│   │   │   └── user.py
│   │   │
│   │   ├── schemas/
│   │   │   ├── ai.py
│   │   │   ├── analytics.py
│   │   │   ├── auth.py
│   │   │   ├── cover_letter.py
│   │   │   ├── interview.py
│   │   │   ├── job.py
│   │   │   └── user.py
│   │   │
│   │   ├── services/
│   │   │   ├── ai_service.py
│   │   │   ├── email_service.py
│   │   │   ├── storage.py
│   │   │   └── user_service.py
│   │   │
│   │   └── main.py
│   │
│   ├── tests/
│   │   ├── conftest.py
│   │   ├── test_agent_memory.py
│   │   ├── test_ai.py
│   │   ├── test_api.py
│   │   ├── test_applications.py
│   │   ├── test_dashboard.py
│   │   ├── test_database.py
│   │   ├── test_jobs.py
│   │   ├── test_password_reset.py
│   │   ├── test_profile.py
│   │   ├── test_resumes.py
│   │   ├── test_security.py
│   │   └── test_users.py
│   │
│   ├── scripts/
│   ├── uploads/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── requirements.txt
│
├── frontend/
│   │
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── store/
│   │   ├── tests/
│   │   ├── api/
│   │   ├── App.tsx
│   │   └── main.tsx
│   │
│   ├── public/
│   ├── package.json
│   ├── vite.config.ts
│   └── vitest.config.ts
│
├── docs/
│
├── scripts/
│
├── tests/
│
├── .gitignore
└── README.md
```

---

# 🔄 Development Workflow

CareerOS follows a feature-oriented Git workflow.

```text
                    ┌─────────────┐
                    │    main     │
                    └──────┬──────┘
                           │
                           ▼
                    ┌─────────────┐
                    │   develop   │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              ▼            ▼            ▼
        feature/*       fix/*       chore/*
```

Development changes are implemented and validated on the development branch before being integrated into the main branch.

---

# 🧪 Testing Strategy

CareerOS uses automated testing to reduce regressions and improve reliability.

## Backend Testing

The backend uses **Pytest**.

Tests cover areas such as:

* Authentication
* User management
* Database behavior
* AI endpoints
* Agent memory
* Jobs
* Applications
* Resumes
* Password reset
* Security
* Dashboard APIs

Run backend tests locally:

```bash
cd backend
pytest
```

---

## Frontend Testing

The frontend uses **Vitest**.

Run frontend tests:

```bash
cd frontend
npm test
```

Run the test suite once:

```bash
npm run test -- --run
```

---

# 🔄 Continuous Integration

GitHub Actions automatically validates changes pushed to the repository.

The CI pipeline currently performs:

```text
Git Push
    │
    ▼
GitHub Actions
    │
    ├── Backend Tests
    │
    ├── Frontend Build
    │
    └── Deployment Validation
```

The backend CI environment uses a PostgreSQL-compatible test service for automated testing, while **CockroachDB Cloud remains the primary application database**.

This separation keeps CI tests isolated from the production/cloud database.

---

# 🐳 Docker

Docker and Docker Compose are included to support reproducible development environments.

Example:

```bash
docker compose up --build
```

Stop the services:

```bash
docker compose down
```

---

# ⚙️ Local Development Setup

## 1. Clone the repository

```bash
git clone https://github.com/VenkateshGN/careeros.git
cd careeros
```

---

## 2. Create Python virtual environment

```bash
cd backend
python -m venv .venv
```

### Windows

```powershell
.venv\Scripts\Activate.ps1
```

### Linux / macOS

```bash
source .venv/bin/activate
```

---

## 3. Install backend dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure environment variables

Create a `.env` file inside the backend directory.

Example:

```env
DATABASE_URL=<COCKROACHDB_CONNECTION_STRING>

SECRET_KEY=<YOUR_SECRET_KEY>

GEMINI_API_KEY=<YOUR_GEMINI_API_KEY>

```

Never commit `.env` files or API credentials to Git.

---

# 🗄️ CockroachDB Cloud Setup

CareerOS uses CockroachDB Cloud as its primary database.

General setup:

```text
CareerOS Backend
       │
       │ SQLAlchemy
       ▼
CockroachDB Cloud
       │
       ▼
CareerOS Database
```

The database connection string should be provided through the `DATABASE_URL` environment variable.

Example:

```env
DATABASE_URL=postgresql://<username>:<password>@<host>:26257/<database>?sslmode=verify-full
```

Use the connection string provided by your CockroachDB Cloud cluster rather than committing credentials to the repository.

---

# ▶️ Running the Backend

From the `backend` directory:

```bash
uvicorn app.main:app --reload
```

The API will normally be available at:

```text
http://localhost:8000
```

FastAPI documentation:

```text
http://localhost:8000/docs
```

---

# ▶️ Running the Frontend

From the `frontend` directory:

```bash
npm install
npm run dev
```

The Vite development server will provide the local frontend URL.

---

# 🔐 Security Practices

CareerOS follows several security practices:

* Password hashing
* Environment-based secrets
* Authentication dependencies
* API-level validation
* Security-focused automated tests
* Sensitive file exclusion
* No API credentials committed to Git
* Uploaded user files excluded from source control

The `.gitignore` configuration prevents sensitive configuration and generated files from being committed.

---

# 📦 File Storage

User-generated files such as uploaded resumes are treated as application data rather than source code.

The repository does **not** store user resume files in Git.

For production deployment, the storage layer can be connected to an object-storage service such as Amazon S3.

The storage functionality is abstracted through a dedicated service layer to avoid coupling application logic directly to a specific storage provider.

---

# ☁️ Cloud & Scalability

CareerOS is designed with cloud deployment in mind.

Current architecture provides foundations for:

```text
                    Cloud Environment
                           │
             ┌─────────────┼─────────────┐
             │             │             │
             ▼             ▼             ▼
        Frontend       Backend API   CockroachDB
             │             │          Cloud
             │             │
             │             ├──── AI Service
             │             │
             │             ├──── Cache
             │             │
             │             └──── Background Tasks
             │
             ▼
          Users
```

The architecture can be extended with:

* Containerized backend deployment
* Object storage
* Managed caching
* Background workers
* Cloud monitoring
* Load balancing
* Automated deployment

---

# 🧩 Design Principles

CareerOS follows several software engineering principles.

### Separation of Concerns

API routes, business logic, database models, schemas, and infrastructure services are separated.

### Loose Coupling

External services such as AI providers and storage are accessed through service layers.

### Testability

Important application functionality is covered by automated tests.

### Maintainability

The codebase is organized into logical modules rather than placing all functionality into a single application file.

### Scalability

CockroachDB Cloud and modular backend services provide a foundation for future horizontal scaling.

### Security

Secrets and credentials are provided through environment variables rather than committed to source control.

---

# 📋 Development Roadmap

## Phase 1 — Foundation

* [x] FastAPI backend
* [x] React frontend
* [x] Database architecture
* [x] CockroachDB Cloud integration
* [x] User model
* [x] Authentication foundation
* [x] Git workflow
* [x] CI workflow

## Phase 2 — Core Career Features

* [x] Resume management
* [x] Job functionality
* [x] Dashboard
* [x] AI assistant
* [x] Agent memory foundation
* [x] Cover letters
* [x] Interview functionality
* [x] Career analytics

## Phase 3 — Engineering Quality

* [x] Automated backend tests
* [x] Frontend tests
* [x] CI validation
* [x] Security tests
* [x] Documentation
* [x] Code quality improvements

## Phase 4 — Cloud Deployment

* [ ] Production container deployment
* [ ] Production frontend deployment
* [ ] Cloud object storage
* [ ] Production monitoring
* [ ] Production secrets management
* [ ] Automated deployment to AWS

## Phase 5 — Advanced AI

* [ ] Improved long-term memory retrieval
* [ ] Semantic memory search
* [ ] Personalized career recommendations
* [ ] Advanced job matching
* [ ] AI interview simulation
* [ ] Career progression analytics

---

# 📊 Current Project Status

🚧 **Active Development**

CareerOS has progressed beyond a basic prototype and is being developed as a structured software engineering project.

Current focus areas include:

* Reliable AI services
* Persistent agent memory
* CockroachDB Cloud integration
* Automated testing
* CI/CD
* Security
* Maintainable architecture
* Cloud deployment readiness

---

# 🏆 Engineering Goals

The project is being developed with an emphasis on building a **real-world, internship-level software product** rather than only optimizing for a demonstration.

Primary engineering goals:

* Clean architecture
* Reliable APIs
* Persistent AI memory
* Scalable database design
* Secure authentication
* Automated testing
* CI/CD
* Maintainable code
* Clear documentation
* Cloud readiness

---

# 📚 Documentation

Additional project documentation is maintained inside the repository.

Recommended documentation areas include:

```text
docs/
├── architecture/
├── adr/
├── api/
├── database/
├── testing/
└── deployment/
```

Architecture Decision Records (ADRs) are used to document important technical decisions and their reasoning.

---

# 👨‍💻 Development

CareerOS is developed using a structured software development lifecycle.

```text
Requirements
     │
     ▼
Architecture
     │
     ▼
Implementation
     │
     ▼
Testing
     │
     ▼
CI Validation
     │
     ▼
Review
     │
     ▼
Deployment
     │
     ▼
Monitoring & Improvement
```

---

# 📜 License

This project is currently under active development.

License information will be added as the project moves toward public release.

---

# 🔗 Repository

**GitHub:**
https://github.com/VenkateshGN/careeros

---

# 👤 Author

**Venkatesh GN**
RV COLLEGE OF ENGINEERING | INFORMATION SCIENCE AND ENGINEERING

CareerOS — AI-powered career development platform.

---

## ⭐ Project Philosophy

> **CareerOS is not just an AI chatbot. It is a career intelligence platform designed around persistent context, modular architecture, and scalable software engineering practices.**
