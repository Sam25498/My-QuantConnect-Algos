
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
            
            
            def BullishDivergence(self, closeWindow, rsiWindow):
        
        self.rsiWindow = rsiWindow
        self.closeWindow = closeWindow
        lower_barrier = 30
        upper_barrier = 70
        
        width = 10
        
         #Bullish Divergence
        for i in range(14):
            try:
                if self.rsiWindow[i] < lower_barrier:
                    for a in range(i + 1, i + width):
                        if self.rsiWindow[a] > lower_barrier:
                            for r in range(a + 1, a + width):
                                if self.rsiWindow[r] < lower_barrier and self.rsiWindow[r] > self.rsiWindow[i] and self.closeWindow[r] < self.closeWindow[i]:
                                    
                                    for s in range(r + 1, r + width):
                                        if self.rsiWindow[s] > lower_barrier:
                                            #self.SetHoldings(self.ticker, 1)
                                            self.DivergenceBullish = True 
                                            return self.DivergenceBullish
                                            break
                                        
                                        else:
                                            continue
                                        
                                else:
                                    continue
                                
                        else:
                            continue
                        
                else:
                    continue
                
            except IndexError:
                pass
            
            
        
    
    def BearishDivergence(self, closeWindow, rsiWindow):
        
        self.rsiWindow = rsiWindow
        self.closeWindow = closeWindow
        lower_barrier = 30
        upper_barrier = 70
        
        width = 10
        #Bearish Divergence
        for i in range(14):
            try:
                if self.rsiWindow[i] > upper_barrier:
                    for a in range(i + 1, i + width):
                        if self.rsiWindow[a] < upper_barrier:
                            for r in range(a + 1, a + width):
                                if self.rsiWindow[r] > upper_barrier and self.rsiWindow[r] < self.rsiWindow[i] and self.closeWindow[r] > self.closeWindow[i]:
                                    
                                    for s in range(r + 1 , r + width):
                                        if self.rsiWindow[s] < upper_barrier:
                                            self.DivergenceBearish = True
                                            return self.DivergenceBearish
    
                                            break
                                        
                                        else:
                                            continue
                                        
                                else:
                                    continue
                                
                        else:
                            continue
                        
                else:
                    continue
                
            except IndexError:
                pass
        
          ''' 1. The width variable refers to the window which we’ll calculate the divergence on. For example, on the chart you may see a big divergence 
    spanning over multiple bars (big width) and you can also see small divergence that happen fast over a few bars (small width).Enlarging the width 
    will make the algorithm take into account those big ones. it's up to you to tweak it.  
    
    2. '''  
        
                
            
  
    
                
            
    
    
            
                    
                                
        
        
        
       

    
                   
