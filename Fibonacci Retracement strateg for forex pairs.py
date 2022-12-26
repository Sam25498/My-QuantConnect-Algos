#region imports
from AlgorithmImports import *
#endregion
class TachyonDynamicShield(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2020, 2, 20)  # Set Start Date
        self.SetCash(100000)  # Set Strategy Cash
        
        tickers = ["GOOG", "AMZN", "AAPL", "TLT", "SPY", "JNJ", "TSLA", "NFLX"]
        self.symbolDict = {}
        
        for ticker in tickers:
            symbol = self.AddEquity(ticker, Resolution.Hour).Symbol
            self.symbolDict[symbol] = SymbolData(self, symbol)
        
        self.SetWarmUp(50)
        
    def OnData(self, data):
        
        if self.IsWarmingUp:
            return
        
        for symbol in self.symbolDict:
            sd = self.symbolDict[symbol]
            self.Log(f"Symbol: {symbol} with fibonacci retracements 38.2%: {sd.fib_38_2},  50.0%: {sd.fib_50_0},  61.8%: {sd.fib_61_8} AND MAX: {sd.max} and MIN: {sd.min}")
        
        
class SymbolData:
    
    
    def __init__(self, algorithm, symbol):
        
        self.algorithm = algorithm
        self.symbol = symbol
        
        self.max = algorithm.MAX(symbol, 50, Resolution.Hour)
        self.min = algorithm.MIN(symbol, 50, Resolution.Hour)
        
        self.fib_50_0 = 0
        self.fib_61_8 = 0
        self.fib_38_2 = 0
        
        
        self.min.Updated += self.OnMin
        
        
    def OnMin(self, sender, updated):
        height = self.max.Current.Value - self.min.Current.Value
        self.fib_50_0 = self.min.Current.Value + (height * 0.500)
        self.fib_61_8 = self.min.Current.Value + (height * 0.618)
        self.fib_38_2 = self.min.Current.Value + (height * 0.382)
        
############################################################################################################


#region imports
from AlgorithmImports import *
#endregion
class TachyonDynamicShield(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2020, 2, 20)  # Set Start Date
        self.SetCash(100000)  # Set Strategy Cash
        
        tickers = ["EURUSD", "USDJPY", "USDCAD", "USDCHF", "SPY", "AUDUSD"]
        self.symbolDict = {}
        
        for ticker in tickers:
            symbol = self.AddForex(ticker, Resolution.Hour).Symbol
            self.symbolDict[symbol] = SymbolData(self, symbol)
        
        self.SetWarmUp(50)
        
    def OnData(self, data):
        
        if self.IsWarmingUp:
            return
        
        for symbol in self.symbolDict:
            sd = self.symbolDict[symbol]
            self.Log(f"Symbol: {symbol} with fibonacci retracements 38.2%: {sd.fib_38_2},  
                     50.0%: {sd.fib_50_0},  
                     61.8%: {sd.fib_61_8} 
                     AND MAX: {sd.max} and 
                     MIN: {sd.min}")
            if self.Portfolio[symbol].Invested:
                     pass
            if not self.Portfolio[symbol].Invested:
                if sd.fib_61_8 > 1:
                     self.SetHoldings(symbol, 1)
                     
        
        
class SymbolData:
    
    
    def __init__(self, algorithm, symbol):
        
        self.algorithm = algorithm
        self.symbol = symbol
        
        self.max = algorithm.MAX(symbol, 50, Resolution.Hour)
        self.min = algorithm.MIN(symbol, 50, Resolution.Hour)
        
        self.fib_50_0 = 0
        self.fib_61_8 = 0
        self.fib_38_2 = 0
        
        
        self.min.Updated += self.OnMin
        
        
    def OnMin(self, sender, updated):
        height = self.max.Current.Value - self.min.Current.Value
        self.fib_50_0 = self.min.Current.Value + (height * 0.500)
        self.fib_61_8 = self.min.Current.Value + (height * 0.618)
        self.fib_38_2 = self.min.Current.Value + (height * 0.382)
