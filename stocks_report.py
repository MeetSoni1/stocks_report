import requests
import json
import asyncio
import aiohttp
import time

financialModelingPrepKey = 'xyz'

start = time.time()

async def data_request(ticker):
    async with aiohttp.ClientSession() as session:
        resp = await session.get(f'https://financialmodelingprep.com/api/v3/historical-price-full/{ticker}?from=1990-10-10&apikey={financialModelingPrepKey}')
        dic = await resp.json()        
    return dic

async def data_collection():
    key = financialModelingPrepKey
    stocks_tickers = ['AAPL', 'MSFT', 'TSLA', 'NVDA', 'GOOG']    
    stocks_data = {}

    AAPL= asyncio.create_task(data_request('AAPL'))
    MSFT= asyncio.create_task(data_request('MSFT'))
    TSLA= asyncio.create_task(data_request('TSLA'))
    NVDA= asyncio.create_task(data_request('NVDA'))
    GOOG= asyncio.create_task(data_request('GOOG'))

    AAPL_data = await AAPL
    MSFT_data = await MSFT
    TSLA_data = await TSLA
    NVDA_data = await NVDA
    GOOG_data = await GOOG    

    stocks_data['AAPL'] = AAPL_data['historical']
    stocks_data['MSFT'] = MSFT_data['historical']
    stocks_data['TSLA'] = TSLA_data['historical']
    stocks_data['NVDA'] = NVDA_data['historical']
    stocks_data['GOOG'] = GOOG_data['historical']

    return stocks_data

asyncio.run(data_collection())

end = time.time()
total_time = end-start
print(total_time)