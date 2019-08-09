#状態の取得及び行動の送信用

import urllib.request, urllib.parse

def getField(url, token):
    req = urllib.request.Request(url, None, token)
    with urllib.request.urlopen(req) as res:
        html = res.read().decode("utf-8")
        return html

def sendAction(url, token, action):
    req = urllib.request.Request(url, action, token)
    with urllib.request.urlopen(req) as res:
        html = res.read().decode("utf-8")
        return html

if __name__ == "__main__":
    sampleToken = {
        "Authorization": "procon30_example_token"
    }
    url = "http://localhost:8081/ping"
    print(getField(url, sampleToken))
    
    sampleAction = {
        "actions": [
                {
                    "agentID": 9,
                    "type": "move",
                    "dx": 1,
                    "dy": 1
                },
                {
                    "agentID": 10,
                    "type": "move",
                    "dx": -1,
                    "dy": -1
                }
            ]
    }
    print(sendAction(url, sampleToken, sampleAction))
