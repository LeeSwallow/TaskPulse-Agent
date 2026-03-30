# BE-003 Implement event CRUD application and repository core

## Owner

- `be-api-engineer`

## Branch

- `feature/be-event-crud`

## Goal

이벤트 생성, 조회, 수정, 삭제를 위한 application service 와 repository core 를 구현한다.

## Scope

- `src/be/application/services/event_service.py`
- `src/be/infra/repositories/event_repository.py`
- `tests/api/test_events_api.py`

## TDD Steps

1. create/list/update/delete API 테스트 작성
2. not found / invalid payload 테스트 작성
3. repository 와 service 최소 구현
4. 테스트 통과 후 리팩터링

## Acceptance Criteria

- create/list/update/delete core 가 동작한다
- 이후 gRPC service 에서 재사용 가능해야 한다
- 오류 응답으로 매핑 가능한 domain/application 결과를 반환한다

## Required Tests

- CRUD API happy path
- 404 path
- validation error path
