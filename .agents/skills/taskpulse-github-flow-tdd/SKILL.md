---
name: taskpulse-github-flow-tdd
description: Use when working on TaskPulse Agent tickets so Codex follows the repository's GitHub Flow and TDD process, starts each unit from a short-lived branch off `dev`, writes tests first, keeps PR scope single-purpose, and updates docs/contracts when interfaces change.
---

# TaskPulse GitHub Flow TDD

Use this skill whenever the task is tied to a TaskPulse Agent ticket or when implementing FE/BE work in this repository.

## Workflow

1. Identify the assigned ticket in `BE/.agents/tasks/manifest.json` or `FE/.agents/tasks/manifest.json`.
2. Read the matching ticket file under `tickets/`.
3. Confirm owner, branch name, dependencies, acceptance criteria, and required tests.
4. Create or switch to the task branch from `dev` before implementation.
5. If the task changes an API or UI contract, read the relevant docs in `BE/docs/` or `FE/docs/`.
6. Work in this order:
   - write or update failing tests first
   - implement the minimum code to pass
   - rerun the nearest tests
   - rerun broader related tests
   - update docs if contracts changed
   - prepare a single-purpose PR summary
7. Keep the change single-purpose and aligned to the ticket branch.

## Required checks

- Do not merge unrelated edits into the same task.
- Do not treat implementation as complete until tests pass.
- Include at least one failure-path test for behavior changes.
- Preserve GitHub Flow:
  - branch from `dev`
  - one ticket per PR
  - PR only after tests pass

## Ticket sources

- Backend tickets: `BE/.agents/tasks/`
- Frontend tickets: `FE/.agents/tasks/`

## When to load references

- For backend work, read:
  - `BE/docs/architecture.md`
  - `BE/docs/implementation-plan.md`
  - `BE/.agents/*.md`
- For frontend work, read:
  - `FE/docs/architecture.md`
  - `FE/docs/implementation-plan.md`
  - `FE/.agents/*.md`
- For collaboration, observability, and release constraints, read:
  - `AGENTS.md`
  - `docs/observability-cicd.md`
  - `references/pr-checklist.md`

## Completion template

Before closing a task, verify:

- branch name is explicit and matches the task scope
- assigned ticket acceptance criteria met
- required tests added and passing
- related docs updated
- logs/metrics considered if execution path changed
- response states covered if UI changed
- PR summary is ready with test commands and residual risks
