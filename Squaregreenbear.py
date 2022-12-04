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
                self.averages[cf.Symbol ] = SymbolData(cf.Symbol)
                

            # Updates the SymbolData object with current EOD price
            avg = self.averages[cf.Symbol]
            avg.update(cf.Time, data[cf].Close)
            

        # Filter the values of the dict: we only want up-trending securities
        values = list(filter(lambda x: x.is_uptrend, self.averages.values()))
        # Sorts the values of the dict: we want those with greater difference between the moving averages
        values.sort(key=lambda x: x.scale, reverse=True)
        
        for x in values:
            if not self.Porfolio[x].Invested:
                self.SetHoldings(x.Symbol, 1)
            

class SymbolData(object):
    def __init__(self, symbol):
        self.symbol = symbol
         
        self.tolerance = 1.01
        self.fast = ExponentialMovingAverage(100)
        self.slow = ExponentialMovingAverage(300)
        self.is_uptrend = False
        self.scale = 0
    def update(self, time, value):
        if self.fast.Update(time, value) and self.slow.Update(time, value):
            fast = self.fast.Current.Value
            slow = self.slow.Current.Value
            self.is_uptrend = fast > slow * self.tolerance

        if self.is_uptrend:
            self.scale = (fast - slow) / ((fast + slow) / 2.0)    
