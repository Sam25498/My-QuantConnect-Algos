#region imports
from AlgorithmImports import *
#endregion
class SimpleMovingAverage(QCAlgorithm):
   
    def Initialize(self):
        self.SetStartDate(2019, 1, 7)
        self.SetEndDate(2020, 12, 7)
        self.SetCash(100000)
        self.AddForex("EURUSD", Resolution.Hour , Market.Oanda)
        self.SetBrokerageModel(BrokerageName.OandaBrokerage)
        
        self.fastsma = self.SMA("EURUSD", 30, Resolution.Hour) 
        self.slowsma = self.SMA("EURUSD", 90, Resolution.Hour)
        self.SetRiskManagement(MaximumDrawdownPercentPerSecurity(0.20))
        
        self.SetWarmUp(180)
        
        
    def OnData(self, data):
        
        #self.Plot("Indicators", "FastSMA", self.fastsma)
        #self.Plot("Indicators", "SlowSMA", self.slowsma)
        if self.IsWarmingUp:
            return
        
        if self.Portfolio.Invested:
            return
        
        if not self.slowsma.IsReady:
            return
        
        self.quantity = self.Portfolio["EURUSD"].Quantity
        #if self.slowsma.IsReady and self.quantity == 0 and 
        self.Debug(self.fastsma.Current.Value)
        
        if self.fastsma.Current.Value > self.slowsma.Current.Value:
            
            self.SetHoldings("EURUSD", 1)
            self.Debug("Purchased EURUSD")
                
        else:
            if self.slowsma.Current.Value < self.fastsma.Current.Value:
                self.Liquidate()
                self.Debug("Liquidate EURUSD")
                
                
    def OnEndOfDay(self):
        self.Plot("Data Chart", self.fastsma)
        self.Plot("Data Chart", self.slowsma)
        
        
#class SelectionData():
    #3. Update the constructor to accept a history array
    #def __init__(self, history):
        #self.slowsma = SMA(90)
        #self.fastsma =SMA(30)
        #self.history = history
        #4. Loop over the history data and update the indicators
        #for bar in history.itertuples():
            #self.slowsma.Update(bar.Index[1], bar.close)
            #self.fastsma.Update(bar.Index[1], bar.close)
    
    #def is_ready(self):
        #return self.slowsma.IsReady and self.fastsma.IsReady
    
    #def update(self, time, price):
        #self.fastsma.Update(time, price)
        #self.slowsma.Update(time, price)
