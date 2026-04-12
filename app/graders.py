from __future__ import annotations

from typing import Any, Dict, List, Tuple


def _normalize_value(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _normalize_row(row: Dict[str, Any]) -> Dict[str, str]:
    return {str(k): _normalize_value(v) for k, v in row.items()}


def _row_signature(row: Dict[str, str]) -> Tuple[Tuple[str, str], ...]:
    return tuple(sorted(row.items()))


def _canonicalize_table(table: List[Dict[str, Any]]) -> List[Dict[str, str]]:
    normalized_rows = [_normalize_row(row) for row in table]
    return sorted(normalized_rows, key=_row_signature)


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

    current_rows = _canonicalize_table(current_table)
    expected_rows = _canonicalize_table(expected_table)

    total_cells = 0
    matched_cells = 0

    min_rows = min(len(current_rows), len(expected_rows))
    max_rows = max(len(current_rows), len(expected_rows))

    for row_idx in range(min_rows):
        current_row = current_rows[row_idx]
        expected_row = expected_rows[row_idx]

        all_columns = set(current_row.keys()) | set(expected_row.keys())

        for col in all_columns:
            total_cells += 1
            current_val = current_row.get(col, "")
            expected_val = expected_row.get(col, "")

            if current_val == expected_val:
                matched_cells += 1

    if max_rows > min_rows:
        extra_rows = max_rows - min_rows
        reference_row = expected_rows[0] if expected_rows else {}
        total_cells += extra_rows * max(len(reference_row.keys()), 1)

    row_count_match = len(current_rows) == len(expected_rows)

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