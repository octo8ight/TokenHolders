import requests
import json
import time

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

def getLargetTokenHoldersWallet():
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

    return tokenHolders

def findWalletAndAmount(data, address):
    for wallet in data:
        if wallet['address'] == address:
            return wallet['amount']
    return -1

def checkTokenAmountInWallet():
    with open('wallets.json') as f:
        data = json.load(f)

    newData = getLargetTokenHoldersWallet()
    for wallet in newData:
        pastAmount = findWalletAndAmount(data=data, address=wallet['address'])
        newAmount = wallet['amount']
        if pastAmount != newAmount and wallet['address'] != '5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1':
            print(wallet['address'] + 'birb token balance changed.   changed amount: ' + abs(int(newAmount) - int(pastAmount)))

    with open('wallets.json', 'w') as f:
        json.dump(newData, f)

while True:
    checkTokenAmountInWallet()
    time.sleep(60*10)
