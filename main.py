import aiohttp
import asyncio
from datetime import datetime, timedelta
import sys


class ExchangeRateAPI:
    async def get_exchange_rates(self, date):
        async with aiohttp.ClientSession() as session:
            try:
                url = f'http://api.nbp.pl/api/exchangerates/tables/C/{date}/'
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self.parse_rates(data)
                    else:
                        return None
            except Exception as e:
                print(f"Error while fetching data: {e}")
                return None

    @staticmethod
    def parse_rates(data):
        rates = {}
        for rate in data[0]['rates']:
            if rate['code'] in ['EUR', 'USD']:
                rates[rate['code']] = {'buy': rate['bid'], 'sell': rate['ask']}
        return rates


class ExchangeRateTool:
    def __init__(self, api):
        self.api = api

    async def get_rates_for_last_days(self, days):
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        tasks = []
        for single_date in (start_date + timedelta(n) for n in range(days)):
            formatted_date = single_date.strftime('%Y-%m-%d')
            task = asyncio.create_task(self.api.get_exchange_rates(formatted_date))
            tasks.append(task)

        rates = await asyncio.gather(*tasks)

        return [{(start_date + timedelta(n)).strftime('%d.%m.%Y'): rate} for n, rate in enumerate(rates) if rate]


async def main(days):
    api = ExchangeRateAPI()
    tool = ExchangeRateTool(api)
    rates = await tool.get_rates_for_last_days(days)
    print(rates)


if __name__ == "__main__":
    try:
        days = min(int(sys.argv[1]), 10)
    except (IndexError, ValueError):
        days = 1

    asyncio.run(main(days))
