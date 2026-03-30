# Desktop Architecture

## 목표

TaskPulse Agent 는 웹 앱이 아니라 데스크톱 앱을 목표로 한다. 프런트엔드는 React renderer 를 사용하되, 백엔드와 직접 HTTP 로 연결하지 않고 Electron main process 를 통해 gRPC 로 통신한다.

## 프로세스 구조

### Renderer

- React UI
- 캘린더, 이벤트, 실행 결과 렌더링
- preload API 만 사용

### Preload

- 안전한 브리지 계층
- renderer 에 노출할 최소 API 정의

### Main Process

- gRPC client 보유
- backend 와의 통신 담당
- desktop notification, local config, window lifecycle 담당

### Backend Service

- Python gRPC server
- scheduler, agent orchestration, persistence 담당

## 데이터 계층

- `User`
- `Workspace`
- `Agent`
- `Event`
- `Execution`

모든 UI 조회와 쓰기 작업은 최소 `workspace_id`, `agent_id` 컨텍스트를 가져야 한다.

## 권장 기술 방향

- FE shell: `Electron`
- UI: `React`
- transport: `gRPC`
- backend: `Python + gRPC + PostgreSQL + Redis`

## HTTP 사용 범위

- `/health`
- `/metrics`
- internal diagnostics only

주 기능은 HTTP 가 아니라 gRPC 로 노출한다.
