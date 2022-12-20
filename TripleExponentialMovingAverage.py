# In Initialize()
self.tema = TripleExponentialMovingAverage(period)
self.symbol = self.AddEquity("SPY").Symbol


# In OnData()
if data.ContainsKey(self.symbol):
    self.tema.Update(data[self.symbol].EndTime, data[self.symbol].High)
if self.tema.IsReady:
    
