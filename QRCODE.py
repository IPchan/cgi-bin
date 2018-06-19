#!/usr/local/bin/python
# -*- coding: utf-8 -*-
import sys, codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout)
import qrcode
from PIL import Image
import cgi
from datetime import datetime

print "Content-Type: text/html\n"

print """
<!DOCTYPE html>
<html lang="ja">
<head>
<meta charset="UTF-8">
</head>
<body>
<style>
#content{
  width: 100%;
  text-align: center;
}

#topmain {
  width: 90%;
  margin: 0 auto;
  margin-top: 100px;
  text-align: center;
}

input[type="text"] {
  width: 400px;
  height: 30px;
}

input[type="submit"] {
  background: #ff9900!important;
  color: #fff;
  font-size: 15px;
  padding: 8px;
  border-radius: 4px;
  width: 200px;
}

</style>
<div id="content">
<div id="topmain">
"""

form = cgi.FieldStorage()

newQr = form["targets"].value
today = datetime.now().strftime("%Y/%m/%d %H:%M:%S")

print "<h1>" + newQr + "</h1>"
print "<p>" + today + "</p>"
print "<p><a href=\"index.html\">Back to TOP</a></p>"

img = qrcode.make(newQr)
img.save('qr_code.png')

print "<p><img src=\"qr_code.png\"></p>"

print """
</div>
</div>
</body>
</html>
"""
