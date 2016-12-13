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
BANANA = "7311a3e6dab74b8a835570d2a2f92430"
EGG = "8d1cc93d1d4f44459816d5fcf97f80e9"
SALMON = "4c8edbcbc28c40cba32bea78425064b2"
STRAWBERRY = "1ba05eed40cc479ea53a1a74016f43bd"
SESSION = 0
COUNTER = 0
SET = 0
@app.route('/favicon.ico')
def sam():
    return True

def call_ai(client_access_token,user_input):
    try:
        ai = apiai.ApiAI(client_access_token)
        request = ai.text_request()
        request.query = user_input
        request.resetContexts = True
        response = request.getresponse()
        output = json.loads(response.read())['result']
        print output
        output_speech = output["fulfillment"]["speech"]
        intent_name = output["metadata"]["intentName"]
    except (RuntimeError,TypeError,NameError):
        pass
    return [output_speech,intent_name]

def get_client_access_token(session):
    if session == 1:
        client_access_token = CHICKEN
    elif session == 2:
        client_access_token = BREAD
    elif session == 3:
        client_access_token = BANANA
    elif session == 4:
        client_access_token = EGG
    elif session == 5:
        client_access_token = SALMON
    elif session == 6:
        client_access_token = STRAWBERRY
    return client_access_token

def basic(user_input):
    fp = open('logfile','a')
    fp.write("User:"+user_input)
    global DEFAULT, CHICKEN, BREAD, SESSION, COUNTER,SET
    [output_speech,intent_name] = call_ai(DEFAULT,user_input)
    if intent_name == "Greetings":
        SESSION = 0
        COUNTER = 0
    if "Okay,let's start cooking" in output_speech:
        if ("chicken" in output_speech) or ("sandwich" in output_speech):
            output_speech = "Okay! Let's start cooking chicken sandwich.Say ready when you are ready to start cooking."
            SESSION = 1
            COUNTER = 0
        elif ("bread" in output_speech) or ("toast" in output_speech):
            output_speech = "Okay! Let's start cooking bread toast.Say ready when you are ready to start cooking."
            SESSION = 2
            COUNTER = 0
        elif ("banana" in output_speech) or ("pudding" in output_speech):
            output_speech = "Okay! Let's start cooking banana pudding.Say ready when you are ready to start cooking."
            SESSION = 3
            COUNTER = 0
        elif ("egg" in output_speech) or ("fried" in output_speech) or ("rice" in output_speech):
            output_speech = "Okay! Let's start cooking egg fried rice.Say ready when you are ready to start cooking."
            SESSION = 4
            COUNTER = 0
        elif ("grilled" in output_speech) or ("salmon" in output_speech):
            output_speech = "Okay! Let's start cooking grilled salmon.Say ready when you are ready to start cooking."
            SESSION = 5
            COUNTER = 0
        elif ("strawberry" in output_speech) or ("pie" in output_speech):
            output_speech = "Okay! Let's start cooking strawberry pie.Say ready when you are ready to start cooking."
            SESSION = 6
            COUNTER = 0
    if (intent_name == 'Default Fallback Intent') and (SESSION!=0):
        output_speech = "Sorry I didn't understand what you are trying to say!Please say repeat to repeat the current recipe" \
                        " or next for the next step or previous for the previous step or exit to return to menu"
        fp.write("System:" + output_speech)
        fp.close()
        return output_speech
    if (intent_name == 'Somethingelse-no') and (SESSION!=0):
        output_speech = "Ok.Would you like to cook something?"
        fp.write("System:" + output_speech)
        fp.close()
        return output_speech

    if (intent_name == "NextSteps") and (SESSION!=0):
        step_no = COUNTER + 1
        COUNTER = step_no
        client_access_token = get_client_access_token(SESSION)
        user_input = "step"+str(step_no)
        [output_speech,intent_name] = call_ai(client_access_token,user_input)
        if intent_name == 'Default':
            SESSION = 0
            COUNTER = 0
        fp.write("System:"+output_speech)
        fp.close()
        return output_speech
    elif (intent_name == "PreviousSteps") and (SESSION!=0):
        if (COUNTER > 1):
            step_no = COUNTER - 1
            COUNTER = step_no
        else:
            step_no = COUNTER
        client_access_token = get_client_access_token(SESSION)
        user_input = "step" + str(step_no)
        [output_speech, intent_name] = call_ai(client_access_token, user_input)
        fp.write("System:" + output_speech)
        fp.close()
        return output_speech
    elif (intent_name == "Repeat") and (SESSION!=0):
        step_no = COUNTER
        client_access_token = get_client_access_token(SESSION)
        user_input = "step" + str(step_no)
        [output_speech, intent_name] = call_ai(client_access_token, user_input)
        fp.write("System:" + output_speech)
        fp.close()
        return output_speech
    fp.write("System:"+output_speech)
    fp.close()
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
