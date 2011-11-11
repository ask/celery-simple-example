import time

from celery.task import task


@task
def add(x, y):
    return x + y


@task(ignore_result=True)
def compute(x, y):
    "Perform a computation, calling another task to handle the results."
    time.sleep(5)
    return handle_result.delay(x * y).task_id


@task(ignore_result=True)
def handle_result(result):
    "Handle the result of compute."
    print result
