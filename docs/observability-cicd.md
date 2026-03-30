# Observability And CI/CD Strategy

## 1. 목표

TaskPulse Agent 는 Grafana 계열 관측성 시스템을 활용해 안정적으로 운영 가능한 서비스 구조를 목표로 한다.

핵심 목표:

- 장애를 빨리 감지한다.
- 실패 원인을 추적할 수 있다.
- 배포 전후 품질 상태를 자동 검증한다.
- 예약 실행 시스템의 특성상 "실행 누락", "중복 실행", "실행 지연" 을 명확히 관찰한다.

## 2. 관측성 스택

권장 스택:

- `Grafana`: 대시보드 및 알림 관리
- `Prometheus`: 메트릭 수집
- `Loki`: 애플리케이션 로그 수집
- `Tempo`: 분산 트레이싱
- `OpenTelemetry`: 애플리케이션 계측 표준

## 3. 수집해야 할 신호

### Metrics

- HTTP 요청 수, 지연 시간, 오류율
- 이벤트 등록 수
- 이벤트 실행 수
- 이벤트 실행 성공률/실패율
- 예약 시간 대비 실제 실행 지연
- 스케줄러 poll 주기 정상 여부
- tool 호출 수와 실패율
- notification 성공률/실패율

### Logs

- 이벤트 생성/수정/삭제 로그
- 스케줄러 tick 로그
- due event 판단 로그
- execution 시작/종료 로그
- tool 실행 로그
- 예외와 stack trace

### Traces

- manual run 요청에서 execution 완료까지
- scheduled run 트리거에서 tool 실행, 결과 저장까지
- notification adapter 실행 구간

## 4. 대시보드 초안

### 서비스 상태 대시보드

- API latency
- API error rate
- health status

### Scheduler 대시보드

- due event count
- execution lag
- missed run count
- duplicate run guard count

### Agent 대시보드

- tool invocation rate
- tool failure rate
- average execution duration
- execution success/failure ratio

### Notification 대시보드

- notify target 별 성공률
- retry 횟수

## 5. 알림 정책

- health check 실패
- API 오류율 임계치 초과
- execution failure 급증
- scheduler lag 임계치 초과
- missed run 감지
- notification failure 연속 발생

## 6. 로깅 원칙

- 구조화 로그(JSON) 사용
- 모든 로그에 `event_id`, `execution_id`, `status`, `tool_name` 같은 correlation field 포함
- 개인정보나 민감정보는 마스킹
- 로그 레벨 기준 명확화

권장 로그 레벨:

- `INFO`: 상태 전이, 정상 실행
- `WARN`: 재시도 가능 이상 징후
- `ERROR`: 실행 실패, 외부 의존성 오류

## 7. CI 전략

PR 마다 자동 실행:

- BE lint
- BE unit/integration tests
- FE lint
- FE component/integration tests
- docs 링크 및 기본 형식 검증

merge 전 품질 게이트:

- 테스트 전부 통과
- 필수 리뷰 완료
- 빌드 성공

## 8. CD 전략

초기 권장 단계:

1. `main` merge 시 staging 배포
2. smoke test 실행
3. 수동 승인 또는 조건 만족 시 production 배포

장기적으로는:

- migration 체크
- rollback 전략
- feature flag

## 9. 팀별 요구사항

### Backend

- endpoint 와 scheduler 에 메트릭/로그 삽입
- execution path 에 trace span 추가
- 실패 원인 구분 가능한 예외 체계

### Frontend

- API 실패 및 주요 사용자 액션 로깅
- 화면 에러 경계 처리
- 필요 시 web-vitals 또는 UX 측정 추가

## 10. 초기 구현 티켓

- `feature/be-structured-logging`
- `feature/be-metrics-instrumentation`
- `feature/be-tracing-bootstrap`
- `feature/ci-be-quality-gate`
- `feature/ci-fe-quality-gate`
- `feature/ops-grafana-dashboards`
