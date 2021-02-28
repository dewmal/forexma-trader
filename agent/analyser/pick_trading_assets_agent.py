import logging
import os

from cryptoxlib.clients.binance.BinanceClient import BinanceClient

from agent import Agent

log = logging.getLogger(Agent.Pick_Trading_Asset_Agent)


class PickTradingAssetAgent:

    def __init__(self, *args, **kwargs):
        api_key = os.environ["BINANCE_API"]
        api_secret = os.environ["BINANCE_SEC"]
        self.client = BinanceClient(api_key, api_secret, api_trace_log=True)

    async def accept_message(self, agent, message):
        log.info(f"{agent=}")
        log.info(f"{message=}")
