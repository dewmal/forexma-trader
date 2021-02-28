import logging

from agent import Agent

log = logging.getLogger(Agent.Pick_Trading_Asset_Agent)


class PickTradingAssetAgent:

    def __init__(self, *args, **kwargs):
        pass

    async def accept_message(self, agent, message):
        log.info(f"{agent=}")
        log.info(f"{message=}")
