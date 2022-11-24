#region imports
from AlgorithmImports import *
#endregion
from datetime import timedelta, datetime
class FocusedYellowLemur(QCAlgorithm):


    def Initialize(self):
        self.SetStartDate(2015, 12, 1)  # Set Start Date
        self.SetEndDate(2016, 12, 1)
        self.SetCash(100000)  # Set Strategy Cash
       
        self.Data = {}

