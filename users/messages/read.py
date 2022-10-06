import base64
import email
import json
from flask import jsonify

from googleapiclient.errors import HttpError
from auth.service import service_gmail


def get_emails(global_email_id_mapping):
    try:
        message = service_gmail.users().messages().list(userId='me').execute()
        message_detail = []
        for msg in message["messages"]:
            resp = get_email_message(msg["id"])
            email_single = {}
            size = message_detail.__sizeof__();
            email_single["id"] = size
            for k, v in resp.items():
                print(k)
                print(v)
                if k == 'From':
                    if v not in global_email_id_mapping.keys():
                        global_email_id_mapping[v] = hash(v)
                    # v = global_email_id_mapping[v]
                    email_single["company"] = global_email_id_mapping[v]
                if k == 'Subject':
                    email_single["Title"] = v
                if k == 'Message-ID':
                    email_single["dummy"] = get_email_message(v)
            message_detail.append(email_single)
            print(email_single)

        return jsonify({"emails": message_detail})
    except HttpError as error:
        print('An error occurred: %s' % error)


def get_email_message(msg_id):
    try:
        print('Phani')
        print(msg_id)
        message = service_gmail.users().messages().get(userId='me', id=msg_id,
                                                       format='raw').execute()

        msg_str = base64.urlsafe_b64decode(message['raw']).decode()

        mime_msg = email.message_from_string(msg_str)

        return mime_msg
    except HttpError as error:
        print('An error occurred: %s' % error)
