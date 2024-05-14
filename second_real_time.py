import json
import time
import requests
from datetime import datetime

with open('wallets.json', 'r') as f:
    data = json.load(f)
    
wallet_addresses = [d['address'] for d in data]

token_contract = "2EBjqPYGLUExdWwJJRLqtGPawzb2aMjE1wTpUYKhy2UQ"

def get_transaction_detail(tx_signature, wallet):
    response = requests.post(
        "https://api.mainnet-beta.solana.com", 
        headers = {"Content-Type": "application/json"}, 
        json={"jsonrpc":"2.0","id":1, "method": "getConfirmedTransaction", 
              "params": [tx_signature, "json"]}
    )
    
    result = json.loads(response.text)
    if 'result' in result:
        if 'meta' in result['result']:
            if 'postTokenBalances' in result['result']['meta']:
                if result['result']['meta']['postTokenBalances'][0]['mint'] == token_contract:
                    trans_time = datetime.fromtimestamp(result['result']['blockTime'])
                    difference_time = datetime.now() - trans_time
                    difference_time = difference_time.total_seconds() / 60
                    if difference_time <= 5:
                        print('wallet:  ', wallet + "     " + datetime.now())

def check_transactions(wallet):
    response = requests.post(
        "https://api.mainnet-beta.solana.com", 
        headers = {"Content-Type": "application/json"}, 
        json={"jsonrpc":"2.0", "id":1, "method":"getConfirmedSignaturesForAddress2",
              "params":[wallet,{"limit":1}]}
    )
    
    result = json.loads(response.text)
    if 'result' in result:
        for transaction in result['result']:
            get_transaction_detail(transaction['signature'], wallet)

while True:
    for wallet in wallet_addresses:
        check_transactions(wallet)
    time.sleep(60*5)  # Check every 5 minutes