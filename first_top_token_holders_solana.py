import requests
import json

url = "https://nd-326-444-187.p2pify.com/9de47db917d4f69168e3fed02217d15b/"

payload = {
    "id": 1,
    "jsonrpc": "2.0",
    "method": "getTokenLargestAccounts",
    "params": ["2EBjqPYGLUExdWwJJRLqtGPawzb2aMjE1wTpUYKhy2UQ"]
}
headers = {
    "accept": "application/json",
    "content-type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)
data = response.json()
tokenHolders = []

lists = data['result']['value']
index = 0
for item in lists:
    payload1 = {
        "id": 1,
        "jsonrpc": "2.0",
        "method": "getAccountInfo",
        "params": [
            item['address'],
            {
                "encoding": "jsonParsed",
                "commitment": "finalized"
            }
        ]
    }
    res = requests.post(url, headers=headers, json=payload1)
    data1 = res.json()
    tokenHolders.insert(index, {"address": data1['result']['value']['data']['parsed']['info']['owner'], 'amount': data1['result']['value']['data']['parsed']['info']['tokenAmount']['amount']})
    index += 1
# print(response.json())

with open('wallets.json', 'w') as f:
    json.dump(tokenHolders, f)