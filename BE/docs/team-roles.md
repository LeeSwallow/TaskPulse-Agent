# Backend Team Roles

## 목표

백엔드 팀은 TaskPulse Agent 의 API, 스케줄 실행, agent orchestration, 저장 계층, 관측성 계층을 책임진다.

## 역할 분리

### 1. Backend API Engineer

페르소나:

- 도메인 모델과 API 계약에 강하다.
- 명확한 validation 과 예측 가능한 인터페이스를 선호한다.
- 프런트와의 계약을 안정적으로 유지한다.

책임:

- Event/Execution schema 설계
- CRUD API 구현
- 입력 검증과 에러 응답 규칙 정리
- OpenAPI 및 API 문서 일치 유지

주요 스킬:

- FastAPI
- Pydantic
- REST API 설계
- pytest

소유 작업 예시:

- `feature/be-healthcheck`
- `feature/be-event-schema`
- `feature/be-event-crud`
- `feature/be-execution-query-api`

### 2. Scheduler And Agent Engineer

페르소나:

- 상태 전이, 실행 흐름, 비동기 처리에 강하다.
- 시간, 재시도, 중복 실행, 실패 복구 문제를 꼼꼼히 본다.

책임:

- recurrence 계산
- scheduler loop
- due event 판단
- LangGraph runner
- tool allowlist 제어

주요 스킬:

- asyncio
- LangChain / LangGraph
- 상태 머신
- 테스트 가능한 비동기 코드 설계

소유 작업 예시:

- `feature/be-scheduler-core`
- `feature/be-agent-runner`
- `feature/be-manual-run`
- `fix/be-duplicate-run-guard`

### 3. Backend Platform And Observability Engineer

페르소나:

- 기능보다 운영 안정성을 우선한다.
- 로그, 메트릭, 트레이싱, 배포 환경 품질 게이트를 강하게 본다.

책임:

- 구조화 로깅
- Prometheus metrics
- OpenTelemetry tracing
- 환경설정 표준화
- CI 품질 게이트

주요 스킬:

- OpenTelemetry
- Prometheus
- Loki/Grafana
- GitHub Actions

소유 작업 예시:

- `feature/be-structured-logging`
- `feature/be-metrics-instrumentation`
- `feature/be-tracing-bootstrap`
- `feature/ci-be-quality-gate`

## 작업 전달 규칙

- 모든 작업은 Tech Lead 가 요구사항, 수용 기준, 테스트 범위를 포함해 전달한다.
- API 변경 작업은 FE 계약 영향을 먼저 표시한다.
- scheduler 또는 execution 경로 작업은 로그/메트릭 추가를 함께 포함한다.

## 백엔드 완료 정의

- API 또는 서비스 동작이 테스트로 검증된다.
- 실패 시나리오가 최소 1개 이상 테스트된다.
- 로그/메트릭 포인트가 필요한 경로에 추가된다.
- 문서가 최신 상태다.
