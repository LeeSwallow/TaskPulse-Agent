# Requirements

## 1. 기능 요구사항

### FR-1 이벤트 등록

- 사용자는 이벤트 제목을 입력할 수 있어야 한다.
- 사용자는 자연어 instruction을 입력할 수 있어야 한다.
- 사용자는 실행 시각 또는 반복 규칙을 설정할 수 있어야 한다.
- 사용자는 이벤트별 허용 tool/MCP 목록을 선택할 수 있어야 한다.
- 사용자는 결과 통지 대상을 선택할 수 있어야 한다.

### FR-2 캘린더 조회

- 사용자는 월/주 기준으로 등록된 이벤트를 볼 수 있어야 한다.
- 사용자는 특정 날짜의 이벤트 상세를 확인할 수 있어야 한다.
- 사용자는 이벤트 상태(active, paused)를 확인할 수 있어야 한다.

### FR-3 이벤트 관리

- 사용자는 이벤트를 수정할 수 있어야 한다.
- 사용자는 이벤트를 일시정지/재개할 수 있어야 한다.
- 사용자는 이벤트를 삭제할 수 있어야 한다.
- 사용자는 이벤트를 즉시 수동 실행할 수 있어야 한다.

### FR-4 스케줄 실행

- 시스템은 예약된 시각이 되면 이벤트를 자동 실행해야 한다.
- 시스템은 반복 이벤트의 다음 실행 시각을 계산해야 한다.
- 서버 재시작 이후에도 저장된 이벤트 기준으로 스케줄을 복구해야 한다.

### FR-5 Agent 실행 제어

- 시스템은 이벤트별 허용 tool/MCP만 agent에 제공해야 한다.
- 시스템은 실행 instruction, 이벤트 메타데이터, 허용 tool 목록을 agent context로 전달해야 한다.
- 시스템은 LangGraph 기반으로 실행 흐름을 구성해야 한다.

### FR-6 결과 기록

- 시스템은 각 실행에 대해 상태를 저장해야 한다.
- 시스템은 시작 시각, 종료 시각, 결과 요약, tool 사용 로그를 저장해야 한다.
- 실패 시 오류 메시지를 저장해야 한다.

### FR-7 결과 조회 및 알림

- 사용자는 최근 실행 결과 목록을 조회할 수 있어야 한다.
- 사용자는 특정 이벤트의 실행 이력을 조회할 수 있어야 한다.
- 시스템은 결과를 지정된 채널로 전달할 수 있어야 한다.

## 2. 비기능 요구사항

### NFR-1 안정성

- 예약된 작업은 서버 시간 기준으로 누락 없이 감지되어야 한다.
- 동일 이벤트가 중복 실행되지 않도록 보호 장치가 필요하다.

### NFR-2 관찰 가능성

- 실행 로그와 상태 전이를 추적할 수 있어야 한다.
- 최소한 이벤트 단위/실행 단위의 구조화 로그가 필요하다.

### NFR-3 확장성

- tool/MCP provider를 플러그인처럼 추가 가능해야 한다.
- 향후 다중 사용자 지원이 가능하도록 모델이 확장 가능해야 한다.

### NFR-4 보안

- 허용되지 않은 tool 호출은 차단되어야 한다.
- 외부 API 키는 환경 변수로 관리해야 한다.
- 민감한 실행 결과는 저장 정책을 명확히 해야 한다.

### NFR-5 개발 생산성

- 백엔드는 `uv` 기반으로 재현 가능하게 세팅되어야 한다.
- 프런트엔드는 `npm` 기반으로 독립 실행 가능해야 한다.

## 3. 데이터 요구사항

### Event

- `id`
- `title`
- `instruction`
- `schedule_type`
- `run_at` 또는 `recurrence_rule`
- `timezone`
- `allowed_tools`
- `notify_target`
- `status`
- `created_at`
- `updated_at`
- `last_run_at`
- `next_run_at`

### Execution

- `id`
- `event_id`
- `status`
- `started_at`
- `finished_at`
- `summary`
- `tool_results`
- `error`

## 4. API 초안

- `GET /api/events`
- `POST /api/events`
- `PATCH /api/events/{event_id}`
- `DELETE /api/events/{event_id}`
- `POST /api/events/{event_id}/run`
- `POST /api/events/{event_id}/pause`
- `POST /api/events/{event_id}/resume`
- `GET /api/executions`
- `GET /api/tools`

## 5. 범위 경계

- MVP는 단일 워크스페이스/단일 사용자 기준으로 정의한다.
- MVP는 "실행 가능한 자동화 프레임"을 목표로 하며, 고도화된 planner 품질은 후순위다.
