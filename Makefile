run:
	uv run fastapi dev main.py --reload-dir app

run-neo4j:
	docker compose up -d neo4j

stop-neo4j:
	docker compose stop neo4j

seed:
	bash scripts/seed/seed.sh
