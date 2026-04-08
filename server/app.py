from fastapi import FastAPI
import subprocess
import os

app = FastAPI()


@app.get("/")
def root():
    return {
        "message": "ClariGrid is running",
        "status": "ok",
        "task": os.getenv("CLARIGRID_TASK", "easy"),
    }


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