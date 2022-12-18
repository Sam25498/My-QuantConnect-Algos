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
        
        tickers = ["AAPL","AMZN","TSLA","FB"]
        #tickers = ["EURUSD","GBPUSD","AUDUSD","USDJPY"]
        for ticker in tickers:
            self.AddSecurity(SecurityType.Equity, ticker, Resolution.Daily)
            #self.symbols = [Symbol.Create(ticker, SecurityType.Equity, Market.USA) for ticker in tickers]
            self.fastsma = self.SMA(ticker, 30, Resolution.Daily) 
            self.slowsma = self.SMA(ticker, 90, Resolution.Daily)
            
        #self.AddAlpha(CustomSimpleMovingAverage())
            
        #self.SetRiskManagement(MaximumDrawdownPercentPerSecurity(0.20))
        #self.SetUniverseSelection(ManualUniverseSelectionModel(self.symbols))
        #self.SetExecution(ImmediateExecutionModel())


