# Backend Architecture

## 목표

백엔드는 예약형 agent 서비스를 위한 API, 스케줄 실행기, agent orchestration, 실행 이력 저장을 담당한다.

기술 스택:

- `uv`
- `FastAPI`
- `LangChain`
- `LangGraph`

## 책임 범위

- 이벤트 등록, 수정, 삭제, 조회 API
- 스케줄 계산 및 예약 실행
- 허용된 tool/MCP 범위 제한
- agent 실행 그래프 구성
- 실행 결과 저장 및 조회
- 향후 알림 채널 연동의 진입점 제공

## 제안 디렉터리 구조

```text
BE/
  src/be/
    app.py
    config.py
    api/
      routes/
        events.py
        executions.py
        tools.py
    domain/
      models/
        event.py
        execution.py
        tool.py
      services/
        event_service.py
        execution_service.py
    agents/
      graph.py
      nodes/
        planner.py
        tool_executor.py
        summarizer.py
      tool_registry.py
    scheduler/
      engine.py
      recurrence.py
    infra/
      repositories/
      notifications/
      persistence/
    tests/
```

## 핵심 컴포넌트

### 1. API Layer

- FastAPI route 에서 요청 검증과 응답 직렬화를 담당한다.
- 비즈니스 로직은 service 계층으로 위임한다.

### 2. Domain Layer

- `Event`, `Execution`, `ToolDefinition` 등 핵심 모델을 정의한다.
- 상태 전이와 검증 규칙을 이 계층에 둔다.

### 3. Scheduler Layer

- 예약 이벤트를 주기적으로 스캔한다.
- 다음 실행 시각 계산과 중복 실행 방지를 담당한다.
- 만기 이벤트를 agent runner 로 전달한다.

### 4. Agent Layer

- LangGraph 로 실행 단계를 정의한다.
- 기본 노드는 `plan -> execute_tools -> summarize -> persist_result` 흐름을 가진다.
- 실제 사용 가능한 tool 은 이벤트에 등록된 allowlist 로 제한한다.

### 5. Infra Layer

- 초기 MVP는 파일 저장 또는 SQLite 를 사용한다.
- 이후 Postgres, Redis, 외부 queue 로 확장 가능하게 추상화한다.

## 데이터 모델 초안

### Event

- `id`
- `title`
- `instruction`
- `schedule_type`
- `run_at`
- `time_of_day`
- `days_of_week`
- `timezone`
- `allowed_tools`
- `notify_target`
- `status`
- `created_at`
- `updated_at`
- `last_run_at`
- `next_run_at`

### Execution

- `id`
- `event_id`
- `status`
- `started_at`
- `finished_at`
- `summary`
- `steps`
- `tool_results`
- `error`

## API 초안

- `GET /health`
- `GET /api/tools`
- `GET /api/events`
- `POST /api/events`
- `PATCH /api/events/{event_id}`
- `DELETE /api/events/{event_id}`
- `POST /api/events/{event_id}/run`
- `POST /api/events/{event_id}/pause`
- `POST /api/events/{event_id}/resume`
- `GET /api/executions`

## Agent 실행 흐름

1. 스케줄러가 만기 이벤트를 조회한다.
2. 실행 레코드를 `running` 상태로 생성한다.
3. LangGraph runner 에 이벤트와 허용 tool 목록을 전달한다.
4. planner node 가 실행 계획을 만든다.
5. executor node 가 허용된 tool 만 호출한다.
6. summarizer node 가 결과를 사람이 읽기 쉬운 형태로 정리한다.
7. 실행 결과를 저장하고 상태를 `succeeded` 또는 `failed` 로 바꾼다.
8. 필요 시 알림 채널로 결과를 전달한다.

## 테스트 전략

### 단위 테스트

- schedule recurrence 계산
- event 상태 전이
- tool allowlist 필터링
- execution 상태 전이

### 통합 테스트

- 이벤트 생성 API
- 수동 실행 API
- 실행 결과 조회 API
- 스케줄 tick 시 due event 처리

### 회귀 테스트

- timezone 경계
- daily/weekly recurrence 계산
- 허용되지 않은 tool 차단
- 실패한 실행의 에러 저장

## 구현 우선순위

1. Domain 모델과 Pydantic schema 정의
2. Event/Execution repository
3. Event CRUD API
4. Scheduler tick 및 recurrence 계산
5. LangGraph runner 뼈대
6. Manual run API
7. Execution history API
8. Notification adapter
