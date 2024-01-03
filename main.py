import aiohttp
import asyncio
from datetime import datetime, timedelta
import sys


class ExchangeRateAPI:
    async def get_exchange_rates(self, start_date, end_date):
        async with aiohttp.ClientSession() as session:
            try:
                url = f'http://api.nbp.pl/api/exchangerates/tables/C/{start_date}/{end_date}/'
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
        rates = []
        for day_data in data:
            date = day_data['effectiveDate']
            day_rates = {}
            for rate in day_data['rates']:
                if rate['code'] in ['EUR', 'USD']:
                    day_rates[rate['code']] = {'buy': rate['bid'], 'sell': rate['ask']}
            if day_rates:
                rates.append({date: day_rates})
        return rates


class ExchangeRateTool:
    def __init__(self, api):
        self.api = api

    async def get_rates_for_last_days(self, days):
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        formatted_start_date = start_date.strftime('%Y-%m-%d')
        formatted_end_date = end_date.strftime('%Y-%m-%d')
        rates = await self.api.get_exchange_rates(formatted_start_date, formatted_end_date)
        return rates


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
