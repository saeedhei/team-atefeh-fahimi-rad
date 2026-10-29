docker compose up -d postgres

docker compose exec postgres pg_isready -U opsgenome -d opsgenome
# accepting connections


docker compose up -d --build api postgres

docker compose logs -f api

docker compose up -d --build api postgres

http://localhost:8000/health/db

http://localhost:8000/docs