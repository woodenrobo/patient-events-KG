# patient-events-KG

> Extract medical entities from free text, build a knowledge graph, query it in natural language.

A portfolio project exploring **LLM-powered information extraction**, **graph databases**, and **agentic tool use** — applied to a realistic clinical domain.

Keywords: `Neo4j` · `Cypher` · `LiteLLM` · `FastAPI` · `Knowledge Graph` · `LLM agents`

---

## What it does

Patients submit free-text messages describing their medical history. A multi-agent pipeline handles the rest:

```
User message
     │
     ▼
┌─────────────────────┐
│  Orchestrator Agent │  classifies intent: INGEST | QUERY | BOTH
└─────────────────────┘
     │                 │
     ▼                 ▼
┌──────────┐    ┌────────────┐
│ Extract  │    │   Query    │
│  Agent   │    │   Agent    │
└──────────┘    └────────────┘
     │                 │
     ▼                 ▼
┌──────────┐    ┌────────────┐
│  Neo4j   │    │  Narrated  │
│  Graph   │    │  response  │
└──────────┘    └────────────┘
```

**Ingestion** — the extraction agent parses free text and writes structured nodes and relationships to Neo4j:

| Nodes | Relationships |
|---|---|
| Patient, Condition, Medication | `HAS_CONDITION`, `PRESCRIBED` |
| Symptom, CareEvent, Provider | `EXPERIENCED`, `VISITED`, `PRECEDED_BY` |

**Querying** — the query agent routes natural language questions to one of three Cypher queries, runs them, and narrates the results:

- *"What is the modal care path for patients with Long COVID?"*
- *"Which symptoms most commonly precede a diagnosis of X?"*
- *"What medications co-occur with symptom Y?"*

---

## Tech stack

| Layer | Technology |
|---|---|
| API | FastAPI (async) |
| LLM | LiteLLM → Gemini |
| Graph DB | Neo4j 5 (Docker) |
| Driver | neo4j async driver |
| Runtime | Python 3.12, uv |

---

## Installation

```bash
uv venv && uv sync
make run-neo4j   # starts Neo4j in Docker
make run         # starts FastAPI dev server
make seed        # populates graph with 10 Long COVID patient narratives
```

Neo4j is wrapped in Docker Compose and exposes:

- `http://localhost:7474` — Neo4j Browser
- `neo4j://localhost:7687` — Bolt driver

The backend defaults to these Neo4j settings unless you override them in `.env`:

```
NEO4J_URI=neo4j://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=neo4jpassword
NEO4J_DATABASE=neo4j
```

## Usage

Send any message to `POST /chat`:

```bash
# Ingest a patient narrative
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"user_message": "I am Sarah K. I was diagnosed with Long COVID after experiencing brain fog and fatigue. My doctor prescribed low-dose naltrexone. I visited a neurologist and a long COVID clinic."}'

# Query the graph
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"user_message": "What symptoms most commonly precede a Long COVID diagnosis?"}'
```
