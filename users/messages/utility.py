import os
from werkzeug.utils import secure_filename
import mimetypes

ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

UPLOAD_FOLDER = '/Users/roshnijalan/Personal/gmail/upload_files'
MAX_CONTENT_LENGTH = 35 * 1024


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def add_attachment(file_attachments, mimeMessage):
    # Attach files
    for attachment in file_attachments:
        if attachment and allowed_file(attachment.filename):
            filename = secure_filename(attachment.filename)
        content_type, encoding = mimetypes.guess_type(filename)
        main_type, sub_type = content_type.split('/')
        file_name = os.path.basename(filename)
        attachment.save(os.path.join(UPLOAD_FOLDER, filename))

        with open(os.path.join(UPLOAD_FOLDER, filename), 'rb') as fp:
            attachment_data = fp.read()
        mimeMessage.add_attachment(attachment_data, main_type, sub_type, filename= file_name)
    return mimeMessage
