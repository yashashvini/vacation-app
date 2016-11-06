__author__ = 'hemalatha_ganireddy'
import os.path
import sys
import json
try:
    import apiai
except ImportError:
    sys.path.append(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), os.pardir)
    )
    import apiai
# CLIENT_ACCESS_TOKEN = 'YOUR_ACCESS_TOKEN'
CLIENT_ACCESS_TOKEN = '7853febc373644728bc5d5f9e6d0282d'

def main():
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)
    request = ai.text_request()
    # request.lang = 'en'  # optional, default value equal 'en'
    # request.session_id = "<SESSION ID, UNIQUE FOR EACH USER>"
    request.query = "i would like to have lunch"
    response = request.getresponse()
    # print json.loads(response.read())['status']['metadata']
    print json.loads(response.read())['result']['metadata']
    return response.read()


if __name__ == '__main__':
    main()
