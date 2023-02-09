import requests
import os


EDEN_API_URL = "https://api.eden.art"

header = {
    "x-api-key": "YOUR_API_KEY",
    "x-api-secret": "YOUR_API_SECRET"
}

def upload_file(file_path):
    with open(file_path, "rb") as file:
        media = file.read()
        filename = os.path.basename(file_path)
        files = {"media": (filename, media)}
        response = requests.post(EDEN_API_URL + "/media/upload", files=files, headers=header)
        return response.json()


result = upload_file("assets/test.jpg")

uploaded_url = result['url']

print(uploaded_url)