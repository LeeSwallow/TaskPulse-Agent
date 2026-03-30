# Backend Architecture

## 목표

백엔드는 `TaskPulse Agent` 데스크톱 앱의 gRPC service, 스케줄 실행기, agent orchestration, 실행 이력 저장을 담당한다.

기술 스택:

- `uv`
- `Python gRPC`
- `LangChain`
- `LangGraph`
- `SQLAlchemy`
- `PostgreSQL`
- `pgvector`
- `Redis`

## 책임 범위

- user/workspace/agent 계층 관리
- 이벤트 등록, 수정, 삭제, 조회 gRPC
- 스케줄 계산 및 예약 실행
- 허용된 tool/MCP 범위 제한
- agent 실행 그래프 구성
- 실행 결과 저장 및 조회
- 알림과 운영 관측성 진입점 제공

## 적용할 디렉터리 구조

```text
BE/
  src/be/
    app.py
    config.py
    bootstrap.py
    presentation/
      grpc/
        server.py
        services/
          health_service.py
          workspace_service.py
          agent_service.py
          event_service.py
          execution_service.py
      api/
        router.py
        routes/
          health.py
          metrics.py
    application/
      services/
        health_service.py
        workspace_service.py
        agent_service.py
        event_service.py
        execution_service.py
    domain/
      entities/
        user.py
        workspace.py
        agent.py
        event.py
        execution.py
      repositories/
        user_repository.py
        workspace_repository.py
        agent_repository.py
        event_repository.py
        execution_repository.py
    infrastructure/
      db/
        base.py
        session.py
        models.py
      cache/
        redis_client.py
      repositories/
        sqlalchemy_user_repository.py
        sqlalchemy_workspace_repository.py
        sqlalchemy_agent_repository.py
        sqlalchemy_event_repository.py
        sqlalchemy_execution_repository.py
      vector/
        pgvector_store.py
    scheduler/
      engine.py
      recurrence.py
    agents/
      graph.py
      tool_registry.py
      nodes/
```

## 핵심 컴포넌트

### 1. Presentation Layer

- gRPC service 와 protobuf contract binding 을 담당한다.
- 선택적으로 health/metrics 용 HTTP endpoint 를 둘 수 있다.
- transport concern 만 처리하고 비즈니스 로직은 application layer 로 위임한다.

### 2. Application Layer

- 유스케이스와 서비스 orchestration 을 담당한다.
- 트랜잭션 경계와 도메인 객체 조합 지점을 가진다.
- scheduler, agent, repository 를 연결한다.

### 3. Domain Layer

- `User`, `Workspace`, `Agent`, `Event`, `Execution` 핵심 모델을 정의한다.
- 상태 전이와 검증 규칙을 이 계층에 둔다.
- 외부 프레임워크에 의존하지 않는 계약을 유지한다.

### 4. Infrastructure Layer

- PostgreSQL, pgvector, Redis, 외부 notification, LLM adapter 를 담당한다.
- SQLAlchemy model, Redis client, repository 구현체를 가진다.

### 5. Scheduler Layer

- 예약 이벤트를 주기적으로 스캔한다.
- 다음 실행 시각 계산과 중복 실행 방지를 담당한다.
- 만기 이벤트를 agent runner 로 전달한다.

Redis 사용 지점:

- scheduler wake-up signal
- duplicate run guard lock
- short-lived cache
- future pub/sub notification

### 6. Agent Layer

- LangGraph 로 실행 단계를 정의한다.
- 기본 노드는 `plan -> execute_tools -> summarize -> persist_result` 흐름을 가진다.
- 실제 사용 가능한 tool 은 이벤트에 등록된 allowlist 로 제한한다.

## 핵심 데이터 계층

### User

- `id: UUID`
- `display_name: str`
- `email: str | null`
- `role: Literal["owner", "member"]`

### Workspace

- `id: UUID`
- `user_id: UUID`
- `name: str`
- `timezone: str`

### Agent

- `id: UUID`
- `workspace_id: UUID`
- `name: str`
- `description: str`
- `status: Literal["active", "paused"]`

### Event

- `id: UUID`
- `agent_id: UUID`
- `title: str`
- `instruction: str`
- `schedule_type: Literal["once", "daily", "weekly"]`
- `run_at: datetime | null`
- `time_of_day: str | null`
- `days_of_week: list[int]`
- `timezone: str`
- `allowed_tools: list[str]`
- `notify_target: Literal["desktop", "dashboard", "slack", "notion"]`
- `status: Literal["active", "paused"]`
- `created_at: datetime`
- `updated_at: datetime`
- `last_run_at: datetime | null`
- `next_run_at: datetime | null`

### Execution

- `id: UUID`
- `workspace_id: UUID`
- `agent_id: UUID`
- `event_id: UUID`
- `status: Literal["pending", "running", "succeeded", "failed"]`
- `started_at: datetime`
- `finished_at: datetime | null`
- `summary: str`
- `steps: list[str]`
- `tool_results: list[dict]`
- `error: str | null`

### EmbeddingDocument

- `id: UUID`
- `source_type: str`
- `source_id: str`
- `content: str`
- `embedding: vector`
- `created_at: datetime`

## gRPC 계약

FE 와 BE 의 주 계약은 `proto/taskpulse/v1/taskpulse.proto` 로 정의한다.

핵심 service:

- `HealthService.Check`
- `WorkspaceService.ListWorkspaces`
- `AgentService.ListAgents`
- `EventService.ListEvents`
- `EventService.CreateEvent`
- `EventService.UpdateEvent`
- `EventService.DeleteEvent`
- `EventService.RunEvent`
- `EventService.PauseEvent`
- `EventService.ResumeEvent`
- `ExecutionService.ListExecutions`
- `ToolService.ListTools`

HTTP route 는 아래 목적에 한정한다.

- `/health`
- `/metrics`
- internal admin/debug endpoint

## 테스트 전략

### 단위 테스트

- schedule recurrence 계산
- event 상태 전이
- tool allowlist 필터링
- execution 상태 전이
- schema validation

### 통합 테스트

- gRPC event create/list/update/delete
- execution 조회
- scheduler tick 시 due event 처리
- PostgreSQL session wiring smoke test
- Redis client bootstrap smoke test
- gRPC server bootstrap smoke test

### 회귀 테스트

- timezone 경계
- daily/weekly recurrence 계산
- 허용되지 않은 tool 차단
- renderer 가 기대하는 proto contract 호환성
