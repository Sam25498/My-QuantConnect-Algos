#region imports
from AlgorithmImports import *
#endregion

from datetime import datetime,timedelta
PriceisOverSlow = None
SlowisOverPrice = None
PreviousPOverPEMA = None
PEMAOverPreviousP = None

class CryingRedLemur(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2019, 1, 30)  # Set Start Date
        self.SetEndDate(2020, 1, 30)
        self.SetCash(100000)  # Set Strategy Cash
        
        self.ticker = "USDCHF" #"USDJPY","GBPUSD",  "USDCAD","EURUSD".
        # Rolling Windows to hold bar close data keyed by symbol
        self.Data = {}

        #for self.ticker in self.tickers:
        symbol = self.AddForex(self.ticker , Resolution.Hour, Market.Oanda).Symbol
        self.Data[symbol] = SymbolData(self, symbol)
         
    
        self.tolerance = 1.001
     
        self.stopLossLevel = -0.05 # stop loss percentage 
        self.stopProfitLevel = 0.01# stop profit percentage
        
            
        self.SetWarmUp(200, Resolution.Hour)
        


    def OnData(self, data):
        
        if self.IsWarmingUp: #Data to warm up the algo is being collected.
        


