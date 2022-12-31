
"""
Created on Thu Dec 29 19:12:49 2022

@author: Sam
"""

#region imports
from AlgorithmImports import *
#endregion
from datetime import datetime,timedelta
import numpy as np


class CreativeYellowTapir(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2020,1, 30)  # Set Start Date
        self.SetEndDate(2020,12, 30)
        self.SetCash(10000)  # Set Strategy Cash
        
        self.ticker = "USDCAD"
        # Rolling Windows to hold bar close data keyed by symbol.
        self.Data = {}

        #for ticker in tickers:
        symbol = self.AddForex(self.ticker, Resolution.Minute, Market.Oanda).Symbol
        self.Data[symbol] = SymbolData(self, symbol)
         
        self.tolerance = 0.0025
        self.toleranceR = 0.986761994
        self.toleranceS = 1.004000555
        self.stopLossLevel = -0.05 # stop loss percentage 
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
            
            #MACD = symbolData.macd.Current.Value
            #MACDfast = symbolData.macd.Fast.Current.Value
            RSI = symbolData.rsi.Current.Value
            current_price = symbolData.closeWindow[0] #data[symbol].Close
            
            #signalDeltaPercent = (MACD - MACD)/MACDfast
            
            #supports = self.NextSupport(symbolData.lowWindow)
            close_hills = self.HillTops(symbolData.closeWindow)
            rsi_hills = self.HillTops(symbolData.rsiWindow)
            close_valleys = self.ValleyBottoms(symbolData.closeWindow)
            rsi_valleys = self.ValleyBottoms(symbolData.rsiWindow)
            #self.Log(f"Symbol: {symbol.Value} , Supports: {supports} , Resistances: {resistances}")
            
            #When confirmed a short trade is ripe
            divergence1 = close_hills[1] < close_hills[0] #and rsi_hills[1] > rsi_hills[0] #or rsi_valleys[1] > rsi_valleys[0]
            #When confirmed a long trade is ripe -je l'espere
            divergence2 = close_valleys[1] < close_valleys[0] #and rsi_hills[1] > rsi_hills[0] # or rsi_valleys[1] > rsi_valleys[0]
        
            #When confirmed a long trade is ripe
            convergence1 = close_hills[1] > close_hills[0] #and rsi_hills[1] < rsi_hills[0] #or rsi_valleys[1] < rsi_valleys[0]
            convergence2 = close_valleys[1] > close_valleys[0] #and rsi_hills[1] < rsi_hills[0] #or rsi_valleys[1] < rsi_valleys[0]
            #self.Log(f"Symbol: {symbol.Value} , Supports: {supports} , Resistances: {resistances}")
            
            #Getting the next support level
            #nextSupportLevel = supports[0]
            #London Session
            #LondonSession = 
            #Getting the next support level
            #nextResistanceLevel = resistances[0]
            
            #if price is close to a support or resistance print or log  that resistance as well as that price
            self.Log(f"Symbol: {symbol.Value} , close_hills[1]: {close_hills[1]} , close_hills[0]: {close_hills[0]} ,current price:{current_price}")
            
            
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
                
        
                
                if convergence2 or divergence2:
                    self.SetHoldings(symbol, 1)
                    # get buy-in price for trailing stop loss/profit
                    self.buyInPrice = current_price
                    # entered long position
                    self.isLong = True
                    self.Log(f"{self.Time} Entered Long Position at {current_price}")
                    #self.Log(f"Symbol: {symbol.Value} , close_hills[1]: {close_hills[1]} , close_hills[0]: {close_hills[0]} ,current price:{current_price}")
            
                        
                if divergence1 or convergence1: 
                    self.SetHoldings(symbol, -1)
                    # get sell-in price for trailing stop loss/profit
                    self.sellInPrice = current_price
                    # entered short position
                    self.isLong = False
                    self.Log(f"{self.Time} Entered Short Position at {current_price}")


