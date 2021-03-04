import logging

from talipp.indicators import EMA, BB

from agent import Agent
from dto import MarketStatus
from helpers import message_filter

log = logging.getLogger(Agent.Technical_Analyser_Agent)


class TechnicalAnalyserAgent:
    def __init__(self, *args, **kwargs):
        self.ema20 = EMA(period=20, input_values=[])
        self.bb = BB(period=14, std_dev_multiplier=2)

    async def accept_message(self, agent, message):
        await self.read_market_status(status=message)

    @message_filter(message_type=MarketStatus, param_name="status")
    async def read_market_status(self, status: MarketStatus):
        self.ema20.add_input_value(status.close)
        self.bb.add_input_value(status.close)

        if len(self.ema50) > 0:
            await self.display({"ema": float(self.ema20[-1])})
