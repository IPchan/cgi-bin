import os , json
import cgi
from http import cookies
import datetime, random, hashlib

#cookieの取得

class CookieSession:
    SESSION_ID = "CookieSessionId"

    SESSION_DIR = os.path.dirname(
    os.path.abspath(__file__)) +"/SESSION"

    def __init__(self):
        if not os.path.exists(self.SESSION_DIR):
            os.mkdir(self.SESSION_DIR)

        rc = os.environ.get('HTTP_COOKIE','')
        self.cookie = cookies.SimpleCookie(rc)
        if self.SESSION_ID in self.cookie:
            self.sid = self.cookie[self.SESSION_ID].value
        else:
            self.sid = self.gen_sid()

        self.modified = False
        self.values = {}
        path = self.SESSION_DIR + "/" + self.sid
        if os.path.exsists(path):
            with open(path, "r", encoding="utf-8")as f:
                a_json = f.read()
                self.values = json.loads(a_json)
    def gen_sid(self):
        token = ":#sa$2jAiN"
        now = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
        rnd = random.randint(0,100000)
        key = (token + now + str(rnd)).encode("utf-8")
        sid = hashlib.sha256(key).hexdigest()
        return sid

    def output(self):
        self.cookie[self.SESSION_ID] = self.sid
        self.save_data()
        return self.cookie.output()


    def save_data(self):
        if not self.modified: return
        path = self.SESSION_DIR + "/" + self.sid
        a_json = json.dumps(self.values)
        with open(path,"w",encoding="utf-8")as f:
            f.write(a_json)

    def __getitem__(self,key):
        return self.values[key]

    def __Setitem__(self,key,value):
        self.modified = True
        self.values[key] = value

    def __contains__(self,key):
        return key in self.values

    def clear(self):
        self.values = {}
