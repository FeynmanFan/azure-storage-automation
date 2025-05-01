import requests
from datetime import datetime
import os
import argparse

api_version = "2023-08-03"

def upload_file(url, local_file_path, id):
    try:
        with open(local_file_path, "rb") as file:
            file_content = file.read()
    except FileNotFoundError:
        print(f"Error: File '{local_file_path}' not found. Please check the file path.")
        exit(1)

    file_size = os.path.getsize(local_file_path)

    create_headers = {
        "x-ms-type": "file",
        "x-ms-content-length": str(file_size),
        "x-ms-version": api_version,
        "x-ms-date": datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
    }

    response_create = requests.put(url, headers=create_headers)
    response_create.raise_for_status()

    write_headers = {
        "x-ms-write": "update",
        "x-ms-range": f"bytes=0-{str(file_size - 1)}",
        "x-ms-version": api_version,
        "Content-Length": str(file_size),
        "Content-Type": "application/json"
    }
    
    params = {"comp": "range"}
    response_put_range = requests.put(url, headers=write_headers, params=params, data=file_content)
    response_put_range.raise_for_status()

parser = argparse.ArgumentParser(description="Upload a file to Azure File Storage using REST API.")
parser.add_argument("--sas-token", required=True, help="SAS token for authentication")
parser.add_argument("--command", required=True, help="Command to execute")
parser.add_argument("--folder", required=True, help="Folder to modify")
parser.add_argument("--id", required=True, help="Id of the object")

args = parser.parse_args()

storage_account = "cbbgamedb"
id = args.id
folder = args.folder
local_file_path = f"C:/code/azure-storage-automation/cbbgamedb/{folder}/{id}.json" 
sas_token = args.sas_token  
command = args.command.lower()

url = f"https://{storage_account}.file.core.windows.net/{folder}/{id}.json?{sas_token}"

headers = {
    "x-ms-type": "file",
    "x-ms-version": api_version
}

match command:
    case "read":
        print(requests.get(url, headers=headers).text)
        exit
    case "create":
        upload_file(url, local_file_path, id)
        exit
    case "update":
        upload_file(url, local_file_path, id)
        exit
    case "delete": 
        response = requests.delete(url, headers=headers)
        exit
    case _:
        raise NotImplementedError(f"Command '{command}' not implemented")