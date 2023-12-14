import subprocess
import os
from flask import Flask, render_template, request, redirect
from markupsafe import escape
from emailObject import Email
from email_service import EmailService
from dotenv import load_dotenv

# loading username and password from the .env file, which has to be created
load_dotenv()
username = os.getenv('USERNAME')
password = os.getenv('PASSWORD')


app = Flask(__name__)
listOfEmails = []
email_service = EmailService(username, password)

@app.route('/')
def hello_world():  # put application's code here
    return redirect('/emails')


@app.route('/emails', methods=['GET', 'POST'])
def get_emails():
    if request.method == 'POST':
        email = request.form['path']
        print("Printing file " + email)
    listOfEmails = email_service.receive_new_emails()
    return render_template('index.html', listOfEmails=listOfEmails)


def print_pdf(filename):
    subprocess.Popen(['lpr', "./files/" + filename])


if __name__ == '__main__':

    app.run()
