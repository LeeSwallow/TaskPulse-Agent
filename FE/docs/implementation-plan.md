# Frontend Implementation Plan

## 원칙

- `GitHub Flow` 를 따른다.
- UI 기능은 사용자 행동 기준으로 잘게 나눈다.
- 각 기능은 테스트와 함께 구현한다.

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

테스트:

- 이벤트가 날짜 셀에 렌더링되는지 검증
- 날짜 클릭 시 상세 영역이 바뀌는지 검증

### Phase 3. Event Form

- create/edit 공용 폼
- 반복 규칙 입력
- 허용 tool 선택

테스트:

- 필수 입력 검증
- submit payload 생성 검증
- 수정 모드 초기값 반영 검증

### Phase 4. Execution Feed

- 최근 실행 결과 리스트
- 상태와 요약 표시
- 상세 로그 토글

테스트:

- 성공/실패 상태 렌더링
- 로그 확장/축소 동작

### Phase 5. Event Actions

- 일시정지/재개
- 수동 실행
- 삭제

테스트:

- 버튼 액션 호출
- 성공 후 화면 갱신
- 실패 시 오류 메시지 표시

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
