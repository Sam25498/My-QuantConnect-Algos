#region imports
from AlgorithmImports import *
#endregion
from datetime import datetime,timedelta
import numpy as np
class DancingYellowGreenAlpaca(QCAlgorithm):


    def Initialize(self):
        self.SetStartDate(2020, 1, 30)  # Set Start Date
        self.SetCash(100000)  # Set Strategy Cash
     
        tickers = ["EURUSD","USDCAD"]
        # Rolling Windows to hold bar close data keyed by symbol
        self.closingData = {}
        self.SMA45 = {}
        for ticker in tickers:
            symbol = self.AddForex(ticker, Resolution.Hour, Market.Oanda).Symbol
            self.closingData[symbol] = RollingWindow[float](50)
        # Warm up our rolling windows
            self.SMA45[symbol] = self.SMA(symbol, 45, Resolution.Hour) 
        self.tolerance = 1.004000555
        self.SetWarmUp(50)
        
    def OnData(self, data):
        
        for symbol, window in self.closingData.items():
            if data.ContainsKey(symbol) and data[symbol] is not None:
                window.Add(data[symbol].Close)
                
      
        current_price = data[symbol].Close
        
        if self.IsWarmingUp or not all([window.IsReady for window in self.closingData.values()]):
            return
        
        for symbol, sma in self.SMA45.items():
            self.Plot('SMA', symbol.Value, sma.Current.Value)
        
        for symbol, window in self.closingData.items():
   
