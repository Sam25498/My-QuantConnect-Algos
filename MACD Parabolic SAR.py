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
            
