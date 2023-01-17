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
            

        
        
