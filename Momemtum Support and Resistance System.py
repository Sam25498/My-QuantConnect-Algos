#region imports
from AlgorithmImports import *
#endregion
from datetime import datetime,timedelta
import numpy as np
#from daily_support_resitance import *
#from fourhr_support_resistance import *

class MeasuredApricot(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2020, 1, 30)  # Set Start Date
        self.SetEndDate(2020, 12, 30)
        self.SetCash(100000)  # Set Strategy Cash
        
        self.ticker = "USDCAD"
        # Rolling Windows to hold bar close data keyed by symbol
        self.Data = {}

        #for ticker in tickers:
        symbol = self.AddForex(self.ticker, Resolution.Hour, Market.Oanda).Symbol
        self.Data[symbol] = SymbolData(self, symbol)
            
        self.tolerance = 0.0025
            
        self.stopLossLevel = -0.05 # stop loss percentage 
        self.stopProfitLevel = 0.01# stop profit percentage
        
        self.SupportResistance = SupportResistance(self, self.ticker)
            
        self.SetWarmUp(50, Resolution.Hour)
        
    def MarketClose(self):
        self.SupportResistance.Reset()


    def OnData(self, data):
        
        if self.IsWarmingUp: #Data to warm up the algo is being collected.
            return
        
        for symbol, symbolData in self.Data.items(): #Return the dictionary's key-value pairs:
            if not (data.ContainsKey(symbol) and data[symbol] is not None and symbolData.IsReady):
                continue
            
            MACD = symbolData.macd.Current.Value
            MACDfast = symbolData.macd.Fast.Current.Value
            RSI = symbolData.rsi.Current.Value
            current_price = data[symbol].Close
            
            signalDeltaPercent = (MACD - MACD)/MACDfast
            #nextSupportZone =
            #nextResistanceZone = 
            support = self.SupportResistance.NextSupport()
            resistance = self.SupportResistance.NextResistance()
            

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
                #Above Support = current_price > closestSupportZone * tolerance(1.01)
                #Below Resistance = current_price < closestResistanceZone * tolerance
                # tolerance = will be dependent on the minimum number of pips before a r/s level
     
              
                
                if RSI > 50 and Macdlong: #Below Resistance:
                    self.SetHoldings(symbol, 1)
                    # get buy-in price for trailing stop loss/profit
                    self.buyInPrice = current_price
                    # entered long position
                    self.isLong = True
                    self.Log(f"{self.Time} Entered Long Position at {current_price}")
                    
                        
                if RSI < 50  and not Macdlong: #Above Support: 
                    self.SetHoldings(symbol, -1)
                    # get sell-in price for trailing stop loss/profit
                    self.sellInPrice = current_price
                    # entered short position
                    self.isLong = False
                    self.Log(f"{self.Time} Entered Short Position at {current_price}")
                        
                    
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
        
        self.closeWindow = RollingWindow[float](21)
        
        # Add consolidator to track rolling close prices
        self.consolidator = QuoteBarConsolidator(4)
        self.consolidator.DataConsolidated += self.CloseUpdated
        algorithm.SubscriptionManager.AddConsolidator(symbol, self.consolidator)
        

    def MacdUpdated(self, sender, updated):
        '''Event holder to update the MACD Rolling Window values'''
        if self.macd.IsReady:
            self.macdWindow.Add(updated)

    def RsiUpdated(self, sender, updated):
        '''Event holder to update the RSI Rolling Window values'''
        if self.rsi.IsReady:
            self.rsiWindow.Add(updated)
            
            
    def CloseUpdated(self, sender, bar):
        '''Event holder to update the close Rolling Window values'''
        self.closeWindow.Add(bar.Close)
       
    @property 
    def IsReady(self):
        return self.macd.IsReady and self.rsi.IsReady and self.closeWindow.IsReady     
         
                      
     
