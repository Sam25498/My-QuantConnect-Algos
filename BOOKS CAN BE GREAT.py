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
                uptrend = self.is_uptrend
                downtrend = self.is_downtrend
                
                if downtrend and current_price < fast:
                    self.SetHoldings(symbol, 0)
                    # get buy-in price for trailing stop loss/profit
                    self.buyInPrice = current_price
                    # entered long position
                    self.isLong = True
                    #Timebought = self.Time
                    self.Log(f"{self.Time} Entered Long Position at {current_price}")
                        
                if uptrend and current_price > fast:
                    self.SetHoldings(symbol, -1)
                    # get sell-in price for trailing stop loss/profit
                    self.sellInPrice = current_price
                    # entered short position
                    self.isLong = False
                    #Timesold = self.Time
                    self.Log(f"{self.Time} Entered Short Position at {current_price}")
                        
              
    
   
          
