import asyncio
import logging
import queue
import matplotlib.pyplot as plt
import numpy as np

from agent import Agent
from anlytics.helpers import peak_detection

log = logging.getLogger(Agent.Trading_Agent)


class TradingAgent:
    history_recodes = queue.Queue(240)
    active_order = None
    total_profit = 0

    def __init__(self, *args, **kwargs):
        pass

    async def accept_message(self, agent, message):
        self.history_recodes.put(message["close"])

        if self.history_recodes.full():
            self.history_recodes.get()
            recodes = np.array(self.history_recodes.queue)
            idxs, peaks_points = peak_detection(recodes, order=20, count=5)

            last_trend = peaks_points[-1] - peaks_points[-2]
            place_to_buy = last_trend < 0

            if place_to_buy and self.active_order is None:
                self.active_order = {
                    "time": message["date"],
                    "price": message["close"]
                }

            if self.active_order is not None:
                profit = message["close"] - self.active_order["price"]
                profit_pv = profit * 100 / self.active_order["price"]

                # Take profit
                if profit_pv > 1 or profit_pv < -0.5:
                    self.active_order = None
                    log.info(f"{profit=} {profit_pv=}")
                    self.total_profit += profit
                    log.info(f"{self.total_profit=}")
