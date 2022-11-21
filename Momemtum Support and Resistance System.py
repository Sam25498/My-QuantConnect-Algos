#region imports
from AlgorithmImports import *
#endregion
from datetime import datetime,timedelta
import numpy as np
#from daily_support_resitance import *
#from fourhr_support_resistance import *

class MeasuredApricot(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2020, 1, 30)  # Set Start Date
        self.SetEndDate(2020, 12, 30)
        self.SetCash(100000)  # Set Strategy Cash
        
        self.ticker = "USDCAD"
        # Rolling Windows to hold bar close data keyed by symbol
        self.Data = {}

        #for ticker in tickers:
        symbol = self.AddForex(self.ticker, Resolution.Hour, Market.Oanda).Symbol
        self.Data[symbol] = SymbolData(self, symbol)
            
        self.tolerance = 0.0025
            
        self.stopLossLevel = -0.05 # stop loss percentage 
        self.stopProfitLevel = 0.01# stop profit percentage
        
        self.SupportResistance = SupportResistance(self, self.ticker)
            
        self.SetWarmUp(50, Resolution.Hour)
        
        
