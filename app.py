import json

import flask
from flask import Flask, request
from flask_cors import CORS


from users.messages import send, draft, read
from users.profile import profile
from flask import jsonify

app = Flask(__name__)

CLIENT_SECRET_FILE = '/Users/roshnijalan/Personal/gmail/client_secret.json'
API_NAME = 'gmail'
API_VERSION = 'v1'
SCOPES = ['https://mail.google.com/']

global_email_id_mapping = {}
CORS(app)

# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# app.config['MAX_CONTENT_LENGTH'] = 35 * 1024

@app.route('/create_draft', methods=['POST'])
def create_draft():
    response = draft.create_draft(request)
    if response['id']:
        return "Draft saved successfully!!"
    else:
        return "There is an error while saving the draft. Please try again"


@app.route('/send_email', methods=['POST'])
def send_email():
    print(request.data)
    # body = request.data.decode('utf8').replace("'", '"')
    # print(body)
    # body = json.loads(body)
    response = send.send(request)
    print(response)
    if response['id'] and response['threadId'] and response['labelIds']:
        return "Email sent successfully"
    else:
        return "There is an error while sending the email. Please try again"


@app.route('/get_user')
def get_user():
    response = profile.getprofile()
    print(response)
    return json.dumps(response)


@app.route('/get_emails', methods=['GET'])
def get_emails():
    response = read.get_emails(global_email_id_mapping)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Content-Type'] = "application/json"
    response.headers['Access-Control-Allow-Credentials']='true'

    return response


@app.route('/get_emails_by_id')
def get_emails_by_id():
    response = read.get_email_message(request.args.get('msgId'))
    print(response.keys())
    return response['To'] + '    ' + response['Message-ID'] + '    ' + response['Subject']


@app.route('/')
def hello():
    return "Welcome to Gmail Integration"


if __name__ == '__main__':
    app.run(host="localhost", port=7000, debug=True)
