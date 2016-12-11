__author__ = 'hemalatha_ganireddy'

import os
from flask import Flask
from flask import request
import sys

import main
import os.path
import json
try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai

app = Flask(__name__)
os.environ["DEFAULT"] = "8bd3b6024a8e461f8e4e63c181882295"
os.environ["CHICKEN"] = "3e46239a1f334a378ee7a212f590010f"
os.environ["BREAD"] = "1b47e65f9fee42d0be30b00a42673ddf"
os.environ["SESSION"] = "0"
os.environ["COUNTER"] = "0"
@app.route('/favicon.ico')
def sam():
    return True

def call_ai(client_access_token,user_input):
    ai = apiai.ApiAI(client_access_token)
    request = ai.text_request()
    request.query = user_input
    response = request.getresponse()
    output = json.loads(response.read())['result']
    output_speech = output["fulfillment"]["speech"]
    intent_name = output["metadata"]["intentName"]
    return [output_speech,intent_name]

def basic(user_input):
    [output_speech,intent_name] = call_ai(os.environ["DEFAULT"],user_input)
    if "chicken" in output_speech:
        os.environ["SESSION"] = "1"
        os.environ["COUNTER"] = "0"
    elif "bread" in output_speech:
        os.environ["SESSION"] = "2"
        os.environ["COUNTER"] = "0"
    if intent_name == "NextSteps":
        step_no = int(os.environ["COUNTER"]) + 1
        os.environ["COUNTER"] = str(step_no)
        if (os.environ["SESSION"] == "1"):
            client_access_token = os.environ["CHICKEN"]
        elif (os.environ["SESSION"] == "2"):
            client_access_token = os.environ["BREAD"]
        user_input = "Step "+str(step_no)
        [output_speech,intent_name] = call_ai(client_access_token,user_input)
        return output_speech
    return output_speech

@app.route('/',methods = ['POST'])
def index():
    data = request.form['data']
    print data
    output_speech = basic(data)
    return output_speech

if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
