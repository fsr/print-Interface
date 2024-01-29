import imaplib
import email
import shutil
from email.header import decode_header
import os
from print_interface.emailObject import Email


def clean(text):
    # clean text for creating a folder
    return "".join(c if c.isalnum() else "_" for c in text)


class EmailService:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.number = 3
        self.imap_server = "mail.ifsr.de"

    def receive_new_emails(self) -> list:
        self.clear_dir()
        list_of_email = []
        status, messages = self.imap.select("INBOX")
        # number of top emails to fetch
        N = self.number
        # total number of emails
        messages = int(messages[0])
        for i in range(messages, messages - N, -1):
            From = str()
            subject = str()
            filenames = []
            # fetch the email message by ID
            try:
                res, msg = self.imap.fetch(str(i), "(RFC822)")
            except imaplib.IMAP4.error:
                continue
            for response in msg:
                if isinstance(response, tuple):
                    # parse a bytes email into a message object
                    msg = email.message_from_bytes(response[1])
                    # decode the email subject
                    try:
                        subject, encoding = decode_header(msg["Subject"])[0]
                        if isinstance(subject, bytes):
                            # if it's a bytes, decode to str
                            try:
                                subject = subject.decode(encoding)
                            except TypeError:
                                subject = ""
                    except TypeError:
                        subject = ""
                    # decode email sender
                    From, encoding = decode_header(msg.get("From"))[0]
                    if isinstance(From, bytes):
                        From = From.decode(encoding)
                    # if the email message is multipart
                    if msg.is_multipart():
                        # iterate over email parts
                        for part in msg.walk():
                            # extract content type of email
                            content_disposition = str(part.get("Content-Disposition"))
                            if "attachment" in content_disposition:
                                # download attachment
                                filename = part.get_filename().strip()
                                if filename:
                                    if ".pdf" in filename:
                                        folder_name = os.getcwd() + "/files"
                                        if not os.path.isdir(folder_name):
                                            # make a folder for this email (named after the subject)
                                            os.mkdir(folder_name)
                                        filepath = os.path.join(folder_name, filename)
                                        # download attachment and save it
                                        open(filepath, "wb").write(part.get_payload(decode=True))
                                        filenames.append(filename)
            list_of_email.append(Email(From, subject, filenames))
        return list_of_email

    def login(self):
        self.imap = imaplib.IMAP4_SSL(self.imap_server)
        self.imap.login(self.username, self.password)

    def logout(self):
        self.imap.logout()

    def clear_dir(self):
        if os.path.exists(os.getcwd() + '/files'):
            shutil.rmtree(os.getcwd() + '/files')
