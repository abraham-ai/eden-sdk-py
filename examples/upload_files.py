import requests
import os
from dotenv import load_dotenv

EDEN_API_URL = "https://api.eden.art"

# upload to eden for generators that require URLs
def upload_file(file_path):
    # form header from env
    header = {
        "x-api-key": os.getenv('EDEN_API_KEY'),
        "x-api-secret": os.getenv('EDEN_API_SECRET')
    }

    with open(file_path, "rb") as file:
        media = file.read()
        filename = os.path.basename(file_path)
        fileType = filename.split(".")[-1]
        print(fileType)
        files = {"media": (filename, media)}
        response = requests.post(EDEN_API_URL + "/media/upload/?fileType=${fileType}", files=files, headers=header)
        return response.json()


load_dotenv()
result = upload_file("assets/test.jpg")
print(result)
uploaded_url = result['url']
print(uploaded_url)

