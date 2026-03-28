# patient-events-KG
LLM extraction of event information and relationships from free text, Knowledge Graph generation and quering

Keywords: graph DBs (Neo4j, Cypher), data mining from free text, Knowledge Graph-based LLM tool use

This is a learning/portfolio project.

## Installation
- `uv venv && uv sync`
- Start Neo4j with `make run-neo4j`
- Run the API with `make run`

Neo4j is wrapped in Docker Compose and exposes:

- `http://localhost:7474` for Neo4j Browser
- `neo4j://localhost:7687` for the Bolt driver

The backend defaults to these Neo4j settings unless you override them in `.env`:

- `NEO4J_URI=neo4j://localhost:7687`
- `NEO4J_USERNAME=neo4j`
- `NEO4J_PASSWORD=neo4jpassword`
- `NEO4J_DATABASE=neo4j`

- Synthetic patient dialogues (JSON) for 3 patients
- an endpoint to talk to LLM to add dialogues
- LLM extraction layer (litellm)
    - entities: Patient, Condition, Medication, Symptom, CareEvent, Provider
    - relations: HAS_CONDITION, PRESCRIBED, EXPERIENCED, VISITED, PRECEDED_BY
- Neo4j ingestion (neo4j driver)
- Cypher query layer exposing:
    - "What's the modal care path for patients with condition X?"
    - "Which symptoms most commonly precede diagnosis Y?"
    - "What medications co-occur with symptom Z?"
- endpoint wrapping the Cypher queries in a simple API
- tool for the LLM to query the knowledge graph internally and return in the answer
