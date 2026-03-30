# BE-006 Implement LangGraph agent runner

## Owner

- `be-scheduler-agent-engineer`

## Branch

- `feature/be-agent-runner`

## Goal

허용된 tool 만 사용하는 LangGraph 기반 실행 러너를 구현한다.

## Scope

- `src/be/agents/graph.py`
- `src/be/agents/tool_registry.py`
- `src/be/agents/nodes/`
- `tests/agents/`

## TDD Steps

1. allowlist 테스트 작성
2. summary 생성 테스트 작성
3. empty tool list / unknown tool 테스트 작성
4. 그래프 최소 구현

## Acceptance Criteria

- `plan -> execute_tools -> summarize` 흐름이 동작한다
- 허용되지 않은 tool 은 실행되지 않는다
- 실행 결과가 summary 와 tool log 로 반환된다

## Required Tests

- allowlist tests
- runner summary tests
- tool failure propagation tests
