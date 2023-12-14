import imaplib
import email
from email.header import decode_header
import os
from emailObject import Email


def clean(text):
    # clean text for creating a folder
    return "".join(c if c.isalnum() else "_" for c in text)


class EmailService:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.imap_server = "mail.ifsr.de"
        # create an IMAP4 class with SSL
        self.imap = imaplib.IMAP4_SSL(self.imap_server)
        # authenticate
        self.imap.login(self.username, self.password)

    def receive_new_emails(self) -> []:
        list_of_email = []

        status, messages = self.imap.select("INBOX")
        # number of top emails to fetch
        N = 3
        # total number of emails
        messages = int(messages[0])
        for i in range(messages, messages - N, -1):
            From = str()
            subject = str()
            filenames = []
            # fetch the email message by ID
            res, msg = self.imap.fetch(str(i), "(RFC822)")
            for response in msg:
                if isinstance(response, tuple):
                    # parse a bytes email into a message object
                    msg = email.message_from_bytes(response[1])
                    # decode the email subject
                    subject, encoding = decode_header(msg["Subject"])[0]
                    if isinstance(subject, bytes):
                        # if it's a bytes, decode to str
                        subject = subject.decode(encoding)
                    # decode email sender
                    From, encoding = decode_header(msg.get("From"))[0]
                    if isinstance(From, bytes):
                        From = From.decode(encoding)
                    # if the email message is multipart
                    if msg.is_multipart():
                        # iterate over email parts
                        for part in msg.walk():
                            # extract content type of email
                            content_type = part.get_content_type()
                            content_disposition = str(part.get("Content-Disposition"))
                            try:
                                # get the email body
                                body = part.get_payload(decode=True).decode()
                            except:
                                pass
                            if content_type == "text/plain" and "attachment" not in content_disposition:
                                # print text/plain emails and skip attachments
                                pass
                            elif "attachment" in content_disposition:
                                # download attachment
                                filename = part.get_filename()
                                if filename:
                                    if ".pdf" in filename:
                                        folder_name = "./files"
                                        if not os.path.isdir(folder_name):
                                            # make a folder for this email (named after the subject)
                                            os.mkdir(folder_name)
                                        filepath = os.path.join(folder_name, filename)
                                        # download attachment and save it
                                        open(filepath, "wb").write(part.get_payload(decode=True))
                                        filenames.append(filename)
            list_of_email.append(Email(From, subject, filenames))
        return list_of_email
