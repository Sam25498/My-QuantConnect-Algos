

from quantconnect.algorithm import *

class ParabolicSARAlgorithm(QCAlgorithm):

    def Initialize(self):
        # Set the account size and leverage
        self.SetCash(10000)
        self.SetBrokerageModel(BrokerageName.OandaBrokerage)
        self.SetLeverage(50)

        # Set the symbols and time frame
        self.symbol = "EURUSD"
        self.SetStartDate(2020, 1, 1)
        self.SetEndDate(2020, 12, 31)
        self.SetTimeZone("Europe/London")
        self.AddForex(self.symbol, Resolution.Minute, Market.Oanda)

        # Initialize the Parabolic SAR
        self.psar = self.PSAR(self.symbol, 0.01, 0.01)

        # Set the order size and stop loss
        self.order_size = 1000
        self.stop_loss = -50

    
