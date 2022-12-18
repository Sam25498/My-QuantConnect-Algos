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

        
        self.SetAlpha(NullAlphaModel())
        self.SetPortfolioConstruction(NullPortfolioConstructionModel())
        #self.SetRiskManagement(NullRiskManagementModel())
        self.SetRiskManagement(MaximumDrawdownPercentPerSecurity(0.20))
        self.SetExecution(NullExecutionModel())
        self.SetWarmUp(180)
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

        
        self.SetAlpha(NullAlphaModel())
        self.SetPortfolioConstruction(NullPortfolioConstructionModel())
        #self.SetRiskManagement(NullRiskManagementModel())
        self.SetRiskManagement(MaximumDrawdownPercentPerSecurity(0.20))
        self.SetExecution(NullExecutionModel())
        self.SetWarmUp(180)


    def OnData(self, data):
        if self.IsWarmingUp:
            return
        
        if self.Portfolio.Invested:
            return
        
        if not self.slowsma.IsReady:
            return
        
    #def __init__(self,indicator):
       # self.indicator = indicator
        tickers = ["AAPL", "AMZN","TSLA","FB"]
        #tickers = ["EURUSD","GBPUSD","AUDUSD","USDJPY"]
        
    #def __gt__(self):
        for ticker in tickers:
            if self.fastsma.Current.Value > self.slowsma.Current.Value and not self.Portfolio[ticker].Invested:
                self.SetHoldings(ticker, 0.05)
                self.Debug("Purchased {}".format(ticker))
            
                
            if self.fastsma.Current.Value < self.slowsma.Current.Value and self.Portfolio[ticker].Invested:
                self.Liquidate(ticker)
                self.Debug("Sold {} position".format(ticker))
                
            
            #self.Plot("My Chart","fast indicator", self.fastsma.Value)
            #self.Plot("My Chart", "slow indicator",self.fastsma.Value)
            
            
                #insight = Insight.Price(ticker, timedelta(1), InsightDirection.Up)
                #return insight
class FocusedLightBrownCamel(QCAlgorithm):
        def OnData(self, data):
        if self.IsWarmingUp:
            return
        
        if self.Portfolio.Invested:
            return
        
      
        



