# ClariGrid

ClariGrid is an OpenEnv-style environment for tabular data quality repair.

The agent interacts with messy spreadsheet-like data and performs cleaning operations such as:
- fixing missing values
- correcting invalid formats
- standardizing inconsistent entries
- removing bad records

## Motivation

Data cleaning is a real-world task performed by analysts, operations teams, and business users. ClariGrid turns this into an agent environment with structured actions, observations, rewards, and graders.

## Tasks

### Easy
Repair missing and invalid values:
- empty emails
- invalid email formats
- inconsistent dates
- country normalization

### Medium
Standardize fields:
- product names
- prices
- currency values
- order dates
- statuses

### Hard
End-to-end dataset repair:
- duplicate handling
- invalid values
- normalization
- impossible values
- preserving correct rows

## Action Space

Supported actions:
- `inspect_cell`
- `set_cell`
- `delete_row`
- `mark_invalid`
- `finish_task`

## Observation Space

The observation contains:
- task name
- instructions
- current table
- columns
- steps taken
- max steps
- last action message

## Reward Design

ClariGrid provides partial progress rewards:
- positive reward when the table gets closer to the expected cleaned output
- negative reward when the table gets worse
- small penalty for no-op or useless actions
- bonus/penalty on finishing based on final quality

## Grading

Each task has a deterministic grader that compares the current table to the expected cleaned table and returns a score in `[0.0, 1.0]`.

## Project Structure

```text
clarigrid/
├── app/
├── data/
├── inference.py
├── openenv.yaml
├── Dockerfile
├── requirements.txt
└── README.md