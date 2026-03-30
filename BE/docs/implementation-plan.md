# Backend Implementation Plan

## 원칙

- `GitHub Flow` 를 따른다.
- 기능 단위마다 테스트를 먼저 작성한다.
- 한 PR 에 하나의 기능만 포함한다.

## 목표 구현 범위

백엔드 MVP는 아래 세 가지를 실제로 제공해야 한다.

1. 이벤트 등록/조회/수정/삭제 API
2. 예약 시각 도달 시 agent 자동 실행
3. 실행 결과 저장 및 조회

기반 인프라:

- `PostgreSQL` for transactional data
- `pgvector` for embeddings and similarity retrieval
- `Redis` for lock, signal, cache, and future pub/sub

## 구현 순서 상세

### Step 1. 앱 진입점과 설정

구현:

- `create_app()` 팩토리
- `/health` endpoint
- `Settings` 기반 환경 변수 로딩
- CORS 및 기본 예외 처리
- layered architecture bootstrap
- PostgreSQL/Redis session manager bootstrap

테스트 파일:

- `tests/test_health.py`
- `tests/test_app_factory.py`

완료 기준:

- `uv run uvicorn be.app:app --reload` 로 서버가 뜬다.
- health check 테스트가 통과한다.

## 단계별 구현 계획

### Phase 1. 프로젝트 기반 정리

- FastAPI app entrypoint 정의
- 설정 모듈 정의
- 테스트 러너와 기본 테스트 구조 준비

완료 조건:

- 서버가 기동된다.
- health check 테스트가 통과한다.

### Phase 2. Event 모델과 CRUD

- Event schema 정의
- 저장소 인터페이스 정의
- 이벤트 생성/조회/수정/삭제 API 구현

구현 세부:

- `EventCreate`, `EventUpdate`, `ScheduledEvent`
- `ScheduleDefinition`
- SQLAlchemy repository
- `GET /api/events`
- `POST /api/events`
- `PATCH /api/events/{event_id}`
- `DELETE /api/events/{event_id}`

테스트:

- 이벤트 생성 성공/실패 케이스
- 필수 필드 검증
- 이벤트 수정/삭제
- 반복 규칙별 payload 검증
- 존재하지 않는 event id 처리

### Phase 3. Scheduler

- recurrence 계산 함수 구현
- due event 탐지 로직 구현
- paused 이벤트 제외 로직 구현

구현 세부:

- `compute_next_run(event)`
- `is_due(event, now)`
- poll loop
- 앱 시작/종료와 scheduler lifecycle 연결
- Redis 기반 duplicate lock 또는 signal channel 준비

테스트:

- once/daily/weekly next run 계산
- due event 만 실행 대상 포함
- paused 상태는 제외
- 서버 재시작 후 next run 복구

### Phase 4. Agent Runner

- LangGraph state 정의
- planner/executor/summarizer node 구현
- tool registry 및 allowlist 제어 구현

구현 세부:

- `AgentState`
- `plan -> execute_tools -> summarize`
- tool registry abstraction
- LLM 사용 가능/불가능 시 fallback path
- event.allowed_tools 기반 실행 제한

테스트:

- 허용 tool 만 실행되는지 검증
- 실행 결과가 summary 로 정리되는지 검증
- tool 실패가 execution 실패로 기록되는지 검증
- registry 에 없는 tool 차단
- empty tool list 에 대한 처리

### Phase 5. Execution History

- 실행 레코드 저장
- 실행 목록/상세 조회 API
- 수동 재실행 API

구현 세부:

- `ExecutionRecord`
- `GET /api/executions`
- `POST /api/events/{event_id}/run`
- event 와 execution 관계 조회
- execution summary embedding 저장 확장 지점 고려

테스트:

- 실행 생성 및 상태 업데이트
- 최근 실행 목록 정렬
- 수동 실행 성공/실패
- 실패 execution 의 error 저장
- tool 로그 직렬화

### Phase 6. Notification Adapter

- dashboard 알림 모델 정의
- Slack 등 외부 채널용 adapter interface 정의

구현 세부:

- `Notifier` protocol
- `DashboardNotifier`
- `SlackNotifier` placeholder

테스트:

- notify target 매핑
- 실패 시 fallback 동작

## 초기 API 우선순위

1. `GET /health`
2. `GET /api/tools`
3. `POST /api/events`
4. `GET /api/events`
5. `PATCH /api/events/{event_id}`
6. `DELETE /api/events/{event_id}`
7. `POST /api/events/{event_id}/run`
8. `GET /api/executions`

## TDD 단위 분할 예시

### PR 1. `feature/be-healthcheck`

- health endpoint 테스트
- app factory 구현

### PR 2. `feature/be-event-schema`

- schedule validation 테스트
- Event schema 구현

### PR 3. `feature/be-event-crud`

- event CRUD API 테스트
- repository + route 구현

### PR 4. `feature/be-scheduler-core`

- recurrence 테스트
- scheduler loop 구현

### PR 5. `feature/be-agent-runner`

- allowlist/summary 테스트
- LangGraph runner 구현

### PR 6. `feature/be-execution-history`

- manual run / execution list 테스트
- execution API 구현

## 브랜치 예시

- `feature/be-healthcheck`
- `feature/be-event-crud`
- `feature/be-scheduler-core`
- `feature/be-agent-runner`
- `feature/be-execution-history`

## PR 완료 체크리스트

- 관련 요구사항 문서 확인
- 테스트 먼저 작성
- 구현 후 테스트 통과
- 관련 문서 갱신
- 머지 가능한 단일 목적 PR 상태 확인
- API 스펙 변경 시 문서 반영
