# region imports
from AlgorithmImports import *
# endregion

#class HyperActiveSkyBlueGuanaco(QCAlgorithm):

from datetime import datetime, timedelta
import numpy as np
import pandas as pd
#from QuantConnect.algorithm import QCAlgorithm
#from QuantConnect.data.market import TradeBar
#from QuantConnect.data.custom import Forex
#from QuantConnect.Indicators import CandlestickPatterns
from QuantConnect.Indicators.CandlestickPatterns import Engulfing

class ForexAlgorithm(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2020, 1, 1)  # Set the start date
        self.SetEndDate(2022, 12, 31)  # Set the end date
        self.SetCash(100000)  # Set the initial capital
        self.engulfing = Engulfing()  # Initialize the bullish engulfing indicator
        self.AddForex("EURUSD", Resolution.Hour)  # Add the EURUSD pair to the algorithm
        #self.engulfing = Engulfing(self.Symbol)  # Initialize the bullish engulfing indicator


        self.resistance_level = None  # Initialize the resistance level variable
        self.previous_bar = None  # Initialize the previous bar variable

    def OnData(self, data):
        if not data.ContainsKey(self.Symbol):
            return

        #bar = data[self.Symbol]  # Get the current bar
        self.engulfing.Update(data.Bars[self.symbol])  # Update the bullish engulfing indicator

  
      # Check if the price has broken the resistance level
        if self.resistance_level is not None and bar.Close > self.resistance_level:
            self.resistance_level = None  # Clear the resistance level

        # Check if the price has retested the resistance level
        if self.resistance_level is not None and self.previous_bar is not None and self.previous_bar.Low <= self.resistance_level <= bar.High:
            # Check if the bullish engulfing pattern is formed
            if self.engulfing.IsReady:
                self.SetHoldings(self.Symbol, 1)  # Execute a buy trade

        self.previous_bar = bar  # Store the previous bar for later reference
