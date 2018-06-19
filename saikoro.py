#!/user/bin/env python

import ramdom

print("Content-Type: text/html")
print("")

no = random.randint(1, 6)

print("""
<html>
<head><title>Dice</title></head>
<body>
    <h1>{num}</h1>
</body>
</html>
""".format(num=no))
