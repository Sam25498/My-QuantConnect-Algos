#region imports
from AlgorithmImports import *
#endregion
class HyperActiveMagentaBat(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2010, 10, 11)  # Set Start Date
        self.SetEndDate(2020, 10, 11)
        self.SetCash(100000)  # Set Strategy Cash
        self.symbol = self.AddForex("EURUSD", Resolution.Hour , Market.Oanda).Symbol
        
        self.xATR = 3
        self.atr = self.ATR("EURUSD", 15, Resolution.Hour) 
        self.StopProfit = 0.01
        self.BigPointValue = 100000

        self.SetWarmUp(30) 
        
    def OnData(self, data):
        '''OnData event is the primary entry point for your algorithm. Each new data point will be pumped in here.
            Arguments:
                data: Slice object keyed by symbol containing the stock data
        '''
        if self.IsWarmingUp:
            return
        if not self.atr.IsReady:
            return
        
        symbol = self.symbol
        current_price = data[symbol].Close
        
        if not self.Portfolio.Invested:
            
            
            ########################################
            #         Your Entry Strategy          #
            #    self.SetHoldings(symbol, 1)       #
            #    self.buyInPrice = current_price   #
            ########################################
            self.SetHoldings(symbol, 1)
            self.isLong = True
            
        if self.Portfolio.Invested:
            ATR = self.atr.Current.Value
            current_price = data[symbol].Close
   
                

        

