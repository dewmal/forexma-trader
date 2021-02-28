import asyncio
import logging
import os

from cryptoxlib.clients.binance.BinanceClient import BinanceClient
from cryptoxlib.clients.binance.BinanceWebsocket import AllMarketTickersSubscription

from agent import Agent

log = logging.getLogger(Agent.Market_Status_Reading_Agent)


class MarketStatusReadingAgent:
    exit_request = False

    def __init__(self, *args, **kwargs):
        api_key = os.environ["BINANCE_API"]
        api_secret = os.environ["BINANCE_SEC"]
        self.client = BinanceClient(api_key, api_secret, api_trace_log=True)

    async def read_market_status(self, response) -> None:
        await self.publish(Agent.Highly_Volatile_Assets_Picker_Agent, response["data"])

    async def execute(self, *args, **kwargs):
        log.info(f"Start execute")
        self.client.compose_subscriptions([
            AllMarketTickersSubscription(callbacks=[self.read_market_status]),
        ])
        # Execute all websockets asynchronously
        while not self.exit_request:
            try:
                await self.client.start_websockets()
            except Exception as e:
                log.error(e, e.args)
                await asyncio.sleep(0.05)

        await self.client.close()
