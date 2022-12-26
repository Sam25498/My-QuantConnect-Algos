#region imports
from AlgorithmImports import *
#endregion
from datetime import datetime,timedelta
import numpy as np

Macdlong = None
AboveSupport = None
BelowResistance = None

class UpgradedTanPigeon(QCAlgorithm):


    def Initialize(self):
        self.SetStartDate(2021, 1, 1)  # Set Start Date
        self.SetEndDate(2021, 12, 30)
        self.SetCash(10000)  # Set Strategy Cash
        
        self.ticker = "USDCAD"
        # Rolling Windows to hold bar close data keyed by symbol.
        self.Data = {}

        #for self.ticker in self.tickers:
        symbol = self.AddForex(self.ticker, Resolution.Hour, Market.Oanda).Symbol
        self.Data[symbol] = SymbolData(self, symbol)
         
        self.tolerance = 0.0025
        self.toleranceR = 0.986761994
        self.toleranceS = 1.004000555
        self.stopLossLevel = -0.05 # stop loss percentage 
        self.stopProfitLevel = 0.01# stop profit percentage
            
        self.SetWarmUp(400, Resolution.Hour)
        
        
    def OnData(self, data):
        
        #if self.IsWarmingUp: #Data to warm up the algo is being collected.
           # return
        
        for symbol, symbolData in self.Data.items(): #Return the dictionary's key-value pairs:
            if not (data.ContainsKey(symbol) and data[symbol] is not None and symbolData.IsReady):
                continue
            
            if self.IsWarmingUp or not all([symbolData.IsReady for symbolData in self.Data.values()]):
                return
            
            MACD = symbolData.macd.Current.Value
            MACDfast = symbolData.macd.Fast.Current.Value
            RSI = symbolData.rsi.Current.Value
            current_price = data[symbol].Close#symbolData.closeWindow[0] #
            
            signalDeltaPercent = (MACD - MACD)/MACDfast
            
            supports1 = self.NextSupport(symbolData.lowWindow)
            resistances1 = self.NextResistance(symbolData.highWindow)
            supports2 = self.NextSupport(symbolData.lowWindowD)
            resistances2 = self.NextResistance(symbolData.highWindowD)
            
            #Combine the 4hour Supports levels with the Daily supports
            supports = supports1 + supports2
            resistances = resistances1 + resistances2
            
            #self.Log(f"Symbol: {symbol.Value} , Supports: {supports} , Resistances: {resistances}")
            
           
            #Filtering through the list of supports to be able to get the next support level.
            supports = sorted(supports, key= lambda x:x < current_price, reverse = True)
            
            #Filtering through the list of resistances to be able to get the next resistance level.
            resistances = sorted(resistances, key= lambda x:x > current_price, reverse = False)
            
            #self.Log(f"Symbol: {symbol.Value} , Supports: {supports} , Resistances: {resistances}")
            
            #Getting the next support level
            nextSupportLevel = supports[0]
            
            #Getting the next support level
            nextResistanceLevel = resistances[0]
            
            #if price is close to a support or resistance print or log  that resistance as well as that price
            self.Log(f"Symbol: {symbol.Value} , nextSupportLevel: {nextSupportLevel} , nextResistanceLevel: {nextResistanceLevel} ,current price:{current_price}")
            
            #s = np.mean(symbolData.highWindow) - np.mean(symbolData.lowWindow)
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
                
            
                MacdLong = signalDeltaPercent > self.tolerance
                AboveSupport = current_price > nextSupportLevel * self.toleranceS
                BelowResistance = current_price < nextResistanceLevel * self.toleranceR
                #tolerance = will be dependent on the minimum number of pips before a r/s level
                
                if RSI > 50 and Macdlong and BelowResistance:
                    self.SetHoldings(symbol, 1)
                    # get buy-in price for trailing stop loss/profit
                    self.buyInPrice = current_price
                    # entered long position
                    self.isLong = True
                    self.Log(f"{self.Time} Entered Long Position at {current_price}")
                        
                if RSI < 50  and not Macdlong and AboveSupport: 
                    self.SetHoldings(symbol, -1)
                    # get sell-in price for trailing stop loss/profit
                    self.sellInPrice = current_price
                    # entered short position
                    self.isLong = False
                    self.Log(f"{self.Time} Entered Short Position at {current_price}")
                    
                    
    def NextResistance(self, window, variation = 0.005, h = 3):
        
        series = window
        resistances = []
        
        maxima = []
        
        # finding maxima and minima by looking for hills/troughs locally
        for i in range(h, series.Size-h):
            if series[i] > series[i-1] and series[i] > series[i+1]  and series[i+1] > series[i+2] and series[i-1] > series[i-2] :
                maxima.append(series[i])
       
        # identifying maximas which are resistances
        for m in maxima:
            r = m * variation
            # maxima which are near each other
            commonLevel = [x for x in maxima if x > m - r and x < m + r]
            # if 2 or more maxima are clustered near an area, it is a resistance
            if len(commonLevel) > 1:
                # we pick the highest maxima if the cluster as our resistance
                level = max(commonLevel)
                if level not in resistances:
                    resistances.append(level)
        
        return resistances
                    
                    
    def NextSupport(self, window, variation = 0.005, h = 3): 
        
        series = window
        supports = []
       
        minima = []
        
        # finding maxima and minima by looking for hills/troughs locally..........
        for i in range(h, series.Size-h):
            if series[i] < series[i-1] and series[i] < series[i+1] and series[i+1] < series[i+2] and series[i-1] < series[i-2]:
                minima.append(series[i])
        
        # identify minima which are supports
        for l in minima:
            r = l * variation
            # minima which are near each other
            commonLevel = [x for x in minima if x > l - r and x < l + r]
            # if 2 or more minima are clustered near an area, it is a support.
            if len(commonLevel) > 1:
                # We pick the lowest minima of the cluster as our support
                level = min(commonLevel)
                if level not in supports:
                    supports.append(level)
                    
        return supports
                        
                    
class SymbolData:
    def __init__(self, algorithm, symbol):
        self.macd = MovingAverageConvergenceDivergence(12,26,9)
        self.rsi = RelativeStrengthIndex(14)
        
        self.macdWindow = RollingWindow[IndicatorDataPoint](2)   #setting the Rolling Window for the fast MACD indicator, takes two values
        algorithm.RegisterIndicator(symbol, self.macd, timedelta(hours=4))
        self.macd.Updated += self.MacdUpdated                    #Updating those two values
        
        self.rsiWindow = RollingWindow[IndicatorDataPoint](2)   #setting the Rolling Window for the slow SMA indicator, takes two values
        algorithm.RegisterIndicator(symbol, self.rsi, timedelta(hours=4))
        self.rsi.Updated += self.RsiUpdated                    #Updating those two values
        
        #self.closeWindow = RollingWindow[float](200)
        self.lowWindow = RollingWindow[float](200)
        self.highWindow = RollingWindow[float](200)
        self.lowWindowD = RollingWindow[float](40)
        self.highWindowD = RollingWindow[float](40)
        
        #Add consolidator to track rolling low prices..
        self.consolidator = QuoteBarConsolidator(4)
        self.consolidator.DataConsolidated += self.LowUpdated
        algorithm.SubscriptionManager.AddConsolidator(symbol, self.consolidator)
        
        #Add consolidator to track daily rolling low prices..
        self.consolidator = QuoteBarConsolidator(24)
        self.consolidator.DataConsolidated += self.LowDUpdated
        algorithm.SubscriptionManager.AddConsolidator(symbol, self.consolidator)
        
        #Add consolidator to track rolling high prices
        self.consolidator = QuoteBarConsolidator(4)
        self.consolidator.DataConsolidated += self.HighUpdated
        algorithm.SubscriptionManager.AddConsolidator(symbol, self.consolidator)
        
        #Add consolidator to track daily rolling high prices
        self.consolidator = QuoteBarConsolidator(24)
        self.consolidator.DataConsolidated += self.HighDUpdated
        algorithm.SubscriptionManager.AddConsolidator(symbol, self.consolidator)

        

    def MacdUpdated(self, sender, updated):
        '''Event holder to update the MACD Rolling Window values'''
        if self.macd.IsReady:
            self.macdWindow.Add(updated)

    def RsiUpdated(self, sender, updated):
        '''Event holder to update the RSI Rolling Window values'''
        if self.rsi.IsReady:
            self.rsiWindow.Add(updated)
            
    def LowUpdated(self, sender, bar):
        '''Event holder to update the 4 hour low Rolling Window values'''
        self.lowWindow.Add(bar.Low)
        
    def HighUpdated(self, sender, bar):
        '''Event holder to update the 4 hour high Rolling Window values'''
        self.highWindow.Add(bar.High)
        
    def LowDUpdated(self, sender, bar):
        '''Event holder to update the daily low Rolling Window values'''
        self.lowWindowD.Add(bar.Low)
        
    def HighDUpdated(self, sender, bar):
        '''Event holder to update the Daily high Rolling Window values'''
        self.highWindowD.Add(bar.High)
       
    @property 
    def IsReady(self):
        return self.macd.IsReady and self.rsi.IsReady and self.lowWindow.IsReady and self.highWindow.IsReady and self.lowWindowD.IsReady and self.highWindowD.IsReady      
       
  
