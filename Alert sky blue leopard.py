#region imports
from AlgorithmImports import *
#endregion
class AlertSkyBlueLeopard(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2021, 2, 9)
        self.SetCash(100000) 
        self.AddEquity("SPY", Resolution.Minute)
       
  
    def OnData(self, data):
        ''' OnData event is the primary entry point for your algorithm. Each new data point will be pumped in here.
            Arguments:
                data: Slice object keyed by symbol containing the stock data
        '''
      
        # Check if we're not invested and then put portfolio 100% in the SPY ETF.      
        if not self.Portfolio.Invested:
           self.SetHoldings("SPY", 1)       
       
