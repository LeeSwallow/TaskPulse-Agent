from be.app import app, create_app


def main() -> None:
    import uvicorn

    uvicorn.run("be.app:app", host="0.0.0.0", port=8000, reload=False)
