__author__ = 'hemalatha_ganireddy'

from flask import Flask
from main import main
import json

app = Flask(__name__)

@app.route('/')
def index():
    output =  main()
    json.loads(output)['result']['metadata']['intentName']
    return "Hello, World!"


if __name__ == '__main__':
    app.run(debug=True)
