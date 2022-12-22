#region imports
from AlgorithmImports import *
#endregion
from datetime import datetime,timedelta
FastisOverSlow = None
SlowisOverFast = None
AboveLong = None
BelowLong = None

class DancingRedBull(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2015, 1, 30)  # Set Start Date
        self.SetEndDate(2020, 1, 30)
        self.SetCash(100000)  # Set Strategy Cash
        
        self.ticker = "EURUSD" #"USDJPY","GBPUSD",  "USDCAD","EURUSD".
        # Rolling Windows to hold bar close data keyed by symbol
        self.Data = {}

  

    
