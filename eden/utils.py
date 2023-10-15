import os
import requests
import time
import io
import PIL.Image
import json
import eden


def http_request(method, endpoint, data=None):
    if eden.api_key is None or eden.api_secret is None:
        raise ValueError("API key and secret must be set")
    headers = {
        "x-api-key": eden.api_key,
        "x-api-secret": eden.api_secret
    }
    if method == "GET":
        response = requests.get(eden.api_url + endpoint, headers=headers)
    elif method == "POST":
        response = requests.post(eden.api_url + endpoint, json=data, headers=headers)
    else:
        raise ValueError("Invalid method")
    if response.status_code != 200:
        raise eden.EdenTaskFailedError(response.text)
    return response.json()


def get(endpoint):
    return http_request("GET", endpoint)


def post(endpoint, data):
    return http_request("POST", endpoint, data)


def download_to_pil(creation):
    """Download and convert to PIL"""
    
    # Ensure creation has required attributes
    if 'uri' not in creation or '_id' not in creation:
        raise ValueError("The provided creation is missing required attributes.")
    
    response = requests.get(creation['uri'])
    response.raise_for_status()
    
    content = io.BytesIO(response.content)
    image = PIL.Image.open(content)
    return image


def save_creation(creation, creation_config, output_folder="eden_creations", fields_to_add = {}):
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

