#region imports
from AlgorithmImports import *
#endregion

from datetime import datetime,timedelta
import numpy as np

Macdlong = None
EmaLong = None
EmaShort = None
PSARLong = None
PSARShort = None

class CasualYellowDolphin(QCAlgorithm):


    def Initialize(self):
        self.SetStartDate(2020, 1, 1)  # Set Start Date
        self.SetEndDate(2020, 12, 30)
        self.SetCash(10000)  # Set Strategy Cash
        
        self.ticker = "EURUSD"
        # Rolling Windows to hold bar close data keyed by symbol.
        self.Data = {}

        #for self.ticker in self.tickers:
        symbol = self.AddForex(self.ticker, Resolution.Minute, Market.Oanda).Symbol
        self.Data[symbol] = SymbolData(self, symbol)
         
        self.tolerance = 0.0025

        self.stopLossLevel = -0.02 # stop loss percentage 
        self.stopProfitLevel = 0.01# stop profit percentage
            
        self.SetWarmUp(400, Resolution.Minute)
        
        
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
            EMA = symbolData.ema.Current.Value
            PSAR = symbolData.psar.Current.Value
            current_price = symbolData.closeWindow[0] #data[symbol].Close
            
            signalDeltaPercent = (MACD - MACD)/MACDfast
            
            if self.Portfolio[symbol].Invested:
                
                if self.isLong:
                    
                    condStopProfit = (current_price - self.buyInPrice)/self.buyInPrice > self.stopProfitLevel
                    condStopLoss = (current_price - self.buyInPrice)/self.buyInPrice < self.stopLossLevel
                    #PsarShort = current_price < PSAR
                    
                    if condStopProfit:
                        self.Liquidate(symbol)
                        self.Log(f"{self.Time} Long Position Stop Profit at {current_price}")

                    if condStopLoss:
                        self.Liquidate(symbol)
                        self.Log(f"{self.Time} Long Position Stop Loss at {current_price}")
                        
                    #if PsarShort:
                        #self.Liquidate(symbol)
                        #self.Log(f"{self.Time} Long Position exited due to Direction Change {current_price}")
                else:
                    condStopProfit = (self.sellInPrice - current_price)/self.sellInPrice > self.stopProfitLevel
                    condStopLoss = (self.sellInPrice - current_price)/self.sellInPrice < self.stopLossLevel
                    #PsarLong = current_price > PSAR 
                    
                    if condStopProfit:
                        self.Liquidate(symbol)
                        self.Log(f"{self.Time} Short Position Stop Profit at {current_price}")
                        
                    if condStopLoss:
                        self.Liquidate(symbol)
                        self.Log(f"{self.Time} Short Position Stop Loss at {current_price}")
                        
                   # if PsarLong:
                        #self.Liquidate(symbol)
                        #self.Log(f"{self.Time} Short Position exited due to Direction Change {current_price}")
            
            
            
            if not self.Portfolio[symbol].Invested:
                
            
                MacdLong = signalDeltaPercent > self.tolerance
                EmaLong = current_price > EMA 
                EmaShort = current_price < EMA
                PSARLong = PSAR < current_price 
                PSARShort = PSAR > current_price
               
                
                if EmaLong and Macdlong and PSARLong:
                    self.SetHoldings(symbol, 1)
                    # get buy-in price for trailing stop loss/profit
                    self.buyInPrice = current_price
                    # entered long position
                    self.isLong = True
                    self.Log(f"{self.Time} Entered Long Position at {current_price}")
                        
                if EmaShort and not Macdlong and PSARShort:
                    self.SetHoldings(symbol, -1)
                    # get sell-in price for trailing stop loss/profit
                    self.sellInPrice = current_price
                    # entered short position
                    self.isLong = False
                    self.Log(f"{self.Time} Entered Short Position at {current_price}")
                    
   
class SymbolData:
    def __init__(self, algorithm, symbol):
        self.macd = MovingAverageConvergenceDivergence(12,26,9)
        self.ema = ExponentialMovingAverage(200)
        self.psar = ParabolicStopAndReverse(0.02, 0.02, 0.2)

        
        self.macdWindow = RollingWindow[IndicatorDataPoint](2)   #setting the Rolling Window for the fast MACD indicator, takes two values
        algorithm.RegisterIndicator(symbol, self.macd, timedelta(minutes=30))
        self.macd.Updated += self.MacdUpdated                    #Updating those two values
        
        self.emaWindow = RollingWindow[IndicatorDataPoint](2)   #setting the Rolling Window for the EMA indicator, takes two values
        algorithm.RegisterIndicator(symbol, self.ema, timedelta(minutes=30))
        self.ema.Updated += self.EmaUpdated                    #Updating those two values
        
        self.closeWindow = RollingWindow[float](30)
        
        # Add consolidator to track rolling close prices
        self.consolidator = QuoteBarConsolidator(30)
        self.consolidator.DataConsolidated += self.CloseUpdated
        algorithm.SubscriptionManager.AddConsolidator(symbol, self.consolidator)
        
        self.psarWindow = RollingWindow[IndicatorDataPoint](2)   #setting the Rolling Window for the PSAR indicator, takes two values
        algorithm.RegisterIndicator(symbol, self.psar, timedelta(minutes=30))
        self.psar.Updated += self.PsarUpdated 
        
       
def MacdUpdated(self, sender, updated):
        '''Event holder to update the MACD Rolling Window values'''
        if self.macd.IsReady:
            self.macdWindow.Add(updated)

    def EmaUpdated(self, sender, updated):
        '''Event holder to update the EMA Rolling Window values'''
        if self.ema.IsReady:
            self.emaWindow.Add(updated)
            
    def PsarUpdated(self, sender, updated):
        '''Event holder to update the PSAR Rolling Window values'''
        if self.psar.IsReady:
            self.psarWindow.Add(updated)
            
    def CloseUpdated(self, sender, bar):
        '''Event holder to update the close Rolling Window values'''
        self.closeWindow.Add(bar.Close)
            
       
    @property 
    def IsReady(self):
        return self.macd.IsReady and self.ema.IsReady and self.psar.IsReady and self.closeWindow.IsReady   
        
        
  
                    



       
    
