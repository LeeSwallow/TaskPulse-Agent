# BE-007 Add structured logging and metrics

## Owner

- `be-platform-observability-engineer`

## Branch

- `feature/be-structured-logging`

## Goal

백엔드 실행 경로에 구조화 로깅과 메트릭 계측을 추가한다.

## Scope

- logging config
- scheduler/execution metrics
- gRPC request metrics
- tests for logging/metrics bootstrap
- CI 품질 게이트 초안

## TDD Steps

1. logging config 테스트 작성
2. metrics registry 테스트 작성
3. bootstrap 구현
4. scheduler/execution/grpc path 연결

## Acceptance Criteria

- 로그가 JSON structured format 으로 출력된다
- execution, scheduler, grpc 관련 메트릭이 노출된다
- correlation field 기준이 문서와 일치한다

## Required Tests

- logging config tests
- metrics registration tests
- instrumentation smoke test
