#region imports
from AlgorithmImports import *
#endregion
class AlertSkyBlueLeopard(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2021, 2, 9)
        self.SetCash(100000) 
        self.AddEquity("SPY", Resolution.Minute)
       
        
