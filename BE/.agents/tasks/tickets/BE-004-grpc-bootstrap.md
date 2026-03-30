# BE-004 Implement gRPC contract and server bootstrap

## Owner

- `be-api-engineer`

## Branch

- `feature/be-grpc-bootstrap`

## Goal

데스크톱 앱과 통신할 gRPC contract 와 server bootstrap 을 구현한다.

## Scope

- `proto/taskpulse/v1/taskpulse.proto`
- `src/be/presentation/grpc/`
- gRPC server bootstrap
- proto generation flow

## TDD Steps

1. gRPC bootstrap smoke test 작성
2. health gRPC contract test 작성
3. server 최소 구현
4. 테스트 통과 확인

## Acceptance Criteria

- backend 가 gRPC server 를 기동할 수 있다
- health service 가 gRPC 로 응답한다
- proto contract 가 버전 경로 아래 관리된다

## Required Tests

- grpc server bootstrap test
- grpc health service test
