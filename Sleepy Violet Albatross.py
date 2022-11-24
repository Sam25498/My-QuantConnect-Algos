#region imports
from AlgorithmImports import *
#endregion
from datetime import timedelta, datetime
class FocusedYellowLemur(QCAlgorithm):


    def Initialize(self):
        self.SetStartDate(2015, 12, 1)  # Set Start Date
        self.SetEndDate(2016, 12, 1)
        self.SetCash(100000)  # Set Strategy Cash
       
        self.Data = {}

        for ticker in ["TSLA","AAPL"]:
            symbol = self.AddEquity(ticker, Resolution.Hour, Market.USA).Symbol
            self.Data[symbol] = SymbolData(self, symbol)
            
            
            
        self.stopLossLevel = -0.05 # stop loss percentage 
        self.stopProfitLevel = 0.01# stop profit percentage
            
        self.SetWarmUp(100, Resolution.Hour)


