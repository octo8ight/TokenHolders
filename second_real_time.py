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
              "params": [tx_signature, {"encoding": "jsonParsed","maxSupportedTransactionVersion":0}]}
    )
    
    result = json.loads(response.text)

    if 'result' in result:
        if 'meta' in result['result'] and 'err' in result['result']['meta'] and result['result']['meta']['err'] == None:
            if 'transaction' in result['result'] and 'message' in result['result']['transaction'] and 'accountKeys' in result['result']['transaction']['message']:
                for item in result['result']['transaction']['message']['accountKeys']:
                    if item['pubkey'] == token_contract:
                        trans_time = datetime.fromtimestamp(result['result']['blockTime'])
                        difference_time = datetime.now() - trans_time
                        difference_time = difference_time.total_seconds() / 60
                        if difference_time <= 5:
                            print('wallet:  ', wallet, "       ", trans_time)
                            break
                        break

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
    
# for wallet in wallet_addresses:
#     check_transactions(wallet)
# get_transaction_detail('5LK5ig3L8oqfs2MYyNHtH2EJ7zvk4c2Ed9KMVmDpoLBRGdtr11y5wDYkHfv4dtxucfdjE9tddJzAx4in7V9A8Rm4', '5Q544fKrFoe6tsEbD7S8EmxGTJYAKtTVhAW5Q5pge4j1')
