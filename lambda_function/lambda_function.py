import json
import asyncio
from datetime import datetime
import boto3

import aiohttp
import requests

# Fetch API key from SSM parameter Store
aws_client = boto3.client('ssm')
response = aws_client.get_parameter(Name = '/stocksReport/keyAlphaVantageAPI', WithDecryption = True)

alphaVantageKey = response['Parameter']['Value']

# List of tickers to process
tickers = ['KPITTECH.BSE', 'PERSISTENT.BSE', 'NEWGEN.BSE', 'TEJASNET.BSE', 'ADANIGREEN.BSE', 'ADANIPOWER.BSE', 'TATAPOWER.BSE', 'JPPOWER.BSE', 'VEDL.BSE', 'RELIANCE.BSE']

async def dataRequest(ticker : str) -> dict:
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol={ticker}&apikey={alphaVantageKey}'

    try:
        async with aiohttp.ClientSession() as session:
            response = await session.get(url)
            return await response.json()
    except Exception as e:
        print(f"Failed to fetch data for {ticker}: {e}")
        return {}

async def dataCollection() -> list:
    
    results = await asyncio.gather(dataRequest('KPITTECH.BSE'), dataRequest('PERSISTENT.BSE'), dataRequest('NEWGEN.BSE'), dataRequest('TEJASNET.BSE'), dataRequest('ADANIGREEN.BSE'), dataRequest('ADANIPOWER.BSE'), dataRequest('TATAPOWER.BSE'), dataRequest('JPPOWER.BSE'), dataRequest('VEDL.BSE'), dataRequest('RELIANCE.BSE'))

    print('Results recieved')
    return results

def weeklyPriceReport(price_weekly: dict) -> dict:
    try:
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
    except KeyError as e:
        print(f"KeyError while processing data: {e}")
        return {}

def lambda_handler(event, context):
    # Collect stock data
    stocksData = asyncio.run(dataCollection())
    
    # Prepare report
    report = []
    for ticker, data in zip(tickers, stocks_data):
        if data:
            processed_data = calculate_percent_change(data)
            report.append((ticker, processed_data))
    print("Report generated")

    # Upload to S3
    try:
        s3_client = boto3.client('s3')
        date_today = datetime.today().date()
        data = json.dumps(report).encode('utf-8')
        s3_client.put_object(Body=data, Bucket='stocksreport', Key=f'Report_{date_today}.json')
        print('Report uploaded successfully')
    except Exception as e:
        print(f"Failed to upload report to S3: {e}")

    return {
        'statusCode': 200,
        'body': json.dumps('Report generation and upload complete')
    }