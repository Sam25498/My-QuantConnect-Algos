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
        self.SetCash(100000)  
        self.assets = [self.AddEquity(ticker, Resolution.Hour).Symbol for ticker in ASSETS]

        self.Schedule.On(self.DateRules.MonthStart('SPY'), self.TimeRules.AfterMarketOpen('SPY', 150), 
            self.Rebalance)
      
    def Rebalance(self):
        if self.Time.month not in MONTHES: return
            
        date = self.Time.strftime("%A %d. %B %Y")
        self.Debug(f"Execute trade at Date: {date}")
