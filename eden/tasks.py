import time
import eden
from . import utils


def create(generatorName, config):
    return utils.post("/tasks/create", {
        "generatorName": generatorName,
        "config": config
    })


def get(taskId):
    result = utils.get("/tasks/" + taskId)
    return result["task"]


def run(generatorName, config):
    task = create(generatorName, config)
    task_id = task["taskId"]
    print(f"Task {task_id} started")
    start_time = time.time()
    task_duration = 0
    while task_duration < eden.timeout:
        task_result = get(task_id)
        task_duration = time.time() - start_time
        status = task_result["status"]
        if eden.verbose:
            progress = task_result["progress"]
            progress_percent_str = f"{(100*progress):.1f}%"
            print(f"Task ID: {task_id}: {status}, progress: {progress_percent_str}, runtime: {task_duration:.1f} seconds")
        if status == 'completed':
            if eden.verbose:
                print(f"Task {task_id} completed in {task_duration:.1f} seconds")
            creation = task_result["creation"]
            return creation
        elif status == 'failed':
            print(f"Task failed after {task_duration:.1f} seconds")
            raise eden.EdenTaskFailedError("Task failed")
        time.sleep(eden.poll_interval)

    print(f"Task {task_id} timed out after {task_duration:.1f} seconds, returning")
