from flask import Flask
from flask import request, jsonify
from flask_cors import CORS
from BrainshopChatbotAPI.chatbasics import chatbotsetup, sendmsg
import requests
import json

apiurl = "https://paulstudiosapi.herokuapp.com"
app = Flask(__name__)
CORS(app)

@app.route('/login', methods=['GET'])
def login():
  if 'user' in request.args:
    user = str(request.args['user'])
  else:
    return "Error: No user field provided. Please specify username."
  if 'pass' in request.args:
    passw = str(request.args['pass'])
  else:
    return "Error: No pass field provided. Please specify password."
  
  users = json.loads(requests.get(apiurl + "/customers").text)
  usersdata = [i['name'] for i in users]
  if user in usersdata:
    for name in usersdata:
      if name == user:
        nameofuser = name
  else:
    print("Username not found")
    return "not found user"
  userindex = usersdata.index(nameofuser) + 1
  userdata = json.loads(requests.get(apiurl + "/customers/" + str(userindex)).text)
  userpass = userdata['pass']
  if passw == userpass:
    print("Logged in as " + user)
    return "Success"
  else:
    print("Wrong password")
    return "wrong pass"

@app.route('/register', methods=['GET'])
def register():
  print("Reg request")
  if 'user' in request.args:
    user = str(request.args['user'])
  else:
    return "Error: No user field provided. Please specify username."
  if 'pass' in request.args:
    passw = str(request.args['pass'])
  else:
    return "Error: No pass field provided. Please specify password."
  if 'email' in request.args:
    email = str(request.args['email'])
  else:
    return "Error: No email field provided. Please specify email."
  users = json.loads(requests.get(apiurl + "/customers").text)
  usernames = [i['name'] for i in users]
  useremails = [i['email'] for i in users]
  if user in usernames:
    print("Username already exists.")
    return "same name"
  if email in useremails:
    print("Email already exists.")
    return "same mail"
  rdata = {
        'email': email,
        'name': user,
        'pass': passw,
        'active': 1
  }
  print(rdata)
  response = json.loads(requests.post(apiurl + "/customers", data=rdata).text)
  if response['name'] == user:
    return "Success", 201

@app.route('/talk', methods=['GET'])
def talk():
  if 'msg' in request.args:
    msg = str(request.args['msg'])
  else:
    return "Error: No msg field provided. Please specify the msg."
  if 'uid' in request.args:
    uid = str(request.args['uid'])
    if uid == "":
      return "Error: No uid field provided. Please specify an uid."
  else:
    return "Error: No uid field provided. Please specify an uid."
  chatbotsetup("156099", "4TG9iu82pFOu9XjD", uid)
  ponse = sendmsg(msg)
  print("Input: " + msg)
  print("Output: " + ponse)
  return ponse

@app.route('/', methods=['GET'])
def home():
  print("Homepage Pinged")
  return "Welcome to PaulStudiosAPI for Website"

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)