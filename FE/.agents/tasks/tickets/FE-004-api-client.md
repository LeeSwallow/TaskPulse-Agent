# FE-004 Add preload/ipc bridge and grpc client mapping

## Owner

- `fe-quality-state-engineer`

## Branch

- `feature/fe-api-client`

## Goal

renderer-preload-main-backend 경로의 통신 브리지를 구현한다.

## Scope

- `electron/main/grpc-client.ts`
- `electron/preload/preload.ts`
- `src/lib/ipc/`
- `src/features/events/`
- `src/features/executions/`
- `src/tests/`

## TDD Steps

1. preload/ipc contract 테스트 작성
2. grpc mapping 테스트 작성
3. mock 기반 최소 구현
4. 테스트 통과 확인

## Acceptance Criteria

- renderer 에 안전한 preload API 가 노출된다
- main process 가 gRPC backend 와 통신할 수 있다
- loading/error 상태 표준이 제공된다

## Required Tests

- preload contract tests
- ipc to grpc mapping tests
- feature hook tests
- loading/error state tests
