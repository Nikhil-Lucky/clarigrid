from copy import deepcopy
from typing import Any, Dict, List, Optional

from app.graders import compare_tables, grade_task
from app.models import (
    ClariGridAction,
    ClariGridObservation,
    ClariGridState,
    ResetResult,
    StepResult,
)
from app.rewards import compute_reward
from app.tasks import get_expected_table, get_task_instructions, load_task_data


class ClariGridEnv:
    def __init__(self, task_name: str = "easy", max_steps: int = 10):
        allowed_tasks = {"easy", "medium", "hard"}
        if task_name not in allowed_tasks:
            raise ValueError(f"Invalid task_name '{task_name}'. Must be one of {sorted(allowed_tasks)}.")

        self.task_name = task_name
        self.max_steps = max_steps
        self._state: Optional[ClariGridState] = None

    def _build_observation(self, last_action_message: Optional[str] = None) -> ClariGridObservation:
        if self._state is None:
            raise ValueError("Environment not initialized. Call reset() first.")

        current_table = self._state.current_table
        columns = list(current_table[0].keys()) if current_table else []

        return ClariGridObservation(
            task_name=self._state.task_name,
            instructions=get_task_instructions(self._state.task_name),
            table=deepcopy(current_table),
            columns=columns,
            steps_taken=self._state.steps_taken,
            max_steps=self._state.max_steps,
            known_issues=[],
            last_action_message=last_action_message,
        )

    def reset(self) -> ResetResult:
        original_table = load_task_data(self.task_name)
        expected_table = get_expected_table(self.task_name)

        self._state = ClariGridState(
            task_name=self.task_name,
            original_table=deepcopy(original_table),
            current_table=deepcopy(original_table),
            expected_table=deepcopy(expected_table),
            steps_taken=0,
            max_steps=self.max_steps,
            done=False,
            last_reward=0.0,
            reward_history=[],
            action_history=[],
        )

        return ResetResult(
            observation=self._build_observation("Environment reset."),
            reward=0.0,
            done=False,
            info={"task_name": self.task_name},
        )

    def state(self) -> ClariGridState:
        if self._state is None:
            raise ValueError("Environment not initialized. Call reset() first.")
        return self._state

    def _set_cell(self, table: List[Dict[str, Any]], action: ClariGridAction) -> str:
        if action.cell is None or action.value is None:
            return "set_cell requires both cell and value."

        row = action.cell.row
        col = action.cell.col

        if row >= len(table):
            return f"Row {row} out of range."

        if col not in table[row]:
            return f"Column '{col}' not found."

        table[row][col] = action.value
        return f"Set row {row}, column '{col}' to '{action.value}'."

    def _delete_row(self, table: List[Dict[str, Any]], action: ClariGridAction) -> str:
        if action.row_index is None:
            return "delete_row requires row_index."

        row = action.row_index
        if row >= len(table):
            return f"Row {row} out of range."

        deleted = table.pop(row)
        return f"Deleted row {row}: {deleted}"

    def _inspect_cell(self, table: List[Dict[str, Any]], action: ClariGridAction) -> str:
        if action.cell is None:
            return "inspect_cell requires cell."

        row = action.cell.row
        col = action.cell.col

        if row >= len(table):
            return f"Row {row} out of range."

        if col not in table[row]:
            return f"Column '{col}' not found."

        value = table[row][col]
        return f"Cell[{row}][{col}] = {value}"

    def _mark_invalid(self, table: List[Dict[str, Any]], action: ClariGridAction) -> str:
        if action.cell is None:
            return "mark_invalid requires cell."

        row = action.cell.row
        col = action.cell.col

        if row >= len(table):
            return f"Row {row} out of range."

        if col not in table[row]:
            return f"Column '{col}' not found."

        table[row][col] = "invalid"
        return f"Marked row {row}, column '{col}' as invalid."

    def step(self, action: ClariGridAction) -> StepResult:
        if self._state is None:
            raise ValueError("Environment not initialized. Call reset() first.")

        if self._state.done:
            return StepResult(
                observation=self._build_observation("Task already completed."),
                reward=0.0,
                done=True,
                info={"score": grade_task(self._state.current_table, self._state.expected_table)},
            )

        previous_table = deepcopy(self._state.current_table)
        current_table = self._state.current_table

        message = ""
        if action.action_type == "set_cell":
            message = self._set_cell(current_table, action)
        elif action.action_type == "delete_row":
            message = self._delete_row(current_table, action)
        elif action.action_type == "inspect_cell":
            message = self._inspect_cell(current_table, action)
        elif action.action_type == "mark_invalid":
            message = self._mark_invalid(current_table, action)
        elif action.action_type == "finish_task":
            message = "Finishing task."
            self._state.done = True
        else:
            message = f"Unsupported action: {action.action_type}"

        self._state.steps_taken += 1

        if self._state.steps_taken >= self._state.max_steps:
            self._state.done = True

        reward = compute_reward(
            previous_table=previous_table,
            current_table=current_table,
            expected_table=self._state.expected_table,
            action_type=action.action_type,
        )

        self._state.last_reward = reward
        self._state.reward_history.append(reward)
        self._state.action_history.append(action.model_dump())

        score, details = compare_tables(self._state.current_table, self._state.expected_table)

        obs = self._build_observation(message)

        return StepResult(
            observation=obs,
            reward=reward,
            done=self._state.done,
            info={
                "message": message,
                "score": score,
                "grader_details": details,
            },
        )