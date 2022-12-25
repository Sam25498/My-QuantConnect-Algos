
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
        
        self.order_size = 1
        self.stop_loss = -5

    def OnData(self, data):
        
        #Get the current price and time
        price = self.Securities[self.symbol].Price
        time = self.Time

        # Check if we are in the London session (8am-5pm GMT)
        if time.hour >= 8 and time.hour < 17:
            # Check if we have a position in the market
            if self.Portfolio[self.symbol].Invested:
                # Check if we need to exit the position
                if self.psar.Current.Value > price:
                    self.Sell(self.symbol, self.order_size)
            else:
                # Check if we need to enter the market
                if self.psar.Current.Value < price:
                    self.Buy(self.symbol, self.order_size)
                    self.SetTrailingStop(self.symbol, self.stop_loss)
        else:
            # Close any open positions outside of the London session
            if self.Portfolio[self.symbol].Invested:
                self.Liquidate(self.symbol)

    
