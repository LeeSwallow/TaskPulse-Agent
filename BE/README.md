# TaskPulse Agent Backend

## Architecture

레이어드 아키텍처 기준:

- `presentation`: FastAPI routes, request/response schema
- `application`: use case and service orchestration
- `domain`: core entity and repository contract
- `infrastructure`: PostgreSQL, pgvector, Redis, external adapters

## Run

```bash
uv sync
uv run uvicorn be.app:app --reload
```

gRPC server:

```bash
uv run be-grpc
```

Proto binding refresh:

```bash
uv run python -m grpc_tools.protoc \
  -I .. \
  --python_out=src \
  --grpc_python_out=src \
  ../proto/taskpulse/v1/taskpulse.proto
```

## Test

```bash
uv run pytest
```

## Data Layer

- `PostgreSQL`
- `pgvector`
- `Redis`

기본 환경 변수:

```env
DATABASE_URL=postgresql+asyncpg://taskpulse:taskpulse@localhost:5432/taskpulse
REDIS_URL=redis://localhost:6379/0
```
