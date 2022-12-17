#region imports
from AlgorithmImports import *
#endregion
from datetime import timedelta, datetime
class CreativeVioletDolphin(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2015, 12, 1)  # Set Start Date
        self.SetEndDate(2016, 12, 1)
        self.SetCash(10000)  # Set Strategy Cash
       
        self.Data = {}

        for ticker in ["TSLA","AAPL"]:
            symbol = self.AddEquity(ticker, Resolution.Hour, Market.USA).Symbol
            self.Data[symbol] = SymbolData(self, symbol)
        self.stopLossLevel = -0.05 # stop loss percentage 
        self.stopProfitLevel = 0.01# stop profit percentage
        self.tolerance = 1.01
            
        self.SetWarmUp(360, Resolution.Hour)


    def OnData(self, data):
        
        if self.IsWarmingUp:
            return
            
        for symbol, symbolData in self.Data.items():
            if not (data.ContainsKey(symbol) and data[symbol] is not None and symbolData.IsReady):
                continue
            
            fast = symbolData.fast.Current.Value
            slow = symbolData.slow.Current.Value
            current_price = symbolData.closeWindow[0]
            #current_price = data[symbol].Close
            self.is_uptrend = fast > slow * self.tolerance
            self.is_downtrend = slow > fast * self.tolerance
            
            
