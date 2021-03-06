import asyncio
import datetime
import logging
import pandas as pd

from agent import Agent
from dto import MarketStatus
from helpers import error_log
from dateutil.parser import *
log = logging.getLogger(Agent.History_Data_Reading_Agent)


class HistoryDataReadingAgent:
    def __init__(self, *args, **kwargs):
        pass

    @error_log(logger=log)
    async def execute(self, *args, **kwargs):
        df = pd.read_csv("./_data_/Binance_XMRUSDT_minute.csv", header=0)
        # df = df.head(10000)
        df = df[::-1]
        for open, high, low, close, unix, date in zip(df.open.values, df.high.values, df.low.values, df.close.values,
                                                      df.unix.values,
                                                      df.date.values):
            status = MarketStatus(
                unix=unix,
                # date=datetime.datetime.strptime(date, '%d/%m/%Y %H:%M').timestamp(),
                date=parse(date, dayfirst=True).timestamp(),
                ask=float(close),
                bid=float(close),
                open=float(open),
                high=float(high),
                low=float(low),
                close=float(close),
                volume=float(close),
                asset="XMRUSDT")
            log.info(f"{status=}")
            data = status.dict()
            await self.publish(Agent.Technical_Analyser_Agent, data)
            await self.publish(Agent.Trading_Agent, data)
            await self.display(data)
            await asyncio.sleep(0.8)
