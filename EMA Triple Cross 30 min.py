
#region imports
from AlgorithmImports import *
#endregion

from datetime import datetime,timedelta
FastisOverSlow = None
SlowisOverFast = None
FastisOverMedium = None
MediumisOverFast = None
PreviousFastAbovePreviousM = None
PreviousFastBelowPreviousM = None

class MuscularRedOrangeHorse(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2020, 1, 1)  # Set Start Date
        self.SetEndDate(2020, 12, 30)
        self.SetCash(100000)  # Set Strategy Cash
        
        self.ticker = "EURGBP" #"USDJPY","GBPUSD",  "USDCAD","EURUSD".
        # Rolling Windows to hold bar close data keyed by symbol
        self.Data = {}

        #for self.ticker in self.tickers:
        symbol = self.AddForex(self.ticker , Resolution.Minute, Market.Oanda).Symbol
        self.Data[symbol] = SymbolData(self, symbol)
         
    
        self.tolerance = 1.001
     
        self.stopLossLevel = -0.0020 # stop loss percentage 
        self.stopProfitLevel = 0.0020# stop profit percentage
        
            
        self.SetWarmUp(50, Resolution.Minute)
        


    def OnData(self, data):
        
        if self.IsWarmingUp: #Data to warm up the algo is being collected.
            return
        
        self.LondonSession = self.Time.hour > 6 and self.Time.hour < 10

        for symbol, symbolData in self.Data.items(): #Return the dictionary's key-value pairs:
            if not (data.ContainsKey(symbol) and data[symbol] is not None and symbolData.IsReady):
                continue
            
            slowEMA = symbolData.slowema.Current.Value
            fastEMA = symbolData.fastema.Current.Value
            mediumEMA = symbolData.mediumema.Current.Value
            previousf = symbolData.fastWindow[1]
            previousm = symbolData.mediumWindow[1]
            
            #current_price = data[symbol].Close
            current_price = symbolData.closeWindow[0]
            
            

            if self.Portfolio[symbol].Invested:
                
                if self.isLong:
                    condStopProfit = (current_price - self.buyInPrice) > self.stopProfitLevel
                    condStopLoss = (current_price - self.buyInPrice) < self.stopLossLevel
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
                FastisOverSlow = fastEMA > slowEMA #* self.tolerance
                SlowisOverFast = slowEMA > fastEMA #* self.tolerance
                FastisOverMedium = fastEMA > mediumEMA #* self.tolerance
                MediumisOverFast = mediumEMA > fastEMA #* self.tolerance
                PreviousFastBelowPreviousM = previousf < previousm 
                PreviousFastAbovePreviousM = previousf > previousm
                
                
                if FastisOverSlow and FastisOverMedium and PreviousFastBelowPreviousM and self.LondonSession: #
                    self.SetHoldings(symbol, 1)
                    # get buy-in price for trailing stop loss/profit
                    self.buyInPrice = current_price
                    # entered long position
                    self.isLong = True
                    self.Log(f"{self.Time} Entered Long Position at {current_price}")
                        
                if SlowisOverFast and MediumisOverFast  and PreviousFastAbovePreviousM and self.LondonSession: #
                    self.SetHoldings(symbol, -1)
                    # get sell-in price for trailing stop loss/profit
                    self.sellInPrice = current_price
                    # entered short position
                    self.isLong = False
                    self.Log(f"{self.Time} Entered Short Position at {current_price}")
                        
                    
class SymbolData:
    def __init__(self, algorithm, symbol):
        self.fastema = ExponentialMovingAverage(5)
        self.mediumema = ExponentialMovingAverage(20)
        self.slowema = ExponentialMovingAverage(50)
        
        self.slowWindow = RollingWindow[Decimal](2)   #setting the Rolling Window for the fast MACD indicator, takes two values
        algorithm.RegisterIndicator(symbol, self.slowema, timedelta(minutes=30))
        self.slowema.Updated += self.SlowEMAUpdated                    #Updating those two values
        
        self.fastWindow = RollingWindow[Decimal](2)   #setting the Rolling Window for the fast MACD indicator, takes two values
        algorithm.RegisterIndicator(symbol, self.fastema, timedelta(minutes=30))
        self.fastema.Updated += self.FastEMAUpdated                    #Updating those two values
        
        self.mediumWindow = RollingWindow[Decimal](2)   #setting the Rolling Window for the fast MACD indicator, takes two values
        algorithm.RegisterIndicator(symbol, self.mediumema, timedelta(minutes=30))
        self.mediumema.Updated += self.MediumEMAUpdated                    #Updating those two values
        
        self.closeWindow = RollingWindow[float](50)
       
        #Add consolidator to track rolling close prices..
        self.consolidator = QuoteBarConsolidator(30)
        self.consolidator.DataConsolidated += self.CloseUpdated
        algorithm.SubscriptionManager.AddConsolidator(symbol, self.consolidator)
        
    def SlowEMAUpdated (self, sender, updated):
        '''Event holder to update the MACD Rolling Window values.'''
        if self.slowema.IsReady:
            self.slowWindow.Add(updated)

    def FastEMAUpdated(self, sender, updated):
        '''Event holder to update the RSI Rolling Window values'''
        if self.fastema.IsReady:
            self.fastWindow.Add(updated)
            
    def MediumEMAUpdated(self, sender, updated):
        '''Event holder to update the RSI Rolling Window values'''
        if self.mediumema.IsReady:
            self.mediumWindow.Add(updated)
            
    def CloseUpdated(self, sender, bar):
        '''Event holder to update the close Rolling Window values'''
        self.closeWindow.Add(bar.Close)
        
    @property 
    def IsReady(self):
        return self.slowema.IsReady and self.fastema.IsReady and self.mediumema.IsReady and self.closeWindow.IsReady
  
    
