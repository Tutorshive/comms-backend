import base64
from auth.service import service_gmail
from email.message import EmailMessage
from googleapiclient.errors import HttpError
from users.messages import utility

def create_draft(request):
    try:
        mimeMessage = EmailMessage()
        mimeMessage['To'] = request.form['toemail']
        mimeMessage['Subject'] = request.form['subject']
        mimeMessage['From'] = 'testing@tutorshive.com'
        mimeMessage.set_content(request.form['draftMsg'])

        file_attachments = request.files.getlist('files')
        mimeMessage = utility.add_attachment(file_attachments, mimeMessage)

        # encoded message
        encoded_message = base64.urlsafe_b64encode(mimeMessage.as_bytes()).decode()


        create_message = {
            'message': {
                'raw': encoded_message
            }
        }
        draft = service_gmail.users().drafts().create(userId="me",
                                                body=create_message).execute()

        print(F'Draft id: {draft["id"]}\nDraft message: {draft["message"]}')

    except HttpError as error:
        print(F'An error occurred: {error}')
        draft = None
    print(draft)
    return draft
