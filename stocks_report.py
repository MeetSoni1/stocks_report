import requests
import json
import asyncio
import aiohttp
import time

financialModelingPrepKey = 'xyz'


start = time.time()

async def data_request(ticker):
    async with aiohttp.ClientSession() as session:
        resp = await session.get(f'https://financialmodelingprep.com/api/v3/historical-price-full/{ticker}?apikey={financialModelingPrepKey}')
        # print(ticker, resp.status_code)
        dic = await resp.json()
    return dic

async def data_collection():
    key = financialModelingPrepKey
    stocks_tickers = ['AAPL', 'MSFT', 'TSLA', 'NVDA', 'GOOG']    
    stocks_data = {}

    results = await asyncio.gather(data_request('AAPL'), data_request('MSFT'), data_request('TSLA'), data_request('NVDA'), data_request('GOOG'))

    for i in results:
        print (i['historical'][0])
    return 0 #stocks_data

asyncio.run(data_collection())

end = time.time()
total_time = end-start
print(total_time)