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
        

