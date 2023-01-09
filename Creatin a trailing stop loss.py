#how to create a moving stop loss to track the price action/profit            
            
            
self.stopLossLevel = -0.05 # stop loss percentage 
self.stopProfitLevel = 0.01# stop profit percentage
self.trailingSL = 0.05             



profit = self.Portfolio[symbol].UnrealizedProfit
#profit = self.Portfolio[symbol].NetProfit #Gets the unrealized profit as a percentage of holdings cost
cash = self.Portfolio.Cash #Sum of all currencies in account in US dollars (only unsettled cash)

if self.Portfolio[symbol].Invested:
            if self.isLong:
                        condStopLoss = (profit / cash) < self.stopLossLevel
                        #condTrailingStop = (profit / cash) < (self.stopLossLevel + self.trailingSL)
                        # if 0.06 > 0.05:
                        if (profit / cash) > self.trailingSL:
                                    self.stopLossLevel = self.stopLossLevel + self.trailingSL
                                    condTrailingStop = (profit / cash) < self.stopLossLevel
                                    self.trailingSL += 0.05
                                    
                        if condStopLoss:
                                    self.Liquidate(symbol)
                                    self.Log(f"{self.Time} Long Position Stop Loss at {current_price}")
                                    
                        if condTrailingStop:
                                    self.Liquidate(symbol)
                                    self.Log(f"{self.Time} Long Position Trailing Stop Loss at {current_price}")           
                                                
                        
                    
            else:
                        condStopLoss = (profit / cash) < self.stopLossLevel
                        #condTrailingStop = (profit / cash) < (self.stopLossLevel + self.trailingSL)
                        # if 0.06 > 0.05:
                        if (profit / cash) > self.trailingSL:
                                    self.stopLossLevel = self.stopLossLevel + self.trailingSL
                                    condTrailingStop = (profit / cash) < self.stopLossLevel
                                    self.trailingSL += 0.05
                                    
                        if condStopLoss:
                                    self.Liquidate(symbol)
                                    self.Log(f"{self.Time} Long Position Stop Loss at {current_price}")
                                    
                        if condTrailingStop:
                                    self.Liquidate(symbol)
                                    self.Log(f"{self.Time} Long Position Trailing Stop Loss at {current_price}")  
                   

            if self.Portfolio[symbol].Invested:
                
                if self.isLong:
                    condStopProfit = (profit / cash) > self.stopProfitLevel
                    condStopLoss = (profit / cash) < self.stopLossLevel
                    if condStopProfit:
                        self.Liquidate(symbol)
                        self.Log(f"{self.Time} Long Position Stop Profit at {current_price}")
                        
                    if condStopLoss:
                        self.Liquidate(symbol)
                        self.Log(f"{self.Time} Long Position Stop Loss at {current_price}")
                else:
                    condStopProfit = (profit / cash) > self.stopProfitLevel
                    condStopLoss = (profit / cash) < self.stopLossLevel
                    if condStopProfit:
                        self.Liquidate(symbol)
                        self.Log(f"{self.Time} Short Position Stop Profit at {current_price}")
                        
                    if condStopLoss:
                        self.Liquidate(symbol)
                        self.Log(f"{self.Time} Short Position Stop Loss at {current_price}")
            
