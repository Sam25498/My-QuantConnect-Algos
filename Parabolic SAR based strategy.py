

from quantconnect.algorithm import *

class ParabolicSARAlgorithm(QCAlgorithm):

    def Initialize(self):
        # Set the account size and leverage
        self.SetCash(10000)
        self.SetBrokerageModel(BrokerageName.OandaBrokerage)
        self.SetLeverage(50)

        
