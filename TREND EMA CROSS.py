#region imports
from AlgorithmImports import *
#endregion

from datetime import datetime,timedelta
PriceisOverSlow = None
SlowisOverPrice = None
PreviousPOverPEMA = None
PEMAOverPreviousP = None

class CryingRedLemur(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2019, 1, 30)  # Set Start Date
        self.SetEndDate(2020, 1, 30)
        self.SetCash(100000)  # Set Strategy Cash
        
        self.ticker = "USDCHF" #"USDJPY","GBPUSD",  "USDCAD","EURUSD".
        # Rolling Windows to hold bar close data keyed by symbol

