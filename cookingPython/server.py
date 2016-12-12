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
DEFAULT = "8bd3b6024a8e461f8e4e63c181882295"
CHICKEN = "3e46239a1f334a378ee7a212f590010f"
BREAD = "1b47e65f9fee42d0be30b00a42673ddf"
SESSION = "0"
COUNTER = "0"
@app.route('/favicon.ico')
def sam():
    return True

def call_ai(client_access_token,user_input):
    try:
        ai = apiai.ApiAI(client_access_token)
        request = ai.text_request()
        request.query = user_input
        response = request.getresponse()
        output = json.loads(response.read())['result']
        output_speech = output["fulfillment"]["speech"]
        intent_name = output["metadata"]["intentName"]
    except (RuntimeError,TypeError,NameError):
        pass
    return [output_speech,intent_name]

def basic(user_input):
    global DEFAULT, CHICKEN, BREAD, SESSION, COUNTER
    [output_speech,intent_name] = call_ai(DEFAULT,user_input)
    if "chicken" in output_speech:
        SESSION = "1"
        COUNTER = "0"
    elif "bread" in output_speech:
        SESSION = "2"
        COUNTER = "0"
    if intent_name == "NextSteps":
        step_no = int(COUNTER) + 1
        COUNTER = str(step_no)
        print "session: " + SESSION
        if (SESSION == "1"):
            client_access_token = CHICKEN
        elif (SESSION == "2"):
            client_access_token = BREAD
        user_input = "Step "+str(step_no)
        [output_speech,intent_name] = call_ai(client_access_token,user_input)
        return output_speech
    return output_speech

@app.route('/',methods = ['POST'])
def index():
    data = request.data
    print data
    output_speech = basic(data)
    return output_speech

if __name__ == '__main__':
    app.debug = True
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
