#!user/yoshiki/hp/hp.py

import cgi
import cgitb
import os
import html
import cksession
import datetime

class HP:
    USERS = {"user":"pass"}

    FILE_MSG = "hp-msg.hp"

    def __iint__(self):
        self.form = cgi.FieldStorage()
        self.session = cksession.CookieSession()
        self.check_mode()

    def check_mode(self):
        mode = self.form.getvalue("mode","login")
        if mode == "login"      :self.mode_login()
        elif mode == "trylogin" :self.mode_trylogin()
        elif mode == "logout"   :self.mode_logout()
        elif mode == "sec"      :self.mode_sec()
        elif mode == "secedit"  :self.secedit()
        else: self.mode_login()

    def print_html(self, title,html,headers = []):
        print("Content-Type: text/html; charset=utf-8")
        for hd in headers: print(hd)
        print("")
        print("""
        <html><head><meta charset = "utf-8">
        <title>{0}</title></head><body>
        <h2>{0}</h2><div>{1}</div></body></html>
        """.format(title, html))


    def show_error(self, msg):
        self.print_html("エラー","""
        <div style="color:red">{0}</div>
        """.format(msg))

    def mode_login(self):
            self.print_html("GI名簿作成","""
            <form method="POST">
            ユーザー名:<input type="text" name="user" size="8"><br>
            パスワード:<input type="password" name="pw" size="8">
            <input type ="submit" value = "ログイン">
            <input type ="hidden" name="mode" value="trylogin">
            </form>
            """ )

    def mode_trylogin(self):
        user = self.form.getvalue("user","")
        pw = self.form.getvalue("pw","")

        if not (user in self.USERS):
            self.show_error("ユーザーが存在しません")
            return
        if self.USERS[user] != pw:
            self.show_error("パスワードが異なります")
            return
            now = datetime.datetime.now()
            self.session["login"] = now.timestamp()
            headers = [self.session.output()]
            self.print_html("ログイン成功","""
            <a href="hp.py?mode=sec">登録情報を見る</a>
            """, headers)

    def mode_logout(self):
        self.session["login"] =0
        self.print_html("ログアウト","""
        <a href="hp.py">ログアウトしました</a>
        """,[self.session.output()]
        )
        def is_login(self):
            if "login" in self.session:
                if self.session['login'] > 0:
                    return True
                    return False


    def mode_sec(self):
        if not self.is_login():
            self.show_error('ログインが必要です')
            return
        msg = "ここにメッセージを書いてください"
        if os.path.exists(self.FILE_MSG):
            with open(self.FILE_MSG,"r",encoding="utf-8")as f:
                msg = f.read()
            msg = html.escape(msg)
            self.print_html("秘密のメッセージ","""
            <form method = "POST" action="hp.py">
            <textarea name ="msg" rows="5" colors="80">{0}</textarea>
            <br><input type "submit" value="変更">
            <input type="hidden" neme ="mode" value="secedit"</form>
            <hr><a href="hp.py?mode=logout">→ログアウト</a>
            """.format(msg))

    def mode_secedit(self):
        if not self.is_login():
            self.show_error("ログインが必要です","")
            return
        msg = self.form.getvalue("msg","")
        with open(self.FILE_MSG,"w",encoding="utf-8")as f:
            f.write(msg)
            self.print_html("変更しました","""
            <a href="hp.py?mode=sec">内容を確認する</a>
            """)
if __name__ == "__main__":
    cgitb.enable()
    app = HP()
