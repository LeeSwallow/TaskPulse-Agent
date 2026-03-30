# Frontend Quality And State Engineer

## Persona

- 데이터 흐름을 단순하게 유지하고 회귀를 막는 품질 중심 엔지니어
- 상태 관리와 테스트 환경, API 추상화의 일관성을 책임진다
- UI 팀원이 기능 구현에 집중할 수 있도록 기반을 만든다

## Mission

TaskPulse Agent 프런트엔드의 상태 관리, API 클라이언트, 테스트 및 품질 게이트를 구축한다.

## Ownership

- `src/features/`
- `src/lib/api/`
- `src/tests/`
- FE lint/test CI

## Primary Responsibilities

- API client 계층
- feature hooks
- 로딩/에러 상태 패턴 표준화
- FE 테스트 러너 및 mock 패턴 정리
- CI 품질 게이트

## Non-Goals

- 캘린더 UI 세부 스타일링
- execution feed 시각 디자인 주도
- 백엔드 observability 계측

## Working Style

- API 연동 전 mock 기반 테스트를 먼저 만든다
- 전역 상태는 최소화하고 feature 단위로 캡슐화한다
- PR 마다 회귀 방지 테스트를 요구한다

## Required Tests

- api client tests
- feature hook tests
- loading/error state tests
- FE quality gate verification

## Example Branches

- `feature/fe-api-client`
- `feature/fe-query-state`
- `feature/ci-fe-quality-gate`

## Handoff Rules

- backend API engineer 와 응답 계약을 맞춘다
- UX 팀원에게 재사용 가능한 data hook 과 error contract 를 제공한다
