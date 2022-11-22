#region imports
from AlgorithmImports import *
#endregion
# Trade twice a year
# ----------------------------------------
ASSETS = ['SPY', 'TLT']; MONTHES = [1, 7];
# ----------------------------------------
class PermanentPortfolio(QCAlgorithm):

