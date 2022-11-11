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
                    self.SetHoldings(symbol, 1)
                    # get buy-in price for trailing stop loss/profit
                    self.buyInPrice = current_price
                    # entered long position
                    self.isLong = True
                    self.Log(f"{self.Time} Entered Long Position at {current_price}")
                        
                if SlowisOverPrice: # and PreviousPOverPEMA: 
                    self.SetHoldings(symbol, -1)
                    # get sell-in price for trailing stop loss/profit
                    self.sellInPrice = current_price
                    # entered short position
                    self.isLong = False
                    self.Log(f"{self.Time} Entered Short Position at {current_price}")
                        
                    
class SymbolData:
    def __init__(self, algorithm, symbol):
        self.slowema= ExponentialMovingAverage(200)
        
        self.slowWindow = RollingWindow[IndicatorDataPoint](2)   #setting the Rolling Window for the fast MACD indicator, takes two values
        algorithm.RegisterIndicator(symbol, self.slowema, timedelta(hours=1))
        self.slowema.Updated += self.SlowEMAUpdated                    #Updating those two values
        
        self.closeWindow = RollingWindow[float](10)
        
        # Add consolidator to track rolling close prices
        self.consolidator = QuoteBarConsolidator(1)
        self.consolidator.DataConsolidated += self.CloseUpdated
        algorithm.SubscriptionManager.AddConsolidator(symbol, self.consolidator)
        
       
    def SlowEMAUpdated (self, sender, updated):
        '''Event holder to update the MACD Rolling Window values.'''
        if self.slowema.IsReady:
            self.slowWindow.Add(updated)
            
    def CloseUpdated(self, sender, bar):
        '''Event holder to update the close Rolling Window values'''
        self.closeWindow.Add(bar.Close)
       
       
       
    @property 
    def IsReady(self):
        return self.slowema.IsReady and self.closeWindow.IsReady
  
                      
                     
                  
                      
            
              
         
           
        


