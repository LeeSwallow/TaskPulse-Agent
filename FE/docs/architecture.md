# Frontend Architecture

## 목표

프런트엔드는 사용자가 이벤트를 캘린더 기반으로 등록하고, 상태와 실행 결과를 확인하며, 수동 실행과 제어를 수행할 수 있는 운영 UI 를 제공한다.

기술 스택:

- `React`
- `Vite`

## 핵심 화면

### 1. Calendar Page

- 월간 또는 주간 이벤트 조회
- 날짜 클릭 시 해당 날짜 이벤트 리스트 표시
- 이벤트 상태 배지 표시

### 2. Event Composer

- 제목 입력
- 자연어 instruction 입력
- 실행 시각/반복 규칙 입력
- 허용 tool 선택
- notify target 선택

### 3. Execution Feed

- 최근 실행 결과 목록
- 성공/실패 상태
- 요약 결과
- 사용 tool 로그

### 4. Event Detail Drawer or Panel

- 이벤트 전체 설정 조회
- 일시정지/재개/수정/삭제/수동 실행

## 제안 디렉터리 구조

```text
FE/
  src/
    app/
    pages/
      CalendarPage.jsx
    components/
      calendar/
      event-form/
      execution/
      layout/
    features/
      events/
      executions/
      tools/
    lib/
      api/
      date/
      constants/
    styles/
    tests/
```

## 상태 관리 방향

- 초기 MVP는 React 내장 상태와 feature 단위 custom hook 으로 시작한다.
- 데이터 fetching 은 경량 wrapper 로 직접 구현하거나 이후 TanStack Query 도입을 검토한다.
- 전역 상태는 최소화한다.

## 주요 컴포넌트 초안

### Calendar Grid

- 월별 날짜 셀 렌더링
- 날짜별 이벤트 개수와 제목 일부 노출
- 선택 날짜 강조

### Event Form

- create/edit 모드 공용
- 반복 규칙 타입에 따라 필드가 동적으로 바뀜
- 허용 tool 멀티 선택 지원

### Execution List

- 최신순 정렬
- 상태 색상 표시
- 요약과 로그 펼침 지원

## API 연동 초안

- `GET /api/events`
- `POST /api/events`
- `PATCH /api/events/{event_id}`
- `DELETE /api/events/{event_id}`
- `POST /api/events/{event_id}/run`
- `POST /api/events/{event_id}/pause`
- `POST /api/events/{event_id}/resume`
- `GET /api/executions`
- `GET /api/tools`

## UX 원칙

- 일정 정보는 한눈에 보여야 한다.
- 등록 폼은 복잡하더라도 단계별로 이해 가능해야 한다.
- 실행 결과는 운영 도구처럼 빠르게 스캔 가능해야 한다.
- 실패 실행은 즉시 재실행 가능해야 한다.

## 테스트 전략

### 컴포넌트 테스트

- Calendar Grid 렌더링
- Event Form 입력/검증
- Execution List 상태 렌더링

### 통합 테스트

- 이벤트 생성 플로우
- 이벤트 수정/일시정지 플로우
- 수동 실행 버튼 동작

### 회귀 테스트

- 반복 규칙 폼 전환
- API 실패 시 에러 표시
- 날짜 선택 변경 시 상세 패널 동기화

## 구현 우선순위

1. 레이아웃과 기본 페이지 셸
2. 이벤트 목록/캘린더 렌더링
3. 이벤트 등록 폼
4. 실행 결과 피드
5. 이벤트 상세 제어 액션
6. 에러/로딩 상태 정리
