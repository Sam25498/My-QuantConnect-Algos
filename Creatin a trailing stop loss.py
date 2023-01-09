            self.stopLossLevel = -0.05 # stop loss percentage 
            self.stopProfitLevel = 0.01# stop profit percentage

##############################################################################################

            profit = self.Portfolio[symbol].UnrealizedProfit
            #profit = self.Portfolio[symbol].NetProfit #Gets the unrealized profit as a percentage of holdings cost
            cash = self.Portfolio.Cash #Sum of all currencies in account in US dollars (only unsettled cash)

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
            
            profit = self.Portfolio[symbol].UnrealizedProfit
            #profit = self.Portfolio[symbol].NetProfit #Gets the unrealized profit as a percentage of holdings cost
            cash = self.Portfolio.Cash #Sum of all currencies in account in US dollars (only unsettled cash)

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
            
