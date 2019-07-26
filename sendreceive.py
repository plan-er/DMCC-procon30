#状態の取得及び行動の送信用

import urllib.request, urllib.parse

def getField(url, token):
    req = urllib.request.Request(url, None, token)
    with urllib.request.urlopen(req) as res:
        html = res.read().decode("utf-8")
        return html

#def sendAction(url, token, action):

if __name__ == "__main__":
    sampleToken = {
        "Authorization": "procon30_example_token"
    }
    print(getField("http://localhost:8081/ping", sampleToken))
