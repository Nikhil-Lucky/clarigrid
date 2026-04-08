import json
from pathlib import Path
from typing import Any, Dict, List

from app.models import TaskName


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def load_task_data(task_name: TaskName) -> List[Dict[str, Any]]:
    file_map = {
        "easy": DATA_DIR / "easy_task.json",
        "medium": DATA_DIR / "medium_task.json",
        "hard": DATA_DIR / "hard_task.json",
    }

    path = file_map[task_name]
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def get_task_instructions(task_name: TaskName) -> str:
    instructions = {
        "easy": (
            "Clean missing and invalid values. "
            "Fix empty emails, invalid email formats, inconsistent date formats, "
            "and normalize country names."
        ),
        "medium": (
            "Standardize product, price, currency, date, and status fields. "
            "Normalize equivalent values into one consistent format."
        ),
        "hard": (
            "Perform end-to-end dataset repair. "
            "Resolve duplicates, fix invalid emails and dates, normalize department values, "
            "and correct impossible salary values without damaging valid rows."
        ),
    }
    return instructions[task_name]


def get_expected_table(task_name: TaskName) -> List[Dict[str, Any]]:
    expected = {
        "easy": [
            {
                "customer_id": "C001",
                "name": "Rahul",
                "email": "rahul@example.com",
                "signup_date": "2024-01-15",
                "country": "India",
            },
            {
                "customer_id": "C002",
                "name": "Ananya",
                "email": "missing@example.com",
                "signup_date": "2024-02-15",
                "country": "India",
            },
            {
                "customer_id": "C003",
                "name": "Vikram",
                "email": "vikram@mail.com",
                "signup_date": "2024-03-10",
                "country": "India",
            },
            {
                "customer_id": "C004",
                "name": "Sneha",
                "email": "sneha@example.com",
                "signup_date": "missing",
                "country": "India",
            },
        ],
        "medium": [
            {
                "order_id": "O101",
                "product": "Laptop",
                "price": "50000",
                "currency": "INR",
                "order_date": "2024-01-05",
                "status": "Delivered",
            },
            {
                "order_id": "O102",
                "product": "Laptop",
                "price": "50000",
                "currency": "INR",
                "order_date": "2024-01-05",
                "status": "Delivered",
            },
            {
                "order_id": "O103",
                "product": "Phone",
                "price": "30000",
                "currency": "INR",
                "order_date": "2024-02-11",
                "status": "Shipped",
            },
            {
                "order_id": "O104",
                "product": "Phone",
                "price": "missing",
                "currency": "INR",
                "order_date": "2024-02-11",
                "status": "Shipped",
            },
        ],
        "hard": [
            {
                "employee_id": "E001",
                "name": "Asha",
                "department": "Engineering",
                "email": "asha@company.com",
                "salary": "120000",
                "join_date": "2022-06-01",
            },
            {
                "employee_id": "E002",
                "name": "Karan",
                "department": "HR",
                "email": "karan@company.com",
                "salary": "missing",
                "join_date": "2021-09-15",
            },
            {
                "employee_id": "E003",
                "name": "Meera",
                "department": "Finance",
                "email": "meera@company.com",
                "salary": "95000",
                "join_date": "missing",
            },
            {
                "employee_id": "E004",
                "name": "Rohit",
                "department": "Sales",
                "email": "rohit@company.com",
                "salary": "0",
                "join_date": "2023-11-10",
            },
        ],
    }
    return expected[task_name]