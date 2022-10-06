import base64
from auth.service import service_gmail
from flask import jsonify
from email.message import EmailMessage
from googleapiclient.errors import HttpError
from users.messages import utility, read


def send(request):
    message = {}
    try:
        if 'files' not in request.files:
            resp = jsonify({'message': 'No file part in the request'})
            resp.status_code = 400
            return resp

        mimeMessage = EmailMessage()
        mimeMessage['To'] = request.form['toemail']
        mimeMessage['Subject'] = request.form['subject']
        mimeMessage['From'] = 'testing@tutorshive.com'
        mimeMessage.set_content(request.form['emailMsg'])
        file_attachments = request.files.getlist('files')
        mimeMessage = utility.add_attachment(file_attachments, mimeMessage)

        if request.form['msgID']!='' and request.form['threadID']!='':
            response = read.get_email_message(request.form['msgID'])
            msgId = format(response['Message-ID'])
            mimeMessage.add_header('Reference', msgId)
            mimeMessage.add_header('In-Reply-To', format(response['In-Reply-To']))
            raw_string = {'raw': base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode(),
                          "threadID": request.form["threadID"]}
        else:
            raw_string = {'raw': base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()}

        message = service_gmail.users().messages().send(userId='me', body=raw_string).execute()
        print(message)
    except HttpError as error:
        print(F'An error occurred: {error}')
        message = None
    except Exception as e:
        print(e)
    return message
