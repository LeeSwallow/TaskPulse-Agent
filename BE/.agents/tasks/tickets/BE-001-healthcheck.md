# BE-001 Bootstrap FastAPI app and healthcheck

## Owner

- `be-api-engineer`

## Branch

- `feature/be-healthcheck`

## Goal

FastAPI 앱 팩토리와 기본 `/health` endpoint 를 만든다.

## Scope

- `src/be/app.py`
- `src/be/config.py`
- `tests/test_health.py`
- `tests/test_app_factory.py`

## TDD Steps

1. app factory 테스트 작성
2. `/health` 응답 테스트 작성
3. 최소 구현 작성
4. 테스트 통과 확인

## Acceptance Criteria

- `create_app()` 가 FastAPI app 을 생성한다
- `GET /health` 가 `200` 과 `{"status":"ok"}` 를 반환한다
- 앱이 로컬에서 기동 가능하다

## Required Tests

- health endpoint test
- app factory smoke test

## Definition Of Done

- 테스트 통과
- README 또는 관련 문서 반영
- PR 설명에 실행 명령 포함
