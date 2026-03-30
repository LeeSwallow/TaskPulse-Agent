# FE-006 Implement event actions and UI quality gate

## Owner

- `fe-operations-ui-engineer`

## Branch

- `feature/fe-event-actions`

## Goal

이벤트 실행/일시정지/재개/삭제 액션과 관련 UI 상태를 구현한다.

## Scope

- detail action bar
- action-driven refresh
- FE quality regression tests

## TDD Steps

1. 액션 버튼 테스트 작성
2. 성공 후 갱신 테스트 작성
3. 실패 메시지 테스트 작성
4. 최소 구현

## Acceptance Criteria

- run now, pause, resume, delete 액션이 동작한다
- 액션 후 관련 목록이 갱신된다
- 실패 시 사용자에게 오류 상태가 보인다

## Required Tests

- action interaction tests
- success refresh tests
- error rendering tests
