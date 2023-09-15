import os
import json
import time
import requests

#####################################################################################
#####################################################################################

EDEN_API_URL = "https://api.eden.art"

HEADERS = {
    "x-api-key":    "YOUR_API_KEY_HERE",
    "x-api-secret": "YOUR_API_SECRET_HERE"
}

POLL_INTERVAL = 5       # poll every 3 seconds
TIMEOUT       = 3600    # timeout after 1 hour

#####################################################################################
#####################################################################################


class EdenAPIError(Exception):
    pass

def save_creation(creation, creation_config, output_folder="eden_creations", fields_to_add = {}):
    """ example creation:
    {
        'mediaAttributes': {'type': 'image'}, 
        'embedding': {'embedding': []}, 
        '_id': '650312effb97c42c63421cfa', 
        'user': '64c24bec7d826645a3c99976',
        'task': '650312dffb97c42c63421770', 
        'praiseCount': 0, 
        'bookmarkCount': 0, 
        'uri': 'https://minio.aws.abraham.fun/creations-stg/f79c7787255e41904048024762045b826de0f9ca2dba7f2bf4b319082ff37e94.jpg', 
        'thumbnail': 'https://minio.aws.abraham.fun/creations-stg/5d45cf147d75fb6fc5f02e12df4502be0d5368d72bc754101bef6360070e95fe.webp', 
        'name': 'A twisting creature of reflective dragonglass swirling above a scorched field amidst a large clearing in a dark forest, radiating with beams of firelight, high quality professional photography, nikon d850 50mm', 
        'attributes': None, 
        'createdAt': '2023-09-14T14:04:31.648Z', 
        'updatedAt': '2023-09-14T14:04:31.648Z', 
        '__v': 0
    }
    """

    """Download and save a creation to a specified folder."""
    
    # Ensure creation has required attributes
    if 'uri' not in creation or '_id' not in creation:
        raise ValueError("The provided creation is missing required attributes.")
    
    response = requests.get(creation['uri'])
    response.raise_for_status()
    
    # Infer the creation filetype from the response headers
    content_type = response.headers.get('Content-Type')
    if not content_type:
        raise ValueError("Could not determine the creation's content type.")
        
    filetype = content_type.split('/')[-1]
    
    # Construct filename and path
    time_string = time.strftime("%Y-%m-%d-%H:%M:%S")
    creation_savename = f"{time_string}_{creation['_id']}"
    creation_filename = f"{creation_savename}.{filetype}"
    creation_filepath = os.path.join(output_folder, creation_filename)

    # Save the creation to a file
    os.makedirs(output_folder, exist_ok=True)
    with open(creation_filepath, 'wb') as f:
        f.write(response.content)

    # Save the creation metadata to a file:
    creation_config_filename = f"{creation_savename}.json"
    creation_config_filepath = os.path.join(output_folder, creation_config_filename)

    if len(fields_to_add) > 0:
        creation_config.update(fields_to_add)

    with open(creation_config_filepath, 'w') as f:
        json.dump(creation_config, f, indent=4, sort_keys=True)

    print(f"Saved creation to {creation_filepath}")


def create_task(generator_name, config):
    request_payload = {
        "generatorName": generator_name,
        "config": config
    }
    response = requests.post(
        f'{EDEN_API_URL}/tasks/create',
        json=request_payload,
        headers=HEADERS
    )
    
    if response.status_code != 200:
        print("---------- an error occured in the Eden API: ----------")
        raise EdenAPIError(response.text)

    return response.json()['taskId']


def get_task_status(task_id):
    response = requests.get(
        f'{EDEN_API_URL}/tasks/{task_id}',
        headers=HEADERS
    )

    if response.status_code != 200:
        print("---------- an error occured in the Eden API: ----------")
        raise EdenAPIError(response.text)

    task = response.json()['task']
    
    creation_config = None
    if task['status'] == 'completed': # also get the creation config:
        creation_config = task['config']

    return task['status'], task.get('progress', None), task.get('creation', None), creation_config


def run_task(generator_name, 
             config, 
             output_folder = None,  # if specified, save the creation to this folder
             verbose = 1,           # if True, print task status while waiting for completion
             fields_to_add = {},    # if specified, append these fields to the saved creation dict 
             ):
    """Run a task and wait for it to complete. Optionally save the creation to a specified folder."""

    start_time = time.time()
    task_id = create_task(generator_name, config)
    print(f"TASK with ID ==== {task_id} started!")
    
    task_duration = 0
    while task_duration < TIMEOUT:
        status, progress, creation, creation_config = get_task_status(task_id)

        if status == 'completed' and creation:
            print(f"Task completed in {task_duration:.1f} seconds")
            if output_folder:
                save_creation(creation, creation_config, output_folder = output_folder, fields_to_add = fields_to_add)
            if verbose:
                print(creation)
            return creation
        elif status == 'failed':
            print(f"Task failed after {task_duration:.1f} seconds")
            return None
        elif verbose:
            progress_percent_str = f"{(100*progress):.1f}%" if progress else "unknown"
            print(f"Task ID: {task_id}: {status}, progress: {progress_percent_str}, runtime: {task_duration:.1f} seconds")
        
        time.sleep(POLL_INTERVAL)
        task_duration = time.time() - start_time

    print(f"Task timed out after {task_duration:.1f} seconds, returning")

    return None


if __name__ == "__main__":
    
    
    generator_name = "create"
    config = {
            "text_input": "a beautiful clearing in the forest with an alien glass orb floating in the air, high quality professional photography, nikon d850 50mm",
            "guidance_scale": 8,
            "width": 1024,
            "height": 1024,
            "n_samples": 1,
            "steps": 35,
            "upscale_f": 1.0,
        }
    
    time_string = time.strftime("%Y-%m-%d")
    creation = run_task(generator_name, config, output_folder="eden_creations_" + time_string)