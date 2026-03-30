# Frontend Architecture

## 목표

프런트엔드는 `TaskPulse Agent` 의 데스크톱 운영 UI 를 제공한다. 사용자는 이벤트를 캘린더 기반으로 등록하고, 상태와 실행 결과를 확인하며, 수동 실행과 제어를 수행할 수 있어야 한다.

기술 스택:

- `React`
- `Vite`
- `Electron`
- `gRPC client` in Electron main process

## 프로세스 구조

### Renderer

- React UI
- 캘린더, 이벤트, 실행 결과 렌더링
- preload API 만 사용

### Preload

- renderer 와 main process 사이의 안전한 브리지
- typed IPC surface 제공

### Main Process

- gRPC backend client 소유
- backend 와의 통신 담당
- desktop notification, local config, window lifecycle 담당

## 핵심 화면

### 1. Calendar Page

- workspace / agent selector
- 월간 또는 주간 이벤트 조회
- 날짜 클릭 시 해당 날짜 이벤트 리스트 표시
- 이벤트 상태 배지 표시
- 오늘 날짜, 선택 날짜, 예정 실행 수 표시

### 2. Event Composer

- 제목 입력
- 자연어 instruction 입력
- 실행 시각/반복 규칙 입력
- 허용 tool 선택
- notify target 선택
- 생성/수정 공용 모드

### 3. Execution Feed

- 최근 실행 결과 목록
- 성공/실패 상태
- 요약 결과
- 사용 tool 로그
- 실행 시간 표시

### 4. Event Detail Panel

- 이벤트 전체 설정 조회
- 일시정지/재개/수정/삭제/수동 실행

## 사용자 계층

- user 가 workspace 를 가진다
- workspace 가 agent 를 가진다
- agent 가 event 와 execution 을 가진다
- UI 는 항상 현재 선택된 workspace 와 agent 컨텍스트 안에서 동작한다

## 적용할 디렉터리 구조

```text
FE/
  electron/
    main/
      main.ts
      grpc-client.ts
    preload/
      preload.ts
  src/
    app/
    pages/
      CalendarPage.jsx
    components/
      calendar/
      event-form/
      execution/
      event-detail/
    features/
      workspaces/
      agents/
      events/
      executions/
      tools/
    lib/
      ipc/
      contracts/
      date/
      constants/
    tests/
```

## 상태 관리 방향

- 초기 MVP는 React 내장 상태와 feature 단위 custom hook 으로 시작한다.
- renderer 는 Electron preload API 를 통해 main process 와 통신한다.
- main process 가 gRPC backend client 를 소유한다.
- 전역 상태는 최소화한다.

## 상태 초안

- `currentMonth: Date`
- `selectedDate: Date`
- `workspaces: Workspace[]`
- `agents: Agent[]`
- `selectedWorkspaceId: string | null`
- `selectedAgentId: string | null`
- `events: Event[]`
- `executions: Execution[]`
- `tools: ToolDefinition[]`
- `selectedEventId: string | null`
- `formMode: "create" | "edit"`
- `loading/error` 상태

## 통신 초안

- renderer -> preload/ipc
- preload -> Electron main process
- Electron main -> backend gRPC

직접 HTTP fetch 를 기본 통신 계층으로 사용하지 않는다.

## FE 타입 계약 초안

```ts
type Workspace = {
  id: string;
  user_id: string;
  name: string;
  timezone: string;
};

type Agent = {
  id: string;
  workspace_id: string;
  name: string;
  description: string;
  status: "active" | "paused";
};

type Event = {
  id: string;
  agent_id: string;
  title: string;
  instruction: string;
  schedule: {
    type: "once" | "daily" | "weekly";
    run_at?: string | null;
    time_of_day?: string | null;
    days_of_week: number[];
    timezone: string;
  };
  allowed_tools: string[];
  notify_target: string;
  status: "active" | "paused";
  last_run_at?: string | null;
  next_run_at?: string | null;
};

type Execution = {
  id: string;
  workspace_id: string;
  agent_id: string;
  event_id: string;
  status: "pending" | "running" | "succeeded" | "failed";
  started_at: string;
  finished_at?: string | null;
  summary?: string;
  steps: string[];
  tool_results: Array<Record<string, unknown>>;
  error?: string | null;
};
```

## 테스트 전략

### 컴포넌트 테스트

- Calendar Grid 렌더링
- Event Form 입력/검증
- Execution List 상태 렌더링
- Event Detail Panel 액션 표시
- workspace / agent selector 동작

### 통합 테스트

- 이벤트 생성 플로우
- 이벤트 수정/일시정지 플로우
- 수동 실행 버튼 동작
- 초기 workspace/agent/event fetch 및 렌더링

### 회귀 테스트

- preload contract test
- ipc to grpc mapping test
- workspace/agent selection regression test
- 반복 규칙 폼 전환
- API 실패 시 에러 표시
