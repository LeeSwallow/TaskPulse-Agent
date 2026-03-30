# Backend Subagents

이 폴더는 `TaskPulse Agent` 백엔드 팀의 로컬 서브에이전트 정의를 담는다.

구성 원칙:

- 각 서브에이전트는 명확한 책임 범위를 가진다.
- 작업은 `GitHub Flow + TDD` 기준으로 분배한다.
- 한 서브에이전트는 하나의 PR 목적만 가진다.
- API/스케줄러/관측성 작업은 서로 계약을 명확히 분리한다.

포함된 서브에이전트:

- `api-engineer.md`
- `scheduler-agent-engineer.md`
- `platform-observability-engineer.md`

참조 문서:

- [BE/docs/team-roles.md](/home/min/Workspace/working/chatbot/BE/docs/team-roles.md)
- [BE/docs/architecture.md](/home/min/Workspace/working/chatbot/BE/docs/architecture.md)
- [BE/docs/implementation-plan.md](/home/min/Workspace/working/chatbot/BE/docs/implementation-plan.md)
