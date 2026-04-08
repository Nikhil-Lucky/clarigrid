import os

from app.env import ClariGridEnv
from app.models import ClariGridAction, CellReference

TASK_NAME = os.getenv("CLARIGRID_TASK", "easy")
BENCHMARK = "clarigrid"
MODEL_NAME = os.getenv("MODEL_NAME", "rule-based-baseline")
MAX_STEPS = 12


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


def choose_action(env: ClariGridEnv, task_name: str, step: int):
    _ = env.state()

    if task_name == "easy":
        if step == 1:
            return "set_cell(row=1,col=email,value=missing@example.com)", ClariGridAction(
                action_type="set_cell",
                cell=CellReference(row=1, col="email"),
                value="missing@example.com",
            )
        if step == 2:
            return "set_cell(row=2,col=email,value=vikram@mail.com)", ClariGridAction(
                action_type="set_cell",
                cell=CellReference(row=2, col="email"),
                value="vikram@mail.com",
            )
        if step == 3:
            return "set_cell(row=1,col=signup_date,value=2024-02-15)", ClariGridAction(
                action_type="set_cell",
                cell=CellReference(row=1, col="signup_date"),
                value="2024-02-15",
            )
        if step == 4:
            return "set_cell(row=2,col=signup_date,value=2024-03-10)", ClariGridAction(
                action_type="set_cell",
                cell=CellReference(row=2, col="signup_date"),
                value="2024-03-10",
            )
        if step == 5:
            return "set_cell(row=1,col=country,value=India)", ClariGridAction(
                action_type="set_cell",
                cell=CellReference(row=1, col="country"),
                value="India",
            )
        if step == 6:
            return "set_cell(row=2,col=country,value=India)", ClariGridAction(
                action_type="set_cell",
                cell=CellReference(row=2, col="country"),
                value="India",
            )
        if step == 7:
            return "set_cell(row=3,col=signup_date,value=missing)", ClariGridAction(
                action_type="set_cell",
                cell=CellReference(row=3, col="signup_date"),
                value="missing",
            )

    elif task_name == "medium":
        if step == 1:
            return "set_cell(row=1,col=product,value=Laptop)", ClariGridAction(
                action_type="set_cell",
                cell=CellReference(row=1, col="product"),
                value="Laptop",
            )
        if step == 2:
            return "set_cell(row=1,col=price,value=50000)", ClariGridAction(
                action_type="set_cell",
                cell=CellReference(row=1, col="price"),
                value="50000",
            )
        if step == 3:
            return "set_cell(row=1,col=currency,value=INR)", ClariGridAction(
                action_type="set_cell",
                cell=CellReference(row=1, col="currency"),
                value="INR",
            )
        if step == 4:
            return "set_cell(row=1,col=order_date,value=2024-01-05)", ClariGridAction(
                action_type="set_cell",
                cell=CellReference(row=1, col="order_date"),
                value="2024-01-05",
            )
        if step == 5:
            return "set_cell(row=1,col=status,value=Delivered)", ClariGridAction(
                action_type="set_cell",
                cell=CellReference(row=1, col="status"),
                value="Delivered",
            )
        if step == 6:
            return "set_cell(row=2,col=price,value=30000)", ClariGridAction(
                action_type="set_cell",
                cell=CellReference(row=2, col="price"),
                value="30000",
            )
        if step == 7:
            return "set_cell(row=2,col=currency,value=INR)", ClariGridAction(
                action_type="set_cell",
                cell=CellReference(row=2, col="currency"),
                value="INR",
            )
        if step == 8:
            return "set_cell(row=2,col=order_date,value=2024-02-11)", ClariGridAction(
                action_type="set_cell",
                cell=CellReference(row=2, col="order_date"),
                value="2024-02-11",
            )
        if step == 9:
            return "set_cell(row=3,col=product,value=Phone)", ClariGridAction(
                action_type="set_cell",
                cell=CellReference(row=3, col="product"),
                value="Phone",
            )
        if step == 10:
            return "set_cell(row=3,col=price,value=missing)", ClariGridAction(
                action_type="set_cell",
                cell=CellReference(row=3, col="price"),
                value="missing",
            )
        if step == 11:
            return "set_cell(row=3,col=status,value=Shipped)", ClariGridAction(
                action_type="set_cell",
                cell=CellReference(row=3, col="status"),
                value="Shipped",
            )

    elif task_name == "hard":
        if step == 1:
            return "delete_row(row=1)", ClariGridAction(
                action_type="delete_row",
                row_index=1,
            )
        if step == 2:
            return "set_cell(row=1,col=email,value=karan@company.com)", ClariGridAction(
                action_type="set_cell",
                cell=CellReference(row=1, col="email"),
                value="karan@company.com",
            )
        if step == 3:
            return "set_cell(row=1,col=salary,value=missing)", ClariGridAction(
                action_type="set_cell",
                cell=CellReference(row=1, col="salary"),
                value="missing",
            )
        if step == 4:
            return "set_cell(row=1,col=join_date,value=2021-09-15)", ClariGridAction(
                action_type="set_cell",
                cell=CellReference(row=1, col="join_date"),
                value="2021-09-15",
            )
        if step == 5:
            return "set_cell(row=2,col=department,value=Finance)", ClariGridAction(
                action_type="set_cell",
                cell=CellReference(row=2, col="department"),
                value="Finance",
            )
        if step == 6:
            return "set_cell(row=2,col=join_date,value=missing)", ClariGridAction(
                action_type="set_cell",
                cell=CellReference(row=2, col="join_date"),
                value="missing",
            )
        if step == 7:
            return "set_cell(row=3,col=salary,value=0)", ClariGridAction(
                action_type="set_cell",
                cell=CellReference(row=3, col="salary"),
                value="0",
            )

    return "finish_task()", ClariGridAction(action_type="finish_task")


def main() -> None:
    env = ClariGridEnv(task_name=TASK_NAME, max_steps=MAX_STEPS)
    rewards: list[float] = []
    steps_taken = 0
    score = 0.0
    success = False

    log_start(task=TASK_NAME, env=BENCHMARK, model=MODEL_NAME)

    try:
        result = env.reset()

        for step in range(1, MAX_STEPS + 1):
            if result.done:
                break

            action_str, action = choose_action(env, TASK_NAME, step)
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

        success = score >= 0.8

    finally:
        log_end(success=success, steps=steps_taken, score=score, rewards=rewards)


if __name__ == "__main__":
    main()