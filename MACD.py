#region imports
from AlgorithmImports import *
#endregion
# Trade twice a year
# ----------------------------------------
ASSETS = ['SPY', 'TLT']; MONTHES = [1, 7];
# ----------------------------------------
class PermanentPortfolio(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2008, 1, 1)               
        self.SetEndDate(2021, 4, 10)
