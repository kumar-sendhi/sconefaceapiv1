import os,requests

headers = {
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': os.environ.get("API_KEY"),
}

def create_person_face(selectedPersonGroup,selectedPersonId,body):
    constructed_url = os.environ.get("BASE_URL") + "/persongroups/" + selectedPersonGroup + "/persons/" +selectedPersonId+"/persistedFaces"
    response = requests.post(constructed_url,headers=headers,json=body)
    if(response.status_code == 200):
        return f"Face Added to {selectedPersonId}"
    else:
        return f"Error : {response.json()}"

def identify(url,selectedPersonGroup):
    detect_url = os.environ.get("BASE_URL")+"/detect"
    detect_body = {"url":url}
    detect_response = requests.post(detect_url,headers=headers,json=detect_body)
    if(detect_response.status_code == 200):
        identify_url = os.environ.get("BASE_URL")+"/identify"
        face_ids = [i["faceId"] for i in detect_response.json()]
        identify_body = {"personGroupId":selectedPersonGroup,"faceIds":face_ids}
        identify_response = requests.post(identify_url,headers=headers,json=identify_body)
        print(identify_response.json())
        # if(identify_response.status_code == 200):
            # for j in identify_response.json():
            #     if(len(j["candidates"])>0):
            #         return f"Identified person with confidence {j['candidates'][0]['confidence']}"
            # return f"Could not Identify"
        return identify_response.json()
    return detect_response.json()

