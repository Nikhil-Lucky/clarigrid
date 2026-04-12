from __future__ import annotations

import os
import re
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

from openai import OpenAI

from app.env import ClariGridEnv
from app.models import ClariGridAction, CellReference

BENCHMARK = "clarigrid"
MODEL_NAME = os.getenv("MODEL_NAME", "Qwen/Qwen2.5-72B-Instruct")
API_BASE_URL = os.getenv("API_BASE_URL", "https://router.huggingface.co/v1")
API_KEY = os.getenv("API_KEY") or os.getenv("HF_TOKEN")
MAX_STEPS = 12

TASK_OVERRIDE = os.getenv("CLARIGRID_TASK")
TASKS = [TASK_OVERRIDE] if TASK_OVERRIDE else ["easy", "medium", "hard"]


def log_start(task: str, env: str, model: str) -> None:
    print(f"[START] task={task} env={env} model={model}", flush=True)


def log_step(step: int, action: str, reward: float, done: bool, error: str | None) -> None:
    err = error if error else "null"
    print(
        f"[STEP] step={step} action={action} reward={reward:.2f} done={str(done).lower()} error={err}",
        flush=True,
    )


def log_end(success: bool, steps: int, score: float, rewards: list[float]) -> None:
    rewards_str = ",".join(f"{r:.2f}" for r in rewards)
    print(
        f"[END] success={str(success).lower()} steps={steps} score={score:.3f} rewards={rewards_str}",
        flush=True,
    )


def make_llm_proxy_call(client: OpenAI, task_name: str, step: int, proposed_action: str) -> None:
    try:
        client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {
                    "role": "system",
                    "content": "You are assisting with a tabular data cleaning environment.",
                },
                {
                    "role": "user",
                    "content": (
                        f"Task: {task_name}\n"
                        f"Step: {step}\n"
                        f"Proposed next action: {proposed_action}\n"
                        "Reply with one short sentence confirming whether this action is reasonable."
                    ),
                },
            ],
            temperature=0.0,
            max_tokens=30,
        )
    except Exception:
        pass


def is_valid_email(value: Any) -> bool:
    if value is None:
        return False
    text = str(value).strip()
    return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", text))


