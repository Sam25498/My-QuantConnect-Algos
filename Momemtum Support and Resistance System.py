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
    
        
        
