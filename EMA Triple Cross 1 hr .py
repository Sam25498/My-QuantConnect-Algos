
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
        
        self.ticker = "EURUSD"  #"USDJPY","GBPUSD",  "USDCAD","EURUSD".
        # Rolling Windows to hold bar close data keyed by symbol
        self.Data = {}

        #for self.ticker in self.tickers:
        symbol = self.AddForex(self.ticker , Resolution.Hour, Market.Oanda).Symbol
        self.Data[symbol] = SymbolData(self, symbol)
         
    
        self.tolerance = 1.001
     
        self.stopLossLevel = -0.005 #-0.01#-0.01# stop loss percentage 
        self.stopProfitLevel = 0.01 #0.02 #0.01#stop profit percentage
        
            
        self.SetWarmUp(50, Resolution.Hour)
        


    def OnData(self, data):
        
        if self.IsWarmingUp: #Data to warm up the algo is being collected.
            return
        
        self.LondonSession = self.Time.hour > 6 and self.Time.hour < 14

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
            
            profit = self.Portfolio[symbol].UnrealizedProfit
            #profit = self.Portfolio[symbol].NetProfit #Gets the unrealized profit as a percentage of holdings cost
            cash = self.Portfolio.Cash #Sum of all currencies in account in US dollars (only unsettled cash)

            if self.Portfolio[symbol].Invested:
                
                if self.isLong:
                    condStopProfit = (profit / cash) > self.stopProfitLevel
                    condStopLoss = (profit / cash) < self.stopLossLevel
                    if condStopProfit:
                        self.Liquidate(symbol)
                        self.Log(f"{self.Time} Long Position Stop Profit at {current_price}")
                        
                    if condStopLoss:
                        self.Liquidate(symbol)
                        self.Log(f"{self.Time} Long Position Stop Loss at {current_price}")
                else:
                    condStopProfit = (profit / cash) > self.stopProfitLevel
                    condStopLoss = (profit / cash) < self.stopLossLevel
                    if condStopProfit:
                        self.Liquidate(symbol)
                        self.Log(f"{self.Time} Short Position Stop Profit at {current_price}")
                        
                    if condStopLoss:
                        self.Liquidate(symbol)
                        self.Log(f"{self.Time} Short Position Stop Loss at {current_price}")
            
            
            

    
