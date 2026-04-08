---
title: ClariGrid
emoji: 📊
colorFrom: blue
colorTo: indigo
sdk: docker
app_port: 7860
pinned: false
---

# ClariGrid

ClariGrid is an OpenEnv-style environment for tabular data quality repair.

The environment lets an AI agent interact with messy spreadsheet-like data, apply cleaning actions, receive intermediate rewards, and get a final score based on how close the cleaned table is to the expected output.

## Motivation

Data cleaning is a real-world task performed by analysts, operations teams, and business users. ClariGrid turns this into an agent environment with:
- structured observations
- structured actions
- deterministic grading
- meaningful reward shaping

## Tasks

ClariGrid includes 3 tasks with increasing difficulty.

### Easy
Repair missing and invalid values:
- empty emails
- invalid email formats
- inconsistent dates
- country normalization

### Medium
Standardize inconsistent fields:
- product names
- prices
- currency values
- order dates
- status labels

### Hard
End-to-end dataset repair:
- duplicate handling
- invalid values
- normalization
- impossible values
- preserving already-correct rows

## Action Space

Supported actions:
- `inspect_cell`
- `set_cell`
- `delete_row`
- `mark_invalid`
- `finish_task`

## Observation Space

Each observation contains:
- task name
- task instructions
- current table
- column names
- steps taken
- maximum steps
- known issues list
- last action message

## Reward Design

ClariGrid uses partial-progress reward shaping:
- positive reward when the table gets closer to the expected cleaned output
- negative reward when the table gets worse
- small penalty for no-op or unhelpful actions
- finish bonus or penalty based on final quality

## Grading

Each task has a deterministic grader that compares the current table against the expected cleaned table and returns a score in the range `[0.0, 1.0]`.

## Environment Structure

The project includes:
- typed Pydantic models
- `reset()`
- `step(action)`
- `state()`
- task-specific datasets
- programmatic graders
- reward shaping
- baseline inference script
- Docker support
- Hugging Face Space deployment

## Inference

The baseline script is `inference.py`.

It prints standardized logs in this format:
- `[START]`
- `[STEP]`
- `[END]`

This is used to produce reproducible baseline scores across tasks.

## Hugging Face Space Endpoints

The Docker Space runs a FastAPI server.

### Root endpoint
`/`

Returns a simple status response:
- message
- status
- current task

### Run endpoint
`/run`

Executes the baseline inference script and returns:
- `stdout`
- `stderr`
- `returncode`

## Project Structure

```text
clarigrid/
├── app/
│   ├── __init__.py
│   ├── env.py
│   ├── graders.py
│   ├── models.py
│   ├── rewards.py
│   ├── tasks.py
│   └── utils.py
├── data/
│   ├── easy_task.json
│   ├── medium_task.json
│   └── hard_task.json
├── server/
│   └── app.py
├── Dockerfile
├── inference.py
├── openenv.yaml
├── pyproject.toml
├── requirements.txt
├── test_run.py
└── README.md