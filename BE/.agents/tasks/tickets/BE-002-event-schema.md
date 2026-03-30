# BE-002 Define event and schedule schemas

## Owner

- `be-api-engineer`

## Branch

- `feature/be-event-schema`

## Goal

이벤트, 스케줄, 실행 레코드의 Pydantic schema 를 정의한다.

## Scope

- `src/be/domain/models/`
- `tests/domain/`

## TDD Steps

1. `once/daily/weekly` validation 테스트 작성
2. invalid payload 테스트 작성
3. schema 구현
4. 테스트 통과 확인

## Acceptance Criteria

- `once` 에는 `run_at` 이 필수다
- `daily`, `weekly` 에는 `time_of_day` 가 필요하다
- `weekly` 는 `days_of_week` 를 1개 이상 가져야 한다
- `allowed_tools`, `notify_target`, `status` 필드가 정의된다

## Required Tests

- schedule validation tests
- event schema serialization test
- execution record schema test
