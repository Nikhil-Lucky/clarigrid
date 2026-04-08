from typing import Any, Dict, Optional
import os
import subprocess

from fastapi import Body, FastAPI, HTTPException

from app.env import ClariGridEnv
from app.models import ClariGridAction

app = FastAPI()

CURRENT_ENV: Optional[ClariGridEnv] = None


@app.get("/")
def root():
    return {
        "message": "ClariGrid is running",
        "status": "ok",
        "task": os.getenv("CLARIGRID_TASK", "easy"),
    }


@app.post("/reset")
def reset(payload: Optional[Dict[str, Any]] = Body(default=None)):
    global CURRENT_ENV

    payload = payload or {}
    task_name = payload.get("task_name", os.getenv("CLARIGRID_TASK", "easy"))
    max_steps = int(payload.get("max_steps", 12))

    try:
        CURRENT_ENV = ClariGridEnv(task_name=task_name, max_steps=max_steps)
        result = CURRENT_ENV.reset()
        return result.model_dump()
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@app.post("/step")
def step(payload: Dict[str, Any] = Body(...)):
    global CURRENT_ENV

    if CURRENT_ENV is None:
        raise HTTPException(status_code=400, detail="Environment not initialized. Call /reset first.")

    try:
        action = ClariGridAction.model_validate(payload)
        result = CURRENT_ENV.step(action)
        return result.model_dump()
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@app.get("/state")
def state():
    global CURRENT_ENV

    if CURRENT_ENV is None:
        raise HTTPException(status_code=400, detail="Environment not initialized. Call /reset first.")

    return CURRENT_ENV.state().model_dump()


@app.get("/run")
def run_inference():
    result = subprocess.run(
        ["python", "inference.py"],
        capture_output=True,
        text=True,
        cwd="/app",
    )
    return {
        "stdout": result.stdout,
        "stderr": result.stderr,
        "returncode": result.returncode,
    }


def main():
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=7860)


if __name__ == "__main__":
    main()