import requests

def lambda_handler(event, context):

    resp = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json')
    print(resp.json())