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
print(data['result']['value'])
# print(response.json())

with open('wallets.json', 'w') as f:
    json.dump(data['result']['value'], f)