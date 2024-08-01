import json
import asyncio
from datetime import datetime
import time
from time import perf_counter
import boto3

import aiohttp
import requests

aws_client = boto3.client('ssm')
response = aws_client.get_parameter(Name = '/stocksReport/keyAlphaVantageAPI', WithDecryption = True)

alphaVantageKey = response['Parameter']['Value']

tickers = ['KPITTECH.BSE', 'PERSISTENT.BSE', 'NEWGEN.BSE', 'TEJASNET.BSE', 'ADANIGREEN.BSE', 'ADANIPOWER.BSE', 'TATAPOWER.BSE', 'JPPOWER.BSE', 'VEDL.BSE', 'RELIANCE.BSE']

async def dataRequest(ticker : str) -> dict:
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol={ticker}&apikey={alphaVantageKey}'

    async with aiohttp.ClientSession() as session:
        response = await session.get(url)
        data = await response.json()
    
    return data

async def dataCollection() -> list:
    
    results = await asyncio.gather(dataRequest('KPITTECH.BSE'), dataRequest('PERSISTENT.BSE'), dataRequest('NEWGEN.BSE'), dataRequest('TEJASNET.BSE'), dataRequest('ADANIGREEN.BSE'), dataRequest('ADANIPOWER.BSE'), dataRequest('TATAPOWER.BSE'), dataRequest('JPPOWER.BSE'), dataRequest('VEDL.BSE'), dataRequest('RELIANCE.BSE'))

    print('Results recieved')
    return results

stocksData = asyncio.run(dataCollection())

def weeklyPriceReport(price_weekly: dict) -> dict:
    lastWeekKey = list(price_weekly['Weekly Time Series'].keys())[0]
    lastWeek = price_weekly['Weekly Time Series'][lastWeekKey]

    for i in lastWeek.keys():
        if 'open' in i.lower():
            open = lastWeek[i]
        if 'close' in i.lower():
            close = lastWeek[i]

    percentChangePrice = round(((float(close)-float(open))/float(open))*100, 2)

    lastWeek['percentChangePrice'] = percentChangePrice
    return lastWeek

def lambda_handler(event, context):
    lst = []

    print('Preparing report')

    for i in stocksData:
        lst.append(weeklyPriceReport(i))

    print('Report ready')

    stockReport = list(zip(tickers, lst))

    print(stockReport)

    s3_client = boto3.client('s3')

    data = json.dumps(stockReport).encode('utf-8')

    date_today =  datetime.today().date()
    
    s3_client.put_object(Body = data, Bucket = 'stocksreport', Key = f'Report{date_today}')