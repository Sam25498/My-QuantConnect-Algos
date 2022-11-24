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


    def OnData(self, data):
        
        if self.IsWarmingUp:
            return
            
        for symbol, symbolData in self.Data.items(): #Returns self.data's dictionary key-value pairs
            if not (data.ContainsKey(symbol) and data[symbol] is not None and symbolData.IsReady):
                continue
            
            rsi = symbolData.rsi.Current.Value # get the current indicator value
            current_price = symbolData.closeWindow[0]
            if self.Portfolio[symbol].Invested:
                
                if self.isLong:
                    condStopProfit = (current_price - self.buyInPrice)/self.buyInPrice > self.stopProfitLevel
                    condStopLoss = (current_price - self.buyInPrice)/self.buyInPrice < self.stopLossLevel
                    if condStopProfit:
                        self.Liquidate(symbol)
                        self.Log(f"{self.Time} Long Position Stop Profit at {current_price}")
                        

                    if condStopLoss:
                        self.Liquidate(symbol)
                        self.Log(f"{self.Time} Long Position Stop Loss at {current_price}")
                  
                else:
                    condStopProfit = (self.sellInPrice - current_price)/self.sellInPrice > self.stopProfitLevel
                    condStopLoss = (self.sellInPrice - current_price)/self.sellInPrice < self.stopLossLevel
                    if condStopProfit:
                        self.Liquidate(symbol)
                        self.Log(f"{self.Time} Short Position Stop Profit at {current_price}")
                        
                    if condStopLoss:
                        self.Liquidate(symbol)
                        self.Log(f"{self.Time} Short Position Stop Profit at {current_price}")
                        
    
            
            if not self.Portfolio[symbol].Invested:
                
                
                if rsi < 15:
                    self.SetHoldings(symbol, 1)
                    # get buy-in price for trailing stop loss/profit
                    self.buyInPrice = current_price
                    # entered long position
                    self.isLong = True
                    #Timebought = self.Time
                    self.Log(f"{self.Time} Entered Long Position at {current_price}")
     
