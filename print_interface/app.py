import subprocess
import os
from flask import Flask, render_template, request, redirect, url_for
from print_interface.email_service import EmailService

username = os.getenv('PRINT_INTERFACE_USERNAME')
password = open(os.getenv("CREDENTIALS_DIRECTORY", default="/dev/null") + "/print_interface_password", "r").readline().strip()


app = Flask(__name__)
email_service = EmailService(username, password)

@app.route('/')
def hello_world():  # put application's code here
    return redirect('/emails')


@app.route('/emails', methods=['GET', 'POST'])
def get_emails():
    email_service.login()
    if request.method == 'POST':
        email = request.form['path']
        try:
            double_sided = request.form['double sided']
        except KeyError:
            double_sided = False
        if double_sided == 'on':
            double_sided = True
        print_pdf(email, double_sided)
        print("Printing file " + email + "\ndouble sided: " + str(double_sided))
    list_of_emails = email_service.receive_new_emails()
    email_service.logout()
    return render_template('index.html', listOfEmails=list_of_emails)


def print_pdf(filename, double_sided):
    if double_sided:
        os.system('lpr -H tomate.local -P Kyocera_Kyocera_ECOSYS_M6630cidn_ -o sides=two-sided-long-edge ' + os.getcwd() + '/files/' + filename)
    else:
        os.system('lpr -H tomate.local -P Kyocera_Kyocera_ECOSYS_M6630cidn_ '+ os.getcwd() + '/files/' + filename)

@app.route('/load-emails', methods=['POST'])
def load_more_emails():
    if request.form['load_emails'] == '5more':
        email_service.number += 5
    elif request.form['load_emails'] == '5less':
        if email_service.number > 5:
            email_service.number -= 5
    return redirect(url_for('get_emails'))

if __name__ == '__main__':
    url_for('static', filename='style.css')
