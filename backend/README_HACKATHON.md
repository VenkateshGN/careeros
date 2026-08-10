# CareerOS: Agentic Memory System (CockroachDB × AWS Hackathon)

## The Core Concept
AI agents are rapidly scaling, and they require persistent, fault-tolerant memory that never goes offline. CareerOS relies heavily on Agentic memory to remember a candidate's conversation context, technical proficiencies, resume vectors, and structural AI coaching parameters.

This project fulfills the **CockroachDB × AWS Hackathon** by migrating the core algorithmic AI layers of the system to rely natively on:
1. **Amazon Bedrock (AWS Tools)**
2. **CockroachDB Distributed Vector Indexing**
3. **CockroachDB Cloud Managed MCP Server**

Instead of standard LLM wrappers, CareerOS physically commits the AI conversational stream asynchronously into a geographically distributed **CockroachDB Cluster** utilizing `pgvector` models natively bound in SQLAlchemy.

---

## 🚀 How we leverage AWS & Cockroach

### 1. Amazon Bedrock (Titan & Claude 3)
CareerOS utilizes the `boto3` Bedrock Runtime endpoints.
- Prompting & Conversational Agent Logic parses securely through `anthropic.claude-3`.
- 1536-dimensional Vectors are natively extracted from memory contexts utilizing the `amazon.titan-embed-text-v1` embedding capabilities.

### 2. CockroachDB Distributed Vector Indexing (`agent_memory` schema)
To achieve semantic retrieval instantaneously, AWS Titan embeddings are injected via CockroachDB `VECTOR` types (`<->` operations determining L2 distances)!
Whenever a user interacts with the AI services, CareerOS calculates mathematical affinity to fetch top-limit contextual memories seamlessly scaling linearly matching the CockroachDB distributed hash capabilities. Look in `app/api/routes/ai.py` for natively implemented routing.

### 3. CockroachDB Cloud Managed MCP Server
We provide the raw configuration required to natively tunnel any local LLM operations securely to monitor this Agent cluster (e.g. for VS Code / Cursor interactions validating the `agent_memories` ORM tables via `https://cockroachlabs.cloud/mcp`).
Checkout the configuration manifest at `backend/mcp_config.json`.

---

## Technical Stack
- **Database**: CockroachDB V23+ (PostgreSQL dialect w/ pgvector extensions).
- **Backend**: Python FastAPI, SQLAlchemy (Cockroach-Psycopg2 Engine).
- **AI Runtimes**: Amazon Bedrock SDK (`boto3`)
- **Frontend Tools**: React (Vite / Zustand), Vitest validations.
