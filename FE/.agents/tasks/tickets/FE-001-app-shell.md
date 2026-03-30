# FE-001 Build Electron app shell and calendar page layout

## Owner

- `fe-calendar-event-ux-engineer`

## Branch

- `feature/fe-app-shell`

## Goal

Electron 기반 앱 셸과 캘린더 페이지 중심의 기본 레이아웃을 만든다.

## Scope

- `electron/main/`
- `electron/preload/`
- `src/App.jsx`
- `src/pages/CalendarPage.jsx`
- `src/tests/app.test.jsx`

## TDD Steps

1. 루트 레이아웃 테스트 작성
2. 핵심 영역 렌더링 테스트 작성
3. 최소 레이아웃 구현
4. 테스트 통과 확인

## Acceptance Criteria

- Electron shell 이 준비된다
- 헤더, 캘린더 영역, 우측 패널 영역이 렌더링된다
- 페이지가 단일 진입점으로 동작한다

## Required Tests

- app render test
- layout region test
