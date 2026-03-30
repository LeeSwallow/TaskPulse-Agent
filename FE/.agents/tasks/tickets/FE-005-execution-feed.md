# FE-005 Implement execution feed and event detail panel

## Owner

- `fe-operations-ui-engineer`

## Branch

- `feature/fe-execution-feed`

## Goal

실행 결과 피드와 이벤트 상세 패널을 구현한다.

## Scope

- `src/components/execution/`
- `src/components/event-detail/`
- `src/tests/execution-feed.test.jsx`

## TDD Steps

1. 상태 badge 테스트 작성
2. 로그 펼침 테스트 작성
3. detail panel 렌더링 테스트 작성
4. 최소 구현

## Acceptance Criteria

- 성공/실패 상태가 구분된다
- 요약과 로그를 볼 수 있다
- 선택 이벤트의 상세 설정이 표시된다

## Required Tests

- execution list tests
- status badge tests
- detail panel tests
