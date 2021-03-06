import logging

from talipp.indicators import EMA, BB
from talipp.indicators.BB import BBVal

from agent import Agent
from dto import MarketStatus, TechnicalAnalysisSnapshot
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

        await self.publish_bb(status=status)
        await self.publish_ema(status=status)

    async def publish_bb(self, status):
        if len(self.bb) > 0:
            bb_val: BBVal = self.bb[-1]
            ta = TechnicalAnalysisSnapshot(
                name="bb",
                date=status.date,
                unix=status.unix,
                values={
                    "period": 14,
                    "upper": bb_val.ub,
                    "center": bb_val.cb,
                    "lower": bb_val.lb,
                }
            )
            await self.publish(Agent.Trading_Agent, ta.dict())
            await self.display(ta.dict())

    async def publish_ema(self, status):
        if len(self.ema20) > 0:
            ta = TechnicalAnalysisSnapshot(
                name="ema20",
                date=status.date,
                unix=status.unix,
                values={
                    "period": 20,
                    "value": float(self.ema20[-1])
                }
            )
            await self.publish(Agent.Trading_Agent, ta.dict())
            await self.display(ta.dict())
