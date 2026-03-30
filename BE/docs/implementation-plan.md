# Backend Implementation Plan

## 원칙

- `GitHub Flow` 를 따른다.
- 기능 단위마다 테스트를 먼저 작성한다.
- 한 PR 에 하나의 기능만 포함한다.

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

테스트:

- 이벤트 생성 성공/실패 케이스
- 필수 필드 검증
- 이벤트 수정/삭제

### Phase 3. Scheduler

- recurrence 계산 함수 구현
- due event 탐지 로직 구현
- paused 이벤트 제외 로직 구현

테스트:

- once/daily/weekly next run 계산
- due event 만 실행 대상 포함
- paused 상태는 제외

### Phase 4. Agent Runner

- LangGraph state 정의
- planner/executor/summarizer node 구현
- tool registry 및 allowlist 제어 구현

테스트:

- 허용 tool 만 실행되는지 검증
- 실행 결과가 summary 로 정리되는지 검증
- tool 실패가 execution 실패로 기록되는지 검증

### Phase 5. Execution History

- 실행 레코드 저장
- 실행 목록/상세 조회 API
- 수동 재실행 API

테스트:

- 실행 생성 및 상태 업데이트
- 최근 실행 목록 정렬
- 수동 실행 성공/실패

### Phase 6. Notification Adapter

- dashboard 알림 모델 정의
- Slack 등 외부 채널용 adapter interface 정의

테스트:

- notify target 매핑
- 실패 시 fallback 동작

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
