import os,requests

headers = {
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': os.environ.get("API_KEY"),
}

def add_person(selectedPersonGroup,body):
    constructed_url = os.environ.get("BASE_URL") + "/persongroups/" + selectedPersonGroup + "/persons"
    response = requests.post(constructed_url,headers=headers,json=body)
    if(response.status_code == 200):
        return f"Person Added to {selectedPersonGroup}"
    else:
        return f"Error : {response.json()}"

def get_person(selectedPersonGroup,personId):
    constructed_url = os.environ.get("BASE_URL") + "/persongroups/" + selectedPersonGroup + "/persons/" + personId
    response = requests.get(constructed_url,headers=headers)
    return response.json()


def get_all_persons(selectedPersonGroup):
    constructed_url = os.environ.get("BASE_URL") + "/persongroups/" + selectedPersonGroup + "/persons"
    response = requests.get(constructed_url,headers=headers)
    return response.json()
