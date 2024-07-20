import pytest
from pydantic import ValidationError
from synctodoist import TodoistAPI
import time
from synctodoist.models import Task, Duration

def test_task_creation_with_duration():
    task = Task(
        content="Test task",
        duration=Duration(amount=15, unit="minute")
    )
    assert task.duration.amount == 15
    assert task.duration.unit == "minute"

def test_task_creation_without_duration():
    task = Task(content="Test task")
    assert task.duration is None

def test_invalid_duration_amount():
    with pytest.raises(ValidationError):
        Task(
            content="Test task",
            duration=Duration(amount=0, unit="minute")
        )

def test_invalid_duration_unit():
    with pytest.raises(ValidationError):
        Task(
            content="Test task",
            duration=Duration(amount=15, unit="hour")
        )

@pytest.mark.integration
def test_add_task_with_duration(synced_todoist):
    task = Task(
        content="Test task with duration",
        duration=Duration(amount=30, unit="minute")
    )
    synced_todoist.add_task(task)
    synced_todoist.commit()
    
    # Fetch the task to ensure it was saved correctly
    saved_task = synced_todoist.get_task(task.id)
    assert saved_task.duration.amount == 30
    assert saved_task.duration.unit == "minute"

    # Clean up
    synced_todoist.delete_task(task)
    synced_todoist.commit()

@pytest.mark.integration
def test_update_task_duration(synced_todoist):
    task = Task(content="Test task for updating duration")
    synced_todoist.add_task(task)
    synced_todoist.commit()
    
    time.sleep(2)  # Add a small delay

    # Update the task with a duration
    task.duration = Duration(amount=45, unit="minute")
    synced_todoist.update_task(task.id, task)
    synced_todoist.commit()

    # Fetch the task to ensure it was updated correctly
    updated_task = synced_todoist.get_task(task.id)
    assert updated_task.duration.amount == 45
    assert updated_task.duration.unit == "minute"

    # Clean up
    synced_todoist.delete_task(task)
    synced_todoist.commit()
