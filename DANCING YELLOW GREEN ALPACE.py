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
            supports, resistances = self.GetPriceLevels(window)
            
            less_than_price = [x for x in supports if x < current_price ]
            nextSupportLevel = less_than_price[min(range(len(less_than_price)), key=lambda i: abs(less_than_price[i] - current_price))]
            
            self.Log(f"Symbol: {symbol.Value} , Supports: {supports} , Resistances: {resistances}")
            #self.Debug(self.SMA45.Current.Value)

            AboveSupport = current_price > nextSupportLevel * self.tolerance
            if self.SMA45[symbol].Current.Value<0 and AboveSupport :
                self.marketTicket=self.MarketOrder(symbol, -100000)
    
    def GetPriceLevels(self, series, variation = 0.005, h = 3):
        
        supports = []
        resistances = []
        
        maxima = []
        
        minima = []
        
        # finding maxima and minima by looking for hills/troughs locally
        for i in range(h, series.Size-h):
            if series[i] > series[i-h] and series[i] > series[i+h]:
                
                maxima.append(series[i])
            elif series[i] < series[i-h] and series[i] < series[i+h]:
                minima.append(series[i])
       

        return supports, resistances    
            # identifying maximas which are resistances
        for m in maxima:
            r = m * variation
            # maxima which are near each other
            commonLevel = [x for x in maxima if x > m - r and x < m + r]
            # if 2 or more maxima are clustered near an area, it is a resistance
            if len(commonLevel) > 1:
                # we pick the highest maxima if the cluster as our resistance
                level = max(commonLevel)
    
