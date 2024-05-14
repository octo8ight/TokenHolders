import requests
import pandas as pd
from datetime import date
import json
today = date.today()

query_template = '''
{
  EVM(dataset: archive, network: eth) {
    TokenHolders(
      date: "%s"
      tokenSmartContract: "%s"
      limit: {count: 50}
      orderBy: {descending: Balance_Amount}
    ) {
      Balance {
        Amount
      }
      Holder {
        Address
      }
    }
  }
}
'''

url = 'https://streaming.bitquery.io/graphql'

token_contract = "0xdAC17F958D2ee523a2206206994597C13D831ec7"

data_contract1 = {}

def shorten_address(address):
    return f"{address[:5]}...{address[-3:]}" if len(address) > 8 else address

def convert_to_millions_or_billions(number):
    if number >= 1_000_000_000:
        return f'{number / 1_000_000_000:.2f}B'
    if number >= 1_000_000:
        return f'{number / 1_000_000:.2f}M'
    return f'{number:.2f}'

formatted_query = query_template % (today.strftime("%Y-%m-%d"), token_contract)
headers = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer ory_at_nDt3gMlklG2ciF-4Hw5yMY4Vztl_UyEgGFiI6y7lM4w.c6tmsOioFn6dF15-8l-3AxxgOjpjWqmLQ9ESuMxg9nc',
    "X-API-KEY": "BQY4z6NH9bRClNbowdXZfFFGtSMRki2L"
}
response = requests.post(url, json={'query': formatted_query}, headers=headers)
data = response.json()

with open('wallets.json', 'w') as f:
    json.dump(data['data']['EVM']['TokenHolders'], f)