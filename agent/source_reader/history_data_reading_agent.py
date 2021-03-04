import asyncio
import logging
import pandas as pd

from agent import Agent

log = logging.getLogger(Agent.History_Data_Reading_Agent)


class HistoryDataReadingAgent:
    def __init__(self, *args, **kwargs):
        pass

    async def execute(self, *args, **kwargs):
        df = pd.read_csv("./_data_/Binance_XMRUSDT_minute.csv", header=0)
        # df = df.head(10000)
        df = df[::-1]
        for close, unix, date in zip(df.close.values, df.unix.values, df.date.values):
            data = {
                "unix": unix,
                "date": date,
                "ask": float(close),
                "bid": float(close),
                "asset": "XMRUSDT"
            }
            await self.publish(Agent.Trading_Agent, data)
            await self.display(data)
            await asyncio.sleep(0.5)
