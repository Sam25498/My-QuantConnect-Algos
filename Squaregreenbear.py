#region imports
from AlgorithmImports import *
#endregion
class SquareGreenBear(QCAlgorithm):


    def Initialize(self):
        self.SetStartDate(2015, 10, 15)  # Set Start Date
        self.SetEndDate(2020, 10, 15)
        self.SetCash(100000)  # Set Strategy Casho
        
