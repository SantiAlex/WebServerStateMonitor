import configparser
import hashlib
import time


class Auth(object):
    def __init__(self):
        self.on_line_users = {}
        cf = configparser.ConfigParser()
        cf.read('conf')
        self.user = cf.get('auth', 'user')
        self.pswd = cf.get('auth', 'pswd')

    def login(self, user, pswd):
        if user == self.user and pswd == self.pswd:
            hash = hashlib.md5(str(time.time()).encode()).hexdigest()
            self.on_line_users[hash] = time.time() + 300
            return hash
        else:
            return None

    def check(self, hash):
        if hash in self.on_line_users:
            t = time.time()
            if t < self.on_line_users[hash]:
                self.on_line_users[hash] = t + 300
                return True
        else:
            return False

    def logout(self, hash):
        pass


auth = Auth()
