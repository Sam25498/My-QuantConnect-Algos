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
            return
        
        for symbol, symbolData in self.Data.items(): #Return the dictionary's key-value pairs:
            if not (data.ContainsKey(symbol) and data[symbol] is not None and symbolData.IsReady):
                continue
            
            slowEMA = symbolData.slowema.Current.Value
            
            self.Log(f"{symbolData.slowWindow[0]} ema values ")
            #sWindow = symbolData.slowWindow
            #previousEMA = symbolData.slowWindow[1]
    
            current_price = symbolData.closeWindow[0] 
            #previous_price = symbolData.closeWindow[1]
            
            

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
                        self.Log(f"{self.Time} Short Position Stop Loss at {current_price}")
            
            
            if not self.Portfolio[symbol].Invested:
                PriceisOverSlow = current_price - slowEMA * self.tolerance
                SlowisOverPrice = slowEMA > current_price * self.tolerance
                #PreviousPOverPEMA = previous_price > previousEMA * self.tolerance
                #PEMAOverPreviousP = previousEMA > previous_price * self.tolerance 
                
              
                
                if PriceisOverSlow: #and PEMAOverPreviousP:
                      
            
              
         
           
        


