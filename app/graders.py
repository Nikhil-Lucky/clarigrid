from typing import Any, Dict, List, Tuple


def _normalize_value(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def compare_tables(
    current_table: List[Dict[str, Any]],
    expected_table: List[Dict[str, Any]],
) -> Tuple[float, Dict[str, Any]]:
    """
    Returns:
        score in [0.0, 1.0]
        details dict
    """
    if not expected_table:
        return 0.0, {
            "matched_cells": 0,
            "total_cells": 0,
            "row_count_match": False,
            "score": 0.0,
        }

    total_cells = 0
    matched_cells = 0

    min_rows = min(len(current_table), len(expected_table))
    max_rows = max(len(current_table), len(expected_table))

    for row_idx in range(min_rows):
        current_row = current_table[row_idx]
        expected_row = expected_table[row_idx]

        all_columns = set(current_row.keys()) | set(expected_row.keys())

        for col in all_columns:
            total_cells += 1
            current_val = _normalize_value(current_row.get(col, ""))
            expected_val = _normalize_value(expected_row.get(col, ""))

            if current_val == expected_val:
                matched_cells += 1

    if max_rows > min_rows:
        extra_rows = max_rows - min_rows
        reference_row = expected_table[0] if expected_table else {}
        total_cells += extra_rows * max(len(reference_row.keys()), 1)

    row_count_match = len(current_table) == len(expected_table)

    cell_score = matched_cells / total_cells if total_cells > 0 else 0.0
    row_bonus = 0.1 if row_count_match else 0.0

    score = min(cell_score + row_bonus, 1.0)

    return score, {
        "matched_cells": matched_cells,
        "total_cells": total_cells,
        "row_count_match": row_count_match,
        "cell_score": round(cell_score, 4),
        "score": round(score, 4),
    }


def grade_task(
    current_table: List[Dict[str, Any]],
    expected_table: List[Dict[str, Any]],
) -> float:
    score, _ = compare_tables(current_table, expected_table)
    return score