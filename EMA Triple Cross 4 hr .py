
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


    
    
