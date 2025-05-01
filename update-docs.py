import requests
from datetime import datetime
import os
import argparse

parser = argparse.ArgumentParser(description="Upload a file to Azure Blob Storage using REST API.")
parser.add_argument("--sas-token", required=True, help="SAS token for authentication")
args = parser.parse_args()

storage_account = "asadocs"
container_name = "docs"
object_type = "blob"
blob_name = "docs.html"
local_file_path = "C:/code/azure-storage-automation/docs.html" 
sas_token = args.sas_token  

url = f"https://{storage_account}.{object_type}.core.windows.net/{container_name}/{blob_name}{sas_token}"

headers = {
    "x-ms-blob-type": "BlockBlob",  
    "x-ms-date": datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT"),  
    "Content-Type": "text/html"  
}

try:
    with open(local_file_path, "rb") as file:
        file_content = file.read()
except FileNotFoundError:
    print(f"Error: File '{local_file_path}' not found. Please check the file path.")
    exit(1)

response = requests.put(url, headers=headers, data=file_content)

if response.status_code == 201:
    print(f"Successfully uploaded '{blob_name}' to container '{container_name}' in account '{storage_account}'.")
else:
    print(f"Failed to upload '{blob_name}'. Status code: {response.status_code}")
    print(f"Error message: {response.text}")