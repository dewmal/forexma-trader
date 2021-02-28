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
        df = df[::-1]
        for close, unix, date in zip(df.close.values, df.unix.values, df.date.values):
            await self.publish(Agent.Trading_Agent, {
                "unix": unix,
                "date": date,
                "close": float(close),
                "asset": "XMRUSDT"
            })
            await asyncio.sleep(0.001)
