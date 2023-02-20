import os
from dotenv import load_dotenv

import request_creation


# some simple wrappers
def renderCreate(prompt):
        # form header from env
        header = {
            "x-api-key": os.getenv('EDEN_API_KEY'),
            "x-api-secret": os.getenv('EDEN_API_SECRET')
        }

        # add other variables here, for example steps
        config = {
            "text_input": prompt,
            "steps": 50
        }

        result = request_creation.run_task("create", config, header)
        
        printResult(result)
        
        # return whatever data we decide, for example our output URL
        output_url = result['output']['file']
        return output_url

def renderTTS(text):
        # form header from env
        header = {
            "x-api-key": os.getenv('EDEN_API_KEY'),
            "x-api-secret": os.getenv('EDEN_API_SECRET')
        }

        # add other variables here, for example steps
        config = {
            "text": text,
        }

        result = request_creation.run_task("tts", config, header)
        
        printResult(result)
        
        # return whatever data we decide, for example our output URL
        output_url = result['output']['file']
        return output_url

# some simple wrappers
def renderInterpolate(lerpList):
        # form header from env
        header = {
            "x-api-key": os.getenv('EDEN_API_KEY'),
            "x-api-secret": os.getenv('EDEN_API_SECRET')
        }

        # add other variables here, for example steps
        config = {
            "interpolation_texts": lerpList,
        }

        result = request_creation.run_task("interpolate", config, header)
        
        printResult(result)
        
        # return whatever data we decide, for example our output URL
        output_url = result['output']['file']
        return output_url


def printResult(result):
    # all results
    print("-- RESULT ---")
    print(result)

    # show seed, other config vars like this, helpful for determining config params
    print("-- SEED ---")
    seed = result['config']['seed']
    print("seed = " + str(seed))

    print("-- RESULT [output] ---")
    print(result['output'])

    print("-- RESULT [output]['file'] ---")
    print(result['output']['file'])

# load .env variables
load_dotenv()

# tests — from render.py
#renderCreate("unicorn, cat, dog, rainbows")

lerpList = ["cat grinning", "dog jumping"]
renderInterpolate(lerpList)

#renderTTS("help, I am stuck in the void. Please lend me a hand.")

