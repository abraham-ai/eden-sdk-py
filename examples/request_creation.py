import requests
import time

# args = https://github.com/abraham-ai/eden-api/blob/main/mongo-init.js

EDEN_API_URL = "https://api.eden.art"

header = {
    "x-api-key": "YOUR_API_KEY",
    "x-api-secret": "YOUR_API_SECRET"
}


def run_task(generatorName, config):
    request = {
        "generatorName": generatorName,
        "config": config
    }

    response = requests.post(
        f'{EDEN_API_URL}/user/create', 
        json=request, 
        headers=header
    )

    if response.status_code != 200:
        print(response.text)
        return None
    
    result = response.json()
    taskId = result['taskId']

    while True:
        response = requests.post(
            f'{EDEN_API_URL}/user/tasks', 
            json={"taskIds": [taskId]},
            headers=header
        )

        if response.status_code != 200:
            print(response.text)
            return None

        result = response.json()
        task = result['tasks'][0]
        status = task['status']

        if status == 'completed':
            return task
        elif status == 'failed':
            print("FAILED!")
            return None

        time.sleep(1)



config = {
    "text_input": "i am a dog"
}

result = run_task("create", config)

output_url = result['output'][-1]
print(output_url)
  
