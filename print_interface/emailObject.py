class Email:
    def __init__(self, email, subject, file: list, printing=False):
        self.email = email
        self.subject = subject
        self.file = file
        self.printing = printing
