#user.py
class User:
    def __init__(self, username, password_hash):
        self.username = username
        self.password_hash = password_hash
        self.balance = 0  # Cash balance
