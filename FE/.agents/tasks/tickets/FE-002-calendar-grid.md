# FE-002 Implement calendar grid and selected date interaction

## Owner

- `fe-calendar-event-ux-engineer`

## Branch

- `feature/fe-calendar-grid`

## Goal

월간 캘린더 그리드와 날짜 선택 상호작용을 구현한다.

## Scope

- `src/components/calendar/`
- `src/lib/date/calendar.js`
- `src/tests/calendar-grid.test.jsx`

## TDD Steps

1. 날짜 셀 렌더링 테스트 작성
2. 오늘 날짜/선택 날짜 테스트 작성
3. 클릭 상호작용 테스트 작성
4. 최소 구현

## Acceptance Criteria

- 월간 그리드가 렌더링된다
- 날짜 선택 시 우측 패널 기준 날짜가 바뀐다
- 이벤트가 날짜 셀에 매핑된다

## Required Tests

- grid rendering tests
- selected date interaction tests
- empty date state tests
