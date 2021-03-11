import asyncio
import logging
import os

from cryptoxlib.Pair import Pair
from cryptoxlib.clients.binance.BinanceClient import BinanceClient
from cryptoxlib.clients.binance.BinanceWebsocket import CandlestickSubscription
from cryptoxlib.clients.binance.enums import CandelstickInterval

from agent import Agent
from dto import MarketStatus

log = logging.getLogger(Agent.Pair_Market_Status_Reading_Agent)


class PairMarketStatusReadingAgent:
    exit_request = False

    def __init__(self, *args, **kwargs):
        api_key = os.environ["BINANCE_API"]
        api_secret = os.environ["BINANCE_SEC"]
        self.client = BinanceClient(api_key, api_secret, api_trace_log=True)

    async def read_market_status(self, response) -> None:
        data = response["data"]
        kline = data["k"]
        open = kline["o"]
        high = kline["h"]
        low = kline["l"]
        close = kline["c"]
        ask = close
        big = close
        unix = kline["t"]
        date = kline["T"]
        asset = kline["s"]
        interval = kline["i"]
        status = MarketStatus(
            interval=interval,
            unix=unix,
            date=date,
            ask=float(ask),
            bid=float(big),
            open=float(open),
            high=float(high),
            low=float(low),
            close=float(close),
            volume=float(close),
            asset=asset)
        await self.publish(Agent.Highly_Volatile_Assets_Picker_Agent, status)

    async def execute(self, *args, **kwargs):
        log.info(f"Start execute")
        asset_one, asset_two = "BTC", "USDT"
        self.client.compose_subscriptions([
            CandlestickSubscription(Pair(asset_one, asset_two), CandelstickInterval.I_1MIN,
                                    callbacks=[self.read_market_status]),
        ])
        # Execute all websockets asynchronously
        while not self.exit_request:
            try:
                await self.client.start_websockets()
            except Exception as e:
                log.error(e, e.args)
                await asyncio.sleep(0.05)

        await self.client.close()
