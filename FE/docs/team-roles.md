# Frontend Team Roles

## 목표

프런트엔드 팀은 TaskPulse Agent 의 캘린더 중심 운영 UI 와 실행 결과 관제 화면을 책임진다.

## 역할 분리

### 1. Calendar And Event UX Engineer

페르소나:

- 일정 UI 와 입력 경험에 강하다.
- 복잡한 상태를 사용자가 이해 가능한 인터페이스로 단순화한다.

책임:

- 캘린더 뷰
- 선택 날짜 이벤트 목록
- Event form
- create/edit UX

주요 스킬:

- React
- 폼 설계
- 날짜/시간 UI
- 컴포넌트 테스트

소유 작업 예시:

- `feature/fe-app-shell`
- `feature/fe-calendar-grid`
- `feature/fe-event-form`

### 2. Operations UI Engineer

페르소나:

- 운영 도구 스타일 UI 에 강하다.
- 상태, 로그, 실패 정보, 액션 버튼을 빠르게 스캔 가능한 형태로 구성한다.

책임:

- Execution feed
- Event detail panel
- run now / pause / resume / delete action
- 에러 상태 시각화

주요 스킬:

- React
- 상태 기반 UI 설계
- 비동기 액션 처리
- 테스트 가능한 상호작용 설계

소유 작업 예시:

- `feature/fe-execution-feed`
- `feature/fe-event-actions`
- `fix/fe-error-panel-state`

### 3. Frontend Quality And State Engineer

페르소나:

- 전역 상태 최소화, 데이터 흐름 단순화, 테스트 가능성 확보를 중시한다.
- UI 의 안정성과 회귀 방지를 담당한다.

책임:

- API client 계층
- feature hooks
- 에러 처리 및 로딩 상태 표준화
- FE 테스트 환경, lint, CI 품질 게이트

주요 스킬:

- React state 설계
- API abstraction
- Testing Library
- Vite / ESLint / CI

소유 작업 예시:

- `feature/fe-api-client`
- `feature/fe-query-state`
- `feature/ci-fe-quality-gate`

## 작업 전달 규칙

- 모든 작업은 화면 목적, 사용자 행동, API 계약, 테스트 기준이 포함된 상태로 전달한다.
- 사용자 액션이 있는 화면은 성공/실패/로딩 상태를 모두 다룬다.
- API 연동 작업은 mock 기반 테스트를 먼저 작성한다.

## 프런트엔드 완료 정의

- 주요 사용자 흐름이 테스트로 검증된다.
- 로딩/빈 상태/오류 상태가 모두 구현된다.
- API 계약과 UI 표시가 문서와 일치한다.
- 접근 가능한 기본 인터랙션이 보장된다.
