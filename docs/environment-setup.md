# Environment Setup

## 1. 목표 스택

- Backend: `uv` + `FastAPI` + `LangChain` + `LangGraph`
- Frontend: `React` + `Vite`

현재 저장소 상태:

- [BE/pyproject.toml](/home/min/Workspace/working/chatbot/BE/pyproject.toml)
- [FE/package.json](/home/min/Workspace/working/chatbot/FE/package.json)

## 2. 로컬 실행 전제

- Python `3.12+`
- `uv`
- Node.js `22+`
- npm `11+`

## 3. Backend 설정

작업 디렉터리:

- [BE](/home/min/Workspace/working/chatbot/BE)

초기 실행:

```bash
cd BE
uv sync
uv run uvicorn be.app:app --reload
```

예정 환경 변수:

```env
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4.1-mini
APP_TIMEZONE=Asia/Seoul
```

메모:

- 현재 `pyproject.toml`에는 FastAPI, LangChain, LangGraph 계열 의존성이 추가되어 있다.
- 실제 app 모듈과 실행 엔트리포인트는 아직 정의 전이며, 다음 구현 단계에서 맞춘다.

## 4. Frontend 설정

작업 디렉터리:

- [FE](/home/min/Workspace/working/chatbot/FE)

초기 실행:

```bash
cd FE
npm install
npm run dev
```

예정 환경 변수:

```env
VITE_API_BASE_URL=http://localhost:8000
```

## 5. 권장 디렉터리 방향

```text
BE/
  src/be/
    app.py
    api/
    domain/
    services/
    scheduler/
    agents/
FE/
  src/
    pages/
    components/
    features/
docs/
```

## 6. 다음 단계 제안

1. 문서 기준으로 MVP 범위를 확정한다.
2. 데이터 모델(Event, Execution, Tool Registry)을 먼저 정의한다.
3. 백엔드 API와 스케줄러를 구현한다.
4. React 캘린더 UI와 실행 결과 뷰를 연결한다.
