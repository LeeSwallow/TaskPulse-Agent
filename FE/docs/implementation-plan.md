# Frontend Implementation Plan

## 원칙

- `GitHub Flow` 를 따른다.
- UI 기능은 사용자 행동 기준으로 잘게 나눈다.
- 각 기능은 테스트와 함께 구현한다.

## 목표 구현 범위

프런트엔드 MVP는 아래를 실제로 제공해야 한다.

1. 캘린더에서 이벤트를 보고 날짜를 선택할 수 있다.
2. 이벤트를 생성/수정/삭제/일시정지/재개할 수 있다.
3. 최근 실행 결과를 조회하고 수동 실행할 수 있다.

## 구현 순서 상세

### Step 1. 앱 셸과 레이아웃

구현:

- `App` 를 `CalendarPage` 중심으로 단순화
- 캘린더, 이벤트 패널, 실행 피드 레이아웃
- API base URL 설정

테스트 파일:

- `src/tests/app.test.jsx`
- `src/tests/calendar-page.test.jsx`

## 단계별 구현 계획

### Phase 1. 앱 셸

- 기본 레이아웃
- 캘린더 페이지 라우팅 또는 단일 페이지 구조
- API base 설정

테스트:

- 루트 화면 렌더링
- 기본 레이아웃 표시

### Phase 2. Event Calendar

- 월간 캘린더 그리드
- 날짜 선택 상태
- 이벤트 목록 연동

구현 세부:

- 월 시작/종료 계산
- 날짜 셀별 이벤트 매핑
- 선택 날짜 하이라이트
- 선택 날짜 이벤트 목록 표시

테스트:

- 이벤트가 날짜 셀에 렌더링되는지 검증
- 날짜 클릭 시 상세 영역이 바뀌는지 검증
- 오늘 날짜 표시
- 빈 날짜 상태 표시

### Phase 3. Event Form

- create/edit 공용 폼
- 반복 규칙 입력
- 허용 tool 선택

구현 세부:

- `once/daily/weekly` 전환
- 주간 반복 요일 선택
- tool checkbox/select
- create/edit payload 변환

테스트:

- 필수 입력 검증
- submit payload 생성 검증
- 수정 모드 초기값 반영 검증
- schedule type 전환 시 필드 변화 검증

### Phase 4. Execution Feed

- 최근 실행 결과 리스트
- 상태와 요약 표시
- 상세 로그 토글

구현 세부:

- 상태 뱃지
- 실행 시간 포맷
- tool 결과 펼침
- 실패 에러 강조

테스트:

- 성공/실패 상태 렌더링
- 로그 확장/축소 동작
- 실행 시간 렌더링

### Phase 5. Event Actions

- 일시정지/재개
- 수동 실행
- 삭제

구현 세부:

- 선택 이벤트에 대한 action bar
- action 성공 후 목록과 피드 재조회
- optimistic update 없이 명시적 refresh 우선

테스트:

- 버튼 액션 호출
- 성공 후 화면 갱신
- 실패 시 오류 메시지 표시

## 초기 컴포넌트 우선순위

1. `CalendarPage`
2. `CalendarGrid`
3. `EventListByDate`
4. `EventForm`
5. `EventDetailPanel`
6. `ExecutionFeed`

## TDD 단위 분할 예시

### PR 1. `feature/fe-app-shell`

- 페이지 레이아웃 테스트
- 기본 화면 구현

### PR 2. `feature/fe-calendar-grid`

- 날짜 셀 렌더링 테스트
- 캘린더 컴포넌트 구현

### PR 3. `feature/fe-event-form`

- 폼 검증/submit 테스트
- create/edit form 구현

### PR 4. `feature/fe-execution-feed`

- 실행 목록 렌더링 테스트
- 실행 피드 구현

### PR 5. `feature/fe-event-actions`

- pause/resume/run/delete 테스트
- 상세 패널 action 구현

## 브랜치 예시

- `feature/fe-app-shell`
- `feature/fe-calendar-grid`
- `feature/fe-event-form`
- `feature/fe-execution-feed`
- `feature/fe-event-actions`

## PR 완료 체크리스트

- 사용자 스토리와 연결되는가
- 테스트가 먼저 작성되었는가
- 주요 UI 상태가 검증되었는가
- API 연동 또는 mock 이 문서화되었는가
- 리뷰 가능한 크기의 PR 인가
- 화면 상태 변화가 테스트로 재현되는가
