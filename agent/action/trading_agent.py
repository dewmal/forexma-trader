import logging
import queue

import numpy as np
from talipp.indicators import EMA, BB
from talipp.indicators.BB import BBVal
import matplotlib.pyplot as plt
from agent import Agent
from anlytics.helpers import peak_detection

log = logging.getLogger(Agent.Trading_Agent)


class TradingAgent:
    history_recodes = queue.Queue(240)
    active_order = None
    total_profit = 0

    def __init__(self, *args, **kwargs):
        self.ema50 = EMA(period=200, input_values=[])
        self.bb = BB(period=14, std_dev_multiplier=2)

    async def accept_message(self, agent, message):
        self.history_recodes.put(message["close"])
        self.ema50.add_input_value(message["close"])
        self.bb.add_input_value(message["close"])

        if self.history_recodes.full():
            self.history_recodes.get()
            self.bb.purge_oldest(1)

            recodes = np.array(self.history_recodes.queue)
            idxs, peaks_points = peak_detection(recodes, order=20, count=5)

            last_trend = peaks_points[-1] - peaks_points[-2]
            place_to_buy = last_trend < 0

            if place_to_buy and self.active_order is None:
                bb_val: BBVal = self.bb[-1]
                ema_val = self.ema50[-1]
                close_val = message['close']

                if ema_val < close_val:  # Ema 50 is lower than price value mean this is a up trend

                    place_order = False

                    # close under ub and cb
                    if bb_val.ub > close_val > bb_val.cb:
                        place_order = True
                    elif bb_val.cb > close_val > bb_val.lb:
                        place_order = True

                    if place_order:
                        self.active_order = {
                            "time": message["date"],
                            "price": message["close"]
                        }

                    # plt.plot(recodes[200:])
                    # plt.plot(self.ema50)
                    # plt.show()

            if self.active_order is not None:
                profit = message["close"] - self.active_order["price"]
                profit_pv = profit * 100 / self.active_order["price"]

                # Take profit
                if profit_pv > 1 or profit_pv < -0.001:
                    self.active_order = None
                    self.total_profit += profit
                    log.info(f"{message['date']} {self.total_profit=}")
