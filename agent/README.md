# Subagent Definitions

이 디렉터리는 이 저장소에서 재사용할 수 있는 로컬 subagent 설정을 둔다.

파일 구성:

- `pm.yaml`: PM/팀장 페르소나. 전체 요구사항 정리, 작업 분할, 우선순위와 머지 가능 상태 판단
- `frontend.yaml`: React/Vite 프런트엔드 구현 전용
- `backend.yaml`: `uv`/FastAPI/LangGraph 백엔드 구현 전용
- `devops.yaml`: CI/CD, 환경 설정, 자동화, 배포 절차 전용
- `qa.yaml`: 테스트 전략, 회귀 점검, 검증 범위 판단 전용
- `docs.yaml`: PRD/요구사항/구현 문서 정합성 유지 전용
- `manager.yaml`: 경량 조율용 보조 에이전트. 필요 시 `pm.yaml` 대신 단순 분할/점검에 사용

운영 원칙:

- 루트 `AGENTS.md` 의 `GitHub Flow + TDD` 를 따른다.
- 구현 전에 `docs/`, `FE/docs/`, `BE/docs/` 기준 문서를 먼저 확인한다.
- 동작 변화가 있으면 테스트를 먼저 추가하고, 테스트 통과 전에는 완료로 간주하지 않는다.
- 관련 없는 변경은 같은 작업에 섞지 않는다.

권장 사용 방식:

1. `pm.yaml` 이 요청을 수용 기준과 작업 단위로 분해한다.
2. `frontend.yaml`, `backend.yaml`, `devops.yaml`, `docs.yaml` 에 역할별 작업을 할당한다.
3. `qa.yaml` 이 테스트 범위와 회귀 리스크를 점검한다.
4. PM 이 최종적으로 문서, 테스트, CI/CD, 머지 가능 상태를 판단한다.
