import logging
import queue

import numpy as np
from talipp.indicators import EMA, BB
from talipp.indicators.BB import BBVal
from agent import Agent
from anlytics.helpers import peak_detection
from dto import MarketStatus, TechnicalAnalysisSnapshot
from helpers import message_filter

log = logging.getLogger(Agent.Trading_Agent)



class Trader:
    number_of_active_orders = 1
    orders = {}

    def buy(self, status: MarketStatus):
        pass

    def sell(self, status: MarketStatus):
        pass


class TradingAgent:
    historical_analysis = {}
    history_recodes = queue.Queue(240)
    active_order = None
    last_profit = 0
    total_profit = 0
    take_profit = 1
    stop_loss = -10
    wait_until_next = True

    def __init__(self, *args, **kwargs):
        self.ema50 = EMA(period=200, input_values=[])
        self.bb = BB(period=14, std_dev_multiplier=2)

    async def accept_message(self, agent, message):
        await self.get_ta_signals(ta=message)
        await self.sell_asset(status=message)
        await self.buy_asset(status=message)

    @message_filter(message_type=MarketStatus, param_name="status")
    async def buy_asset(self, status: MarketStatus):
        pass

    @message_filter(message_type=MarketStatus, param_name="status")
    async def sell_asset(self, status: MarketStatus):
        pass

    @message_filter(message_type=TechnicalAnalysisSnapshot, param_name="ta")
    async def get_ta_signals(self, ta: TechnicalAnalysisSnapshot):
        log.info(f"{ self.historical_analysis=}")
        if ta.date not in self.historical_analysis:
            self.historical_analysis[ta.date] = {
                "position": len(self.historical_analysis)
            }
        existing_ta = self.historical_analysis[ta.date]
        self.historical_analysis[ta.date] = {
            ta.name: ta,
            **existing_ta
        }

    @message_filter(message_type=MarketStatus, param_name="status")
    async def market_status(self, status: MarketStatus):

        self.history_recodes.put(status.close)
        self.ema50.add_input_value(status.close)
        self.bb.add_input_value(status.close)

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
                close_val = status.close

                if ema_val < close_val:  # Ema 50 is lower than price value mean this is a up trend

                    place_order = False

                    # close under ub and cb
                    if bb_val.ub > close_val > bb_val.cb:
                        place_order = True
                    elif bb_val.cb > close_val > bb_val.lb:
                        place_order = True

                    if place_order:
                        self.active_order = {
                            "time": status.date,
                            "price": status.close
                        }

                    # plt.plot(recodes[200:])
                    # plt.plot(self.ema50)
                    # plt.show()

            if self.active_order is not None:
                profit = status.close - self.active_order["price"]
                profit_pv = profit * 100 / self.active_order["price"]

                if profit > self.last_profit:
                    if profit_pv > self.take_profit:
                        self.take_profit += 0.05

                if self.take_profit <= profit_pv or profit_pv <= self.stop_loss:
                    self.active_order = None
                    self.total_profit += profit
                    log.info(f"{status.date} {self.total_profit=} {self.take_profit=}")
                    self.take_profit = 1

                self.last_profit = profit_pv
