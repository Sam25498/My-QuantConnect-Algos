# In Initialize()
self.tema = TripleExponentialMovingAverage(period)
self.symbol = self.AddEquity("SPY").Symbol


# In OnData()
if data.ContainsKey(self.symbol):
