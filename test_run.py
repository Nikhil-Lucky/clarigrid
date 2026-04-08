from app.env import ClariGridEnv
from app.models import ClariGridAction, CellReference

env = ClariGridEnv(task_name="easy", max_steps=5)

result = env.reset()
print("RESET:")
print(result.model_dump())

step1 = env.step(
    ClariGridAction(
        action_type="set_cell",
        cell=CellReference(row=1, col="email"),
        value="missing@example.com",
    )
)
print("\nSTEP 1:")
print(step1.model_dump())

step2 = env.step(
    ClariGridAction(
        action_type="finish_task"
    )
)
print("\nSTEP 2:")
print(step2.model_dump())