

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
    def OnData(self, data):
        # Get the current price
        price = self.Securities[self.symbol].Price

        # Check if we have a position in the market
        if self.Portfolio[self.symbol].Invested:
            # Check if we need to exit the position
            if self.psar.Current.Value > price:
                self.Sell(self.symbol, self.order_size)
        else:
             
            # Check if we need to enter the market
            if self.psar.Current.Value < price:
                self.Buy(self.symbol, self.order_size)
                self.StopMarketOrder(self.symbol, -self.order_size, self.stop_loss)
#Updated with new stop loss and take profit values
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

        # Set the order size, take profit, and stop loss
        self.order_size = 1000
        self.take_profit = 0.001
        self.stop_loss = 0.0005

    def OnData(self, data):
        # Get the current price
        price = self.Securities[self.symbol].Price

        # Check if we have a position in the market
        if self.Portfolio[self.symbol].Invested:
            # Check if we need to exit the position
            if self.psar.Current.Value > price:
                self.Sell(self.symbol, self.order_size)
        else:
            # Check if we need to enter the market
            if self.psar.Current.Value < price:
                self.Buy(self.symbol, self.order_size)
                self.StopMarketOrder(self.symbol, -self.order_size, self.stop_loss)
                self.LimitOrder(self.symbol, self.order_size, price + self.take_profit)


        


        


    

