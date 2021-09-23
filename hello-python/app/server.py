from flask import Flask, render_template, url_for, jsonify, request, redirect
from flask.wrappers import Response
import person_group_operations,person_operations,person_face_operations
import uuid

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/persongroups/create', methods=['POST','GET'])
def create_person_group_route():
    if(request.method == 'POST'):
        data = {"name":request.form["name"]}
        res =  person_group_operations.create_person_group(str(uuid.uuid4()),data)
        print(res)
        return render_template("personGroupForm.html",message=res)
    else:
        return render_template("personGroupForm.html")
        
    

@app.route('/persongroups/get', methods=['GET'])
def get_person_group(persongroupid):
    data = request.get_json()
    # return person_group_operations.get_person_group(persongroupid)
    return render_template("personGroupCreate.html")

@app.route('/persongroups/<string:persongroupid>', methods=['PATCH'])
def update_person_group_route(persongroupid):
    data = request.get_json()
    return person_group_operations.update_person_group(persongroupid,request.get_json())

@app.route('/persongroups/all', methods=['GET'])
def get_all_person_groups_route():
    personGroupList = person_group_operations.get_all_person_groups()
    return render_template("personGroupAll.html", personGroupList=personGroupList)

@app.route('/persongroups/person/add', methods=['POST','GET'])
def create_person_route():
    if(request.method == 'POST'):
        selectedPersonGroup = request.form["persongroups"]
        data = {"name":request.form["name"]}
        print(selectedPersonGroup)
        res =  person_operations.add_person(selectedPersonGroup,data)
        personGroupList = person_group_operations.get_all_person_groups()
        return render_template("personAdd.html",personGroupList=personGroupList,message=res)
    else:
        personGroupList = person_group_operations.get_all_person_groups()
        return render_template("personAdd.html",personGroupList=personGroupList)

@app.route('/persongroups/person/all', methods=['POST','GET'])
def get_all_persons_route():
    if(request.method == 'POST'):
        selectedPersonGroup = request.form["persongroups"]
        print(selectedPersonGroup)
        res =  person_operations.get_all_persons(selectedPersonGroup)
        print(res)
        personGroupList = person_group_operations.get_all_person_groups()
        return render_template("personAll.html",personList=res,personGroupList=personGroupList,message=res)
    else:
        personGroupList = person_group_operations.get_all_person_groups()
        return render_template("personAll.html",personGroupList=personGroupList) 

@app.route('/persongroups/person/addface', methods=['POST','GET'])
def add_person_face_route():
    if(request.method == 'POST'):
        selectedPersonGroup = request.form["persongroups"]
        print(selectedPersonGroup)
        res =  person_operations.get_all_persons(selectedPersonGroup)
        print(res)
        personGroupList = person_group_operations.get_all_person_groups()
        return redirect(url_for("add_person_face_form_route",selectedPersonGroup=selectedPersonGroup))
    else:
        personGroupList = person_group_operations.get_all_person_groups()
        return render_template("personFace.html",personGroupList=personGroupList,btn="Get Persons")

@app.route('/persongroups/person/addface/<selectedPersonGroup>', methods=['POST','GET'])
def add_person_face_form_route(selectedPersonGroup):
    if(request.method == 'POST'):
        selectedPerson = request.form["persons"]
        body = {"url":request.form["url"]}
        response = person_face_operations.create_person_face(selectedPersonGroup,selectedPerson,body)
        return render_template("personFaceSubmit.html",message=response,btn="Add Face")
    else:
        personGroupList = person_group_operations.get_all_person_groups()
        personList =  person_operations.get_all_persons(selectedPersonGroup)
        print(personList)
        return render_template("personFaceForm.html",personGroupList=personGroupList,personList=personList,btn="Add Face",selectedGroupId=selectedPersonGroup)

@app.route('/persongroups/train', methods=['POST','GET'])
def train_person_group_route():
    if(request.method == 'POST'):
        selectedPersonGroup = request.form["persongroups"]
        res = person_group_operations.train_person_group(selectedPersonGroup)
        personGroupList = person_group_operations.get_all_person_groups()
        return render_template("personGroupTrain.html",personGroupList=personGroupList,message=res)
    else:
        personGroupList = person_group_operations.get_all_person_groups()
        return render_template("personGroupTrain.html",personGroupList=personGroupList)

@app.route('/persongroups/training', methods=['POST','GET'])
def person_group_training_status_route():
    if(request.method == 'POST'):
        selectedPersonGroup = request.form["persongroups"]
        res = person_group_operations.get_person_group_training_status(selectedPersonGroup)
        personGroupList = person_group_operations.get_all_person_groups()
        return render_template("personGroupTrainingStatus.html",personGroupList=personGroupList,message=res,selectedGroupId=selectedPersonGroup)
    else:
        personGroupList = person_group_operations.get_all_person_groups()
        return render_template("personGroupTrainingStatus.html",personGroupList=personGroupList)

@app.route('/identify', methods=['POST','GET'])
def person_identify():
    if(request.method == 'POST'):
        selectedPersonGroup = request.form["persongroups"]
        image_url = request.form["url"]
        res = person_face_operations.identify(image_url,selectedPersonGroup)
        personGroupList = person_group_operations.get_all_person_groups()
        if(type(res)==list):
            for j in res:
                if(len(j["candidates"])>0):
                    person_name = person_operations.get_person(selectedPersonGroup,j['candidates'][0]['personId'])
                    j["candidates"][0]["name"] = person_name["name"]
            return render_template("personIdentify.html",identifiedPersonList=res,personGroupList=personGroupList)
        return render_template("personIdentify.html",message=res,personGroupList=personGroupList)
    else:
        personGroupList = person_group_operations.get_all_person_groups()
        return render_template("personIdentify.html",personGroupList=personGroupList)

if __name__ == "__main__":
    #app.run(host="0.0.0.0",port = 8000,debug=True)
    app.run(host="0.0.0.0")