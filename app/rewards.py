from typing import Any, Dict, List

from app.graders import compare_tables


def compute_reward(
    previous_table: List[Dict[str, Any]],
    current_table: List[Dict[str, Any]],
    expected_table: List[Dict[str, Any]],
    action_type: str,
) -> float:
    prev_score, _ = compare_tables(previous_table, expected_table)
    curr_score, _ = compare_tables(current_table, expected_table)

    delta = curr_score - prev_score

    reward = 0.0

    if delta > 0:
        reward += min(delta + 0.05, 0.3)
    elif delta < 0:
        reward -= min(abs(delta) + 0.05, 0.3)
    else:
        reward -= 0.02

    if action_type == "finish_task":
        reward += 0.1 if curr_score > 0.8 else -0.1

    reward = max(min(reward, 1.0), -1.0)
    return round(reward, 4)