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

@app.route('/favicon.ico')
def sam():
    return True


def basic(user_input):
    f = open('clienttoken', 'r+')
    r = open('logfile','a')
    client_access_token = f.read()
    ui = '"hello"'
    user_input = (str(user_input))
    if str(user_input) == ui:
        client_access_token = "8bd3b6024a8e461f8e4e63c181882295"
        f.seek(0,0)
        f.write(client_access_token)
    ai = apiai.ApiAI(client_access_token)
    request = ai.text_request()
    # request.lang = 'en'  # optional, default value equal 'en'
    # request.session_id = "unique"
    request.query = user_input
    r.write("User:"+user_input+"\n")
    response = request.getresponse()
    output = json.loads(response.read())['result']
    output_speech = output["fulfillment"]["speech"]
    r.write("System:"+output_speech+"\n")
    print output_speech
    intent_name = output["metadata"]["intentName"]
    if "chicken" in output_speech:
        client_access_token = "3e46239a1f334a378ee7a212f590010f"
        f.seek(0,0)
        a = f.tell()
        print a
        f.write(client_access_token)
    elif "bread" in output_speech:
        client_access_token = "1b47e65f9fee42d0be30b00a42673ddf"
        f.seek(0, 0)
        f.write(client_access_token)
    f.close()
    print output_speech
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
