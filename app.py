import subprocess

from flask import Flask, render_template, request, redirect
from markupsafe import escape
from emailObject import Email

app = Flask(__name__)
listOfEmails = []

@app.route('/')
def hello_world():  # put application's code here
    return redirect('/emails')


@app.route('/emails', methods=['GET', 'POST'])
def get_emails():
    if request.method == 'POST':
        email = request.form['path']
        print("Printing file " + email)
    return render_template('index.html', listOfEmails=listOfEmails)


def print_pdf(filename):
    subprocess.Popen(['lpr', "./files/" + filename])

@app.route('/generateEmails', methods=['POST'])
def generate_email():
    listOfEmails.append(Email("joachim.stramke@ifsr.de", "test", "test", False))
    return redirect("/emails")

@app.route('/hello/<username>')
def show_name(username):
    return f'Hello {escape(username)}'


if __name__ == '__main__':
    app.run()
