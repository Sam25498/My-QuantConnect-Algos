#region imports
from AlgorithmImports import *
#endregion
from datetime import datetime,timedelta
import numpy as np
class DancingYellowGreenAlpaca(QCAlgorithm):


    def Initialize(self):
        self.SetStartDate(2020, 1, 30)  # Set Start Date
        self.SetCash(100000)  # Set Strategy Cash
     
        tickers = ["EURUSD","USDCAD"]
        # Rolling Windows to hold bar close data keyed by symbol
        self.closingData = {}
        self.SMA45 = {}
        for ticker in tickers:
