#region imports
from AlgorithmImports import *
#endregion
from datetime import datetime, timedelta


class FocusedLightBrownCamel(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2019, 1, 7)
        self.SetEndDate(2020, 1, 7)
        self.SetCash(100000)  # Set Strategy Cash
        # self.AddEquity("SPY", Resolution.Minute)
        

