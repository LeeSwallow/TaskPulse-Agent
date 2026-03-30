# Backend Foundation Runtime Observability

## Summary

- 목적: 백엔드 런타임 기반, 이벤트 CRUD, 스케줄링 코어, 에이전트 실행 골격, 관찰 가능성 계층을 한 번에 정리한 구현 내용을 PR 기준으로 설명한다.
- 관련 브랜치: `feature/be-foundation-runtime-observability`
- 관련 커밋: `2574fe6 be: implement backend runtime, agent execution, and observability (#2 #3 #4)`

## Background

- MVP 백엔드는 문서상으로만 정의되어 있었고 실제 실행 가능한 API, 스케줄러, 에이전트 런너, 저장소 계층이 필요했다.
- 이후 프런트엔드와 연결하거나 별도 기능 PR을 쪼개기 전에, 백엔드 기반 레이어가 어떤 상태까지 구현되었는지 문서로 정리할 필요가 있다.

## Scope

### Included

- FastAPI 앱 팩토리와 lifespan 기반 리소스 초기화/정리
- 설정 로더와 bootstrap 기반 의존성 조립
- 이벤트 도메인 모델, DTO, 서비스, 저장소 인터페이스
- SQLAlchemy 기반 이벤트 저장소와 DB 세션 매니저
- Redis 클라이언트 매니저
- `/api/events`, `/health` API
- gRPC 서버 부트스트랩과 health 서비스
- LangGraph 기반 `plan -> execute_tools -> summarize` 에이전트 실행 골격
- 스케줄 next run 계산 및 due event 수집 로직
- 구조화 로깅 및 in-memory metric registry
- 도메인, 애플리케이션, API, 인프라, 스케줄러, gRPC, 관찰 가능성 테스트

### Not Included

- 실제 외부 MCP/tool provider 연동
- execution 영속화 완성 및 실행 이력 조회 API
- 스케줄러의 백그라운드 루프/잡 실행 오케스트레이션
- 알림 채널 연동
- 인증/인가
- CI/CD 워크플로 설정

## Acceptance Criteria Mapping

- 이벤트 CRUD API가 생성/조회/수정/삭제 흐름을 제공한다.
- 스케줄 계산이 once/daily/weekly 기준으로 다음 실행 시각을 계산한다.
- paused 이벤트는 due 대상으로 간주하지 않는다.
- 허용된 tool만 에이전트 실행 계획에 반영된다.
- API와 gRPC 엔트리포인트가 애플리케이션 컨테이너를 통해 기동된다.
- 로깅/메트릭 훅이 런타임 계층에 연결된다.

## Implementation Notes

### Architecture / Design

- 앱 조립은 [bootstrap.py](/home/min/Workspace/working/chatbot/BE/src/be/bootstrap.py) 에서 수행한다.
- FastAPI 앱은 [app.py](/home/min/Workspace/working/chatbot/BE/src/be/app.py) 에서 컨테이너를 만들고 DB schema 초기화와 Redis 정리를 lifespan에 묶는다.
- 설정은 [config.py](/home/min/Workspace/working/chatbot/BE/src/be/config.py) 에서 환경 변수 기반으로 로드한다.
- 레이어 경계는 `presentation -> application -> domain -> infrastructure` 순서로 유지한다.

### Key Files

- API 엔트리: [app.py](/home/min/Workspace/working/chatbot/BE/src/be/app.py)
- gRPC 엔트리: [grpc_app.py](/home/min/Workspace/working/chatbot/BE/src/be/grpc_app.py)
- 이벤트 서비스: [service.py](/home/min/Workspace/working/chatbot/BE/src/be/application/events/service.py)
- 이벤트 라우트: [routes.py](/home/min/Workspace/working/chatbot/BE/src/be/presentation/api/v1/events/routes.py)
- 이벤트 저장소: [event_repository.py](/home/min/Workspace/working/chatbot/BE/src/be/infrastructure/db/repositories/event_repository.py)
- 스케줄 계산: [recurrence.py](/home/min/Workspace/working/chatbot/BE/src/be/scheduler/recurrence.py)
- due 판별: [engine.py](/home/min/Workspace/working/chatbot/BE/src/be/scheduler/engine.py)
- 에이전트 그래프: [graph.py](/home/min/Workspace/working/chatbot/BE/src/be/agents/graph.py)
- 메트릭 레지스트리: [metrics.py](/home/min/Workspace/working/chatbot/BE/src/be/observability/metrics.py)

### API / Interface Changes

- `GET /health`
- `GET /api/events`
- `POST /api/events`
- `PATCH /api/events/{event_id}`
- `DELETE /api/events/{event_id}`

### Data / Runtime Notes

- 기본 `DATABASE_URL` 은 PostgreSQL async URL 이지만 테스트에서는 SQLite로 오버라이드한다.
- Redis는 런타임 자원으로 초기화되지만, 현재 단계에서는 캐시/큐 시나리오보다 연결 관리 기반에 가깝다.
- Proto 바인딩 파일이 저장소에 포함되어 있어 gRPC health 서비스 구동 기반이 있다.

## Test Plan

### Automated

- 표준 명령: `uv run pytest`
- 주요 범위:
- `BE/tests/api/test_events_api.py`
- `BE/tests/application/test_event_service.py`
- `BE/tests/domain/test_event_schema.py`
- `BE/tests/infrastructure/test_event_repository.py`
- `BE/tests/scheduler/test_recurrence.py`
- `BE/tests/scheduler/test_engine.py`
- `BE/tests/agents/test_runner.py`
- `BE/tests/grpc/test_grpc_server.py`
- `BE/tests/observability/test_logging.py`

### Manual

- `uv run uvicorn be.app:app --reload` 로 FastAPI 기동
- `uv run be-grpc` 로 gRPC 서버 기동
- `/api/events` CRUD 및 `/health` 응답 확인

## Risks

- 실행 이력 `Execution` 모델은 존재하지만 영속화/조회 흐름이 아직 완결되지 않았다.
- 스케줄러는 계산/필터링 함수 수준이며, 실제 주기 실행 엔진과 중복 실행 방지까지는 연결되지 않았다.
- 에이전트 런너는 골격과 allowlist 중심 구현이며, 실제 외부 도구 연동과 장애 복구는 후속 작업이 필요하다.
- proto 생성 파일과 캐시 산출물 관리 기준이 추가로 필요하다.

## Follow-up

- `POST /api/events/{event_id}/run`, execution history API, notification adapter 구현
- execution repository 및 상태 전이 영속화
- scheduler loop 와 agent runner 연결
- CI 파이프라인에서 `uv run pytest` 와 정적 검증을 머지 게이트로 추가
- 생성 산출물과 캐시 파일의 버전 관리 기준 명확화

## Reviewer Checklist

- 이벤트 CRUD와 스케줄 계산 범위가 현재 작업 목적과 일치하는가
- 레이어 분리가 실제 코드에서 유지되는가
- 테스트가 핵심 동작과 회귀 지점을 충분히 덮는가
- 아직 미구현인 실행 이력/수동 실행/알림 기능이 문서에 명확히 드러나는가
