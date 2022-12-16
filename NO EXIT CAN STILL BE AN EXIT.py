#region imports
from AlgorithmImports import *
#endregion
class UpgradedRedOrangeGorilla(QCAlgorithm):

    def Initialize(self):
        self.SetStartDate(2015, 12, 1)  # Set Start Date
        self.SetEndDate(2020, 12, 1)
        self.SetCash(100000)  # Set Strategy Cash
        #EURUSD", "USDJPY", "GBPUSD", "AUDUSD" "USDCAD",
        #"GBPJPY", "EURUSD", "AUDUSD", "EURJPY", "EURGBP"
        
        self.Data = {}

        for ticker in ["EURUSD","NZDUSD","USDJPY"]:
            symbol = self.AddForex(ticker, Resolution.Hour, Market.FXCM).Symbol
            self.Data[symbol] = SymbolData(self, symbol)
            
        
