from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field


TaskName = Literal["easy", "medium", "hard"]
ActionType = Literal[
    "inspect_cell",
    "set_cell",
    "delete_row",
    "mark_invalid",
    "finish_task",
]


class CellReference(BaseModel):
    row: int = Field(..., ge=0)
    col: str = Field(..., min_length=1)


class ClariGridAction(BaseModel):
    action_type: ActionType
    cell: Optional[CellReference] = None
    value: Optional[str] = None
    row_index: Optional[int] = Field(default=None, ge=0)
    reason: Optional[str] = None


class ClariGridObservation(BaseModel):
    task_name: TaskName
    instructions: str
    table: List[Dict[str, Any]]
    columns: List[str]
    steps_taken: int
    max_steps: int
    known_issues: List[str] = Field(default_factory=list)
    last_action_message: Optional[str] = None


class ClariGridReward(BaseModel):
    value: float = Field(..., ge=-1.0, le=1.0)
    reason: str


class ClariGridState(BaseModel):
    task_name: TaskName
    original_table: List[Dict[str, Any]]
    current_table: List[Dict[str, Any]]
    expected_table: List[Dict[str, Any]]
    steps_taken: int = 0
    max_steps: int = 10
    done: bool = False
    last_reward: float = 0.0
    reward_history: List[float] = Field(default_factory=list)
    action_history: List[Dict[str, Any]] = Field(default_factory=list)


class StepResult(BaseModel):
    observation: ClariGridObservation
    reward: float
    done: bool
    info: Dict[str, Any] = Field(default_factory=dict)


class ResetResult(BaseModel):
    observation: ClariGridObservation
    reward: float = 0.0
    done: bool = False
    info: Dict[str, Any] = Field(default_factory=dict)