import requests
import json

def upload_file(file_name, content, auth_token):
    url = "http://localhost:3001/api/v1/document/raw-text"

    payload = json.dumps({
        "textContent": f"{content}",
        "metadata": {
            "title": file_name
        }
    })
    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 200:
        print("File uploaded successfully.")
        return response.json()["documents"][0]["location"]
    else:
        print(f"Failed to upload file: {response.text}")
        return None

def move_to_workspace(workspace_name, location):
    url = "http://localhost:3001/api/v1/workspace/nlp/update-embeddings"

    payload = json.dumps({
        "adds": [location],
        "deletes": []
    })

    headers = {
        'Authorization': f'Bearer {auth_token}',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 200:
        print("Move to workspace successfully.")
    else:
        print("Failed to move file to workspace")

if __name__ == "__main__":
    # Prompt user for website URL and authentication token
    # KHV13QM-W24MKZN-QATD8WF-DTK8DDJ
    auth_token = input("Enter the Authorization token: ")
    workspace_name = 'nlp'

    # Open the file and read the content
    file_name = 'document.txt'
    with open(file_name, 'r', encoding='utf-8') as file:
        file_content = file.read()
        # Call the upload_file function to upload the scraped content
        location = upload_file(file_name, file_content, auth_token)
        if location is not None:
            move_to_workspace(workspace_name, location)