
class EnergeticFluorescentPinkRat(QCAlgorithm):
    NormalHoldingPeriod = None
    AbnormalHoldingPeriod = None
    DivergenceInProgress = None
    def Initialize(self):
        self.SetStartDate(2019, 7, 3)  # Set Start Date
        self.SetEndDate(2020,7, 3)
        self.SetCash(10000)  # Set Strategy Cash
        
        self.ticker = "USDJPY"
       
        

        #for ticker in tickers:
        symbol = self.AddForex(self.ticker, Resolution.Hour, Market.Oanda).Symbol
        self.rsi = self.RSI(symbol,14, Resolution.Hour)
        
        self.rsiWindow = RollingWindow[float](50)
        self.closeWindow = RollingWindow[float](50)
        
        self.WarmingUp = (50, Resolution.Hour)


    def OnData(self, data):
        '''OnData event is the primary entry point for your algorithm. Each new data point will be pumped in here.
            Arguments:
                data: Slice object keyed by symbol containing the stock data
        '''
        if self.IsWarmingUp:
            return
        
        self.closeWindow.Add(data[self.ticker].Close)
        self.rsiWindow.Add(self.rsi.Current.Value)
        current_price = data[self.ticker].Close
        
        
        if self.IsWarmingUp or not self.closeWindow.IsReady and not self.rsiWindow.IsReady:
                return
            
        
        bullish = self.BullishDivergence(self.closeWindow, self.rsiWindow)
        bearish = self.BearishDivergence(self.closeWindow, self.rsiWindow)
        
        if self.Portfolio[self.ticker].Invested:
            NormalHoldingPeriod = self.Time.weekday() == (self.DayTaken + 1) and self.Time.weekday() < 3 and self.Time.hour == self.TimeTaken #We are setting a 24h holding period
            AbnormalHoldingPeriod = self.Time.weekday() == self.DayTaken == 3 and self.Time.hour == 20  #We are setting a holding period for trades taken on friday, which we have less than 24hours to sell befor close of market
            ScndHoldingPeriod = (self.DayTaken + 1) == 7 and self.Time.weekday() == 0 and self.Time.hour == self.TimeTaken #This holding period is for trades taken at market open which is usually on Sunday UTC time hence the first condition .
            
            if NormalHoldingPeriod:
                self.Liquidate(self.ticker)
                self.Log(f"{self.Time} Position liquidated at Normal Holding Period ")
                
            if AbnormalHoldingPeriod:
                self.Liquidate(self.ticker)
                self.Log(f"{self.Time} Position liquidated at Abnormal Holding Period ")
                
            if ScndHoldingPeriod:
                self.Liquidate(self.ticker)
                self.Log(f"{self.Time} Position liquidated at Second Holding Period ")
                
        
        if not self.Portfolio[self.ticker].Invested:
            if bullish:
                self.SetHoldings(self.ticker, 1)
                self.DayTaken = self.Time.weekday()
                self.TimeTaken = self.Time.hour
                self.Log(f"{self.Time} Entered Long Position at {current_price} on {self.DayTaken}")
            else:
                pass
                
            if bearish:
                self.SetHoldings(self.ticker, -1)
                self.DayTaken = self.Time.weekday()
                self.TimeTaken = self.Time.hour
                self.Log(f"{self.Time} Entered Short Position at {current_price} on {self.DayTaken}")
            else:
                pass
                
            
    
    
            
                    
                                

    
                   
