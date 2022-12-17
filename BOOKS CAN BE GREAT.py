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
                        
                    
class SymbolData:
    def __init__(self, algorithm, symbol):
        self.fast = algorithm.SMA(symbol, 5) 
        self.fastWindow = RollingWindow[IndicatorDataPoint](2)
        
        #Generating 5-period EMA values of 4 hours Resolution
        algorithm.RegisterIndicator(symbol, self.fast, timedelta(hours=4))
        self.fast.Updated += self.FastUpdated 
        self.slow = algorithm.SMA(symbol, 10 ) 
        self.slowWindow = RollingWindow[IndicatorDataPoint](2)
        
        #Generating 10-period EMA values of 4 hours Resolution.
        algorithm.RegisterIndicator(symbol, self.slow, timedelta(hours=4))
        self.slow.Updated += self.SlowUpdated 

        self.closeWindow = RollingWindow[float](10)
        
        # Add consolidator to track rolling close prices
        self.consolidator = TradeBarConsolidator(4)
        self.consolidator.DataConsolidated += self.CloseUpdated
        algorithm.SubscriptionManager.AddConsolidator(symbol, self.consolidator)
        

    def FastUpdated(self, sender, updated):
        #'''Event holder to update the fast EMA Rolling Window values'''
        if self.fast.IsReady:
            self.fastWindow.Add(updated)
    def SlowUpdated(self, sender, updated):
        '''Event holder to update the slow SMA Rolling Window values'''
        if self.slow.IsReady:
            self.slowWindow.Add(updated)
            
            
    def CloseUpdated(self, sender, bar):
        '''Event holder to update the close Rolling Window values'''
        self.closeWindow.Add(bar.Close)
       
           


                                
    
   
          
