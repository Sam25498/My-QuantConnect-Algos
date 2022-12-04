#region imports
from AlgorithmImports import *
#endregion
class SquareGreenBear(QCAlgorithm):


    def Initialize(self):
        self.SetStartDate(2015, 10, 15)  # Set Start Date
        self.SetEndDate(2020, 10, 15)
        self.SetCash(100000)  # Set Strategy Casho
        
        self.averages = { }
        for ticker in ["EURUSD", "AUDUSD","USDCHF"]:
            symbol = self.AddForex(ticker, Resolution.Daily, Market.Oanda).Symbol
            self.averages[symbol] = SymbolData(symbol)
    
            
        self.coarse_count = 10
        
     


    def OnData(self, data):
        '''OnData event is the primary entry point for your algorithm. Each new data point will be pumped in here.
            Arguments:
                data: Slice object keyed by symbol containing the stock data
        '''

        # if not self.Portfolio.Invested:
        #    self.SetHoldings("SPY", 1)
        # We are going to use a dictionary to refer the object that will keep the moving averages
        #["EURUSD", "AUDUSD","USDCHF"]
        for cf in self.averages.values() :
            if cf.Symbol not in self.averages:
