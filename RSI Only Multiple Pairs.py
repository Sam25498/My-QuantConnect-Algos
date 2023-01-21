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

        for ticker in ["EURUSD","USDJPY", "USDCHF", "AUDUSD"]:
            symbol = self.AddForex(ticker, Resolution.Hour, Market.Oanda).Symbol
            self.Data[symbol] = SymbolData(self, symbol)
            
            
            
        self.stopLossLevel = -0.05 # stop loss percentage 
        self.stopProfitLevel = 0.01# stop profit percentage
            
        self.SetWarmUp(100, Resolution.Hour)


    def OnData(self, data):
        
        if self.IsWarmingUp:
            return
            
        for symbol, symbolData in self.Data.items(): #Returns self.data's dictionary key-value pairs
            if not (data.ContainsKey(symbol) and data[symbol] is not None and symbolData.IsReady):
                continue
            
            rsi = symbolData.rsi.Current.Value # get the current indicator value
            current_price = symbolData.closeWindow[0]



            
