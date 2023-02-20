import requests
import time


EDEN_API_URL = "https://api.eden.art"

# header expects format. Load from .env
# header = {
#    "x-api-key": "YOUR_API_KEY",
#    "x-api-secret": "YOUR_API_SECRET"
#}

# geneneratorName = "create" or other ones

# confif has parameters like this, see Eden docs
#config = {
#    "text_input": "i am a dog"
#}

# local or server-side code for Eden post request
def run_task(generatorName, config, header):
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


