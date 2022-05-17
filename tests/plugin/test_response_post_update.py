"""When a Plugin's operation is tied to a task, the plugin can update that task while it is still running,
or asynchronously at any time."""

import json

import pytest

from steamship.app import Response
from steamship.base.tasks import TaskState, Task
from tests.plugin.trainable.util import create_dummy_training_task
from tests.utils.client import get_steamship_client


def test_response_post_update_fails_when_no_task_present():
    client = get_steamship_client()
    response = Response()
    with pytest.raises(Exception):
        response.post_update(client)

    # No task_id
    response2 = Response(status=Task())
    with pytest.raises(Exception):
        response2.post_update(client)


def test_response_post_update_can_update_task():
    client = get_steamship_client()
    task_result = create_dummy_training_task(client)
    task = task_result.task

    new_state = TaskState.failed
    new_message = "HI THERE"
    new_output = {"a": 3}

    assert task.state != new_state
    assert task.status_message != new_message
    assert task.output != new_output

    response = Response(status=task)

    response.status.state = new_state
    response.status.status_message = new_message
    response.status.new_output = new_output

    # Sanity check: we'll prove that caling task.check() resets this..
    task_result.check()

    # Assert not equal
    assert task.state != new_state
    assert task.status_message != new_message
    assert task.output != new_output

    # And override again
    response.status.state = new_state
    response.status.status_message = new_message
    response.set_data(json=new_output)

    # Now we call post_update
    response.post_update(client)

    # Call task.check
    task_result.check()

    # Assert equal
    assert task.state == new_state
    assert task.status_message == new_message
    assert task.output == json.dumps(new_output)