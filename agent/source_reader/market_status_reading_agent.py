import logging

from agent import Agent

log = logging.getLogger(Agent.Market_Status_Reading_Agent)


class MarketStatusReadingAgent:
    def __init__(self, *args, **kwargs):
        log.info("Start ")

    async def execute(self, *args, **kwargs):
        log.info("Excecute")