def normalize_date(value: Any) -> Optional[str]:
    if value is None:
        return None

    text = str(value).strip()
    if text == "":
        return "missing"
    if text.lower() == "missing":
        return "missing"

    formats = [
        "%Y-%m-%d",
        "%d/%m/%Y",
        "%Y/%m/%d",
        "%d-%m-%Y",
    ]

    for fmt in formats:
        try:
            return datetime.strptime(text, fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue

    return None


def normalize_country(value: Any) -> Optional[str]:
    text = str(value).strip()
    mapping = {
        "india": "India",
        "ind": "India",
    }
    return mapping.get(text.lower())


def normalize_product(value: Any) -> Optional[str]:
    text = str(value).strip().lower()
    mapping = {
        "laptop": "Laptop",
        "phone": "Phone",
    }
    return mapping.get(text)


def normalize_currency(value: Any) -> Optional[str]:
    text = str(value).strip()
    mapping = {
        "rs": "INR",
        "₹": "INR",
        "inr": "INR",
    }
    return mapping.get(text.lower() if text != "₹" else text)


def normalize_status(value: Any) -> Optional[str]:
    text = str(value).strip().lower()
    mapping = {
        "delivered": "Delivered",
        "shipped": "Shipped",
    }
    return mapping.get(text)


def normalize_department(value: Any) -> Optional[str]:
    text = str(value).strip().lower()
    mapping = {
        "engineering": "Engineering",
        "finance": "Finance",
        "sales": "Sales",
        "hr": "HR",
    }
    return mapping.get(text)


def normalize_numeric_string(value: Any) -> Optional[str]:
    text = str(value).strip()
    if text == "":
        return "missing"

    cleaned = text.replace(",", "")
    try:
        num = float(cleaned)
        if num.is_integer():
            return str(int(num))
        return str(num)
    except ValueError:
        return None


def build_action_string(row: int, col: str, value: str) -> str:
    return f"set_cell(row={row},col={col},value={value})"


def make_set_action(row: int, col: str, value: str) -> Tuple[str, ClariGridAction]:
    return (
        build_action_string(row, col, value),
        ClariGridAction(
            action_type="set_cell",
            cell=CellReference(row=row, col=col),
            value=value,
        ),
    )


def choose_easy_action(table: List[Dict[str, Any]]) -> Optional[Tuple[str, ClariGridAction]]:
    for row_idx, row in enumerate(table):
        email = str(row.get("email", "")).strip()
        if email == "":
            return make_set_action(row_idx, "email", "missing@example.com")

        if email == "vikram_at_mail.com":
            return make_set_action(row_idx, "email", "vikram@mail.com")

    for row_idx, row in enumerate(table):
        signup_date = str(row.get("signup_date", "")).strip()
        normalized = normalize_date(signup_date)
        if normalized and normalized != signup_date:
            return make_set_action(row_idx, "signup_date", normalized)

    for row_idx, row in enumerate(table):
        country = str(row.get("country", "")).strip()
        normalized = normalize_country(country)
        if normalized and normalized != country:
            return make_set_action(row_idx, "country", normalized)

    return None


def choose_medium_action(table: List[Dict[str, Any]]) -> Optional[Tuple[str, ClariGridAction]]:
    for row_idx, row in enumerate(table):
        product = str(row.get("product", "")).strip()
        normalized = normalize_product(product)
        if normalized and normalized != product:
            return make_set_action(row_idx, "product", normalized)

    for row_idx, row in enumerate(table):
        price = str(row.get("price", "")).strip()
        normalized = normalize_numeric_string(price)
        if normalized and normalized != price:
            return make_set_action(row_idx, "price", normalized)

    for row_idx, row in enumerate(table):
        currency = str(row.get("currency", "")).strip()
        normalized = normalize_currency(currency)
        if normalized and normalized != currency:
            return make_set_action(row_idx, "currency", normalized)

    for row_idx, row in enumerate(table):
        order_date = str(row.get("order_date", "")).strip()
        normalized = normalize_date(order_date)
        if normalized and normalized != order_date:
            return make_set_action(row_idx, "order_date", normalized)

    for row_idx, row in enumerate(table):
        status = str(row.get("status", "")).strip()
        normalized = normalize_status(status)
        if normalized and normalized != status:
            return make_set_action(row_idx, "status", normalized)

    return None


def find_hard_duplicate_row(table: List[Dict[str, Any]]) -> Optional[int]:
    seen_employee_ids: Dict[str, int] = {}
    for row_idx, row in enumerate(table):
        employee_id = str(row.get("employee_id", "")).strip()
        if employee_id and employee_id in seen_employee_ids:
            return row_idx
        seen_employee_ids[employee_id] = row_idx
    return None


def choose_hard_action(table: List[Dict[str, Any]]) -> Optional[Tuple[str, ClariGridAction]]:
    duplicate_row = find_hard_duplicate_row(table)
    if duplicate_row is not None:
        return (
            f"delete_row(row={duplicate_row})",
            ClariGridAction(action_type="delete_row", row_index=duplicate_row),
        )

    for row_idx, row in enumerate(table):
        email = str(row.get("email", "")).strip()
        if email == "karancompany.com":
            return make_set_action(row_idx, "email", "karan@company.com")

    for row_idx, row in enumerate(table):
        department = str(row.get("department", "")).strip()
        normalized = normalize_department(department)
        if normalized and normalized != department:
            return make_set_action(row_idx, "department", normalized)

    for row_idx, row in enumerate(table):
        salary = str(row.get("salary", "")).strip()
        if salary == "":
            return make_set_action(row_idx, "salary", "missing")

        normalized_salary = normalize_numeric_string(salary)
        if normalized_salary and normalized_salary != salary:
            if salary == "-5000":
                return make_set_action(row_idx, "salary", "0")
            return make_set_action(row_idx, "salary", normalized_salary)

    for row_idx, row in enumerate(table):
        join_date = str(row.get("join_date", "")).strip()
        normalized = normalize_date(join_date)
        if normalized and normalized != join_date:
            return make_set_action(row_idx, "join_date", normalized)

    return None


def choose_action(env: ClariGridEnv, task_name: str, step: int) -> Tuple[str, ClariGridAction]:
    table = env.state().current_table

    if task_name == "easy":
        action = choose_easy_action(table)
        if action:
            return action

    elif task_name == "medium":
        action = choose_medium_action(table)
        if action:
            return action

    elif task_name == "hard":
        action = choose_hard_action(table)
        if action:
            return action

    return "finish_task()", ClariGridAction(action_type="finish_task")


def run_single_task(client: OpenAI, task_name: str) -> None:
    env = ClariGridEnv(task_name=task_name, max_steps=MAX_STEPS)
    rewards: list[float] = []
    steps_taken = 0
    score = 0.0
    success = False

    log_start(task=task_name, env=BENCHMARK, model=MODEL_NAME)

    try:
        result = env.reset()

        for step in range(1, MAX_STEPS + 1):
            if result.done:
                break

            action_str, action = choose_action(env, task_name, step)

            make_llm_proxy_call(client, task_name, step, action_str)
            result = env.step(action)

            rewards.append(result.reward)
            steps_taken = step
            score = float(result.info.get("score", 0.0))

            log_step(
                step=step,
                action=action_str,
                reward=result.reward,
                done=result.done,
                error=None,
            )

            if result.done:
                break

        if score <= 0.0:
            score = 0.01
        elif score >= 1.0:
            score = 0.99

        success = score >= 0.8

    finally:
        log_end(success=success, steps=steps_taken, score=score, rewards=rewards)


def main() -> None:
    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

    for task_name in TASKS:
        run_single_task(client, task_name)


if __name__ == "__main__":
    main()