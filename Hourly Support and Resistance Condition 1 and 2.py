#region imports
from AlgorithmImports import *
#endregion
from datetime import datetime,timedelta
import numpy as np


BelowSupport = None
AboveResistance = None


class SwimmingFluorescentPinkShark(QCAlgorithm):


    def Initialize(self):
        self.SetStartDate(2020, 1, 1)  # Set Start Date
        self.SetEndDate(2020, 12, 30)
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
            
        self.SetWarmUp(200, Resolution.Hour)
    def OnData(self, data):
        
        #if self.IsWarmingUp: #Data to warm up the algo is being collected.
           # return
        
        for symbol, symbolData in self.Data.items(): #Return the dictionary's key-value pairs:
            if not (data.ContainsKey(symbol) and data[symbol] is not None and symbolData.IsReady):
                continue
            
            if self.IsWarmingUp or not all([symbolData.IsReady for symbolData in self.Data.values()]):
                return
            
            
            current_price = data[symbol].Close #symbolData.closeWindow[0] #
         
            
            supports = self.NextSupport(symbolData.lowWindow)
            resistances = self.NextResistance(symbolData.highWindow)
            
           
            #Filtering through the list of supports to be able to get the next support level.
            supports = sorted(supports, key= lambda x:x < current_price, reverse = True)
            
            
            #Filtering through the list of resistances to be able to get the next resistance level.
            resistances = sorted(resistances, key= lambda x:x > current_price, reverse = False)

           
            self.Log(f"Symbol: {symbol.Value} , Supports: {supports} , Resistances: {resistances}")
            
            #Getting the next support level
            nextSupportLevel = supports[0] # max([num for num in supports if num < current_price])#
            
            #Getting the next support level
            nextResistanceLevel = resistances[0] #min([nom for nom in resistances if nom > current_price])#
            
            #if price is close to a support or resistance print or log  that resistance as well as that price
            self.Log(f"Symbol: {symbol.Value} , nextSupportLevel: {nextSupportLevel} , nextResistanceLevel: {nextResistanceLevel} ,current price:{current_price}")
            

        
            current_low = symbolData.lowWindow[0]
            current_high = symbolData.highWindow[0]
            previous_low = symbolData.lowWindow[1]
            previous_high = symbolData.highWindow[1] 

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
                
            
               
                BelowSupport = current_price < nextSupportLevel# * self.toleranceS
                AboveResistance = current_price > nextResistanceLevel #* self.toleranceR
                price_retestedB = current_low <= nextResistanceLevel and current_low < previous_low
                price_retestedS = current_high >= nextSupportLevel and current_high > previous_high
                #tolerance = will be dependent on the minimum number of pips before a r/s level
                
                if AboveResistance and price_retestedB:
                    self.SetHoldings(symbol, 1)
                    # get buy-in price for trailing stop loss/profit
                    self.buyInPrice = current_price
                    # entered long position
                    self.isLong = True
                    self.Log(f"{self.Time} Entered Long Position at {current_price}")
                        
                if BelowSupport and price_retestedS: 
                       
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
        #self.closeWindow = RollingWindow[float](200)
        self.lowWindow = RollingWindow[float](200)
        self.highWindow = RollingWindow[float](200)
        #self.lowWindowD = RollingWindow[float](40)
        #self.highWindowD = RollingWindow[float](40)
        
        #Add consolidator to track rolling low prices..
        self.consolidator = QuoteBarConsolidator(1)
        self.consolidator.DataConsolidated += self.LowUpdated
        algorithm.SubscriptionManager.AddConsolidator(symbol, self.consolidator) 
        
        #Add consolidator to track rolling high prices
        self.consolidator = QuoteBarConsolidator(1)
        self.consolidator.DataConsolidated += self.HighUpdated
        algorithm.SubscriptionManager.AddConsolidator(symbol, self.consolidator)

            
    def LowUpdated(self, sender, bar):
        '''Event holder to update the 1 hour low Rolling Window values'''
        self.lowWindow.Add(bar.Low)
        
    def HighUpdated(self, sender, bar):
        '''Event holder to update the 1 hour high Rolling Window values'''
        self.highWindow.Add(bar.High)
        
  
    @property 
    def IsReady(self):
        return self.lowWindow.IsReady and self.highWindow.IsReady 
    
    #Backtest Results FY2020
"""
Sharpe Ratio 0.178
Total Trades 23
Average Win 1.11%
Average Loss -5.40%
Compounding Annual Return 1.282%
Drawdown 7.600%
Expectancy 0.096
Net Profit 1.282%
Loss Rate 9%
Win Rate 91%
Profit-Loss Ratio 0.21
"""

#Backtest Results FY2021
"""
Sharpe Ratio 1.176
Total Trades 17
Average Win 1.03%
Average Loss 0%
Compounding Annual Return 8.767%
Drawdown 4.900%
Expectancy 0
Net Profit 8.742%
Loss Rate 0%
Win Rate 100%
Profit-Loss Ratio 0
"""

#Backtest Results FY2022
"""
Sharpe Ratio 0.191
Total Trades 19
Average Win 1.07%
Average Loss -4.87%
Compounding Annual Return 1.542%
Drawdown 7.900%
Expectancy 0.085
Net Profit 1.536% 
Loss Rate 11%
Win Rate89%
Profit-Loss Ratio0.22 """
         
