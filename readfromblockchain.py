import json
import urllib.request
import urllib.parse
import base64


APT_URL = 'http://192.168.0.51:8888'

contents = urllib.request.urlopen(APT_URL+"/getheight").read()
data = json.loads(contents)

lastnum = data["Data"]

contents = urllib.request.urlopen(APT_URL+"/getblockbyheight?number="+str(lastnum)).read()
data = json.loads(contents)

hash = data["Data"]["txs"][0]

contents = urllib.request.urlopen(APT_URL+"/getstore?hash=" + urllib.parse.quote(str(hash))).read()

data = json.loads(contents)
print(json.loads(base64.b64decode(data["Data"])))