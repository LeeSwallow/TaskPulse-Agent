# BE-005 Implement scheduler recurrence core

## Owner

- `be-scheduler-agent-engineer`

## Branch

- `feature/be-scheduler-core`

## Goal

다음 실행 시각 계산과 due event 판정 로직을 구현한다.

## Scope

- `src/be/scheduler/recurrence.py`
- `src/be/scheduler/engine.py`
- `tests/scheduler/`

## TDD Steps

1. recurrence unit tests 작성
2. due 판정 테스트 작성
3. scheduler 순수 함수 구현
4. 테스트 통과 후 lifecycle 연결

## Acceptance Criteria

- `once/daily/weekly` 의 next run 계산이 정확하다
- `paused` 이벤트는 제외된다
- due event 만 실행 후보가 된다
- Redis lock 확장 지점을 고려한다

## Required Tests

- recurrence boundary tests
- timezone tests
- paused exclusion tests
