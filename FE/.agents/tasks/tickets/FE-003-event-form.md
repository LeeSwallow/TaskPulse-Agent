# FE-003 Implement event form for create and edit

## Owner

- `fe-calendar-event-ux-engineer`

## Branch

- `feature/fe-event-form`

## Goal

이벤트 생성/수정 공용 폼을 구현한다.

## Scope

- `src/components/event-form/`
- `src/tests/event-form.test.jsx`

## TDD Steps

1. 필수 입력 검증 테스트 작성
2. schedule type 전환 테스트 작성
3. submit payload 테스트 작성
4. 최소 구현

## Acceptance Criteria

- `once/daily/weekly` 전환이 가능하다
- 허용 tool 선택이 가능하다
- create/edit 모드를 모두 지원한다

## Required Tests

- validation tests
- payload mapping tests
- edit mode initial state tests
