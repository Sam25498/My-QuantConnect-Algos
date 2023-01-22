#region imports
from AlgorithmImports import *
#endregion
from datetime import datetime,timedelta
import numpy as np


AboveSupport = None
BelowResistance = None


class SwimmingFluorescentPinkShark(QCAlgorithm):


    def Initialize(self):
        self.SetStartDate(2020, 1, 1)  # Set Start Date
        self.SetEndDate(2020, 12, 30)
        self.SetCash(10000)  # Set Strategy Cash
        
        self.ticker = "USDCAD"
        # Rolling Windows to hold bar close data keyed by symbol.
        self.Data = {}

        #for self.ticker in self.tickers:
        symbol = self.AddForex(self.ticker, Resolution.Hour, Market.Oanda).Symbol
        self.Data[symbol] = SymbolData(self, symbol)
         
        self.tolerance = 0.0025
        self.toleranceR = 0.986761994
        self.toleranceS = 1.004000555
        self.stopLossLevel = -0.05 # stop loss percentage 
        self.stopProfitLevel = 0.01# stop profit percentage
            
        self.SetWarmUp(50, Resolution.Hour)
        
      def OnData(self, data):
        
        #if self.IsWarmingUp: #Data to warm up the algo is being collected.
           # return
        
        for symbol, symbolData in self.Data.items(): #Return the dictionary's key-value pairs:
            if not (data.ContainsKey(symbol) and data[symbol] is not None and symbolData.IsReady):
                continue
            
            if self.IsWarmingUp or not all([symbolData.IsReady for symbolData in self.Data.values()]):
                return
            
            
            current_price = data[symbol].Close #symbolData.closeWindow[0] #
            RSI = symbolData.rsi.Current.Value


            
           
            
            supports = self.NextSupport(symbolData.closeWindow)
            resistances = self.NextResistance(symbolData.closeWindow)
            rsiList = self.calculate_rsi(symbolData.closeWindow)

            nlist = symbolData.rsiWindow #list(symbolData.rsiWindow)
            indlist = []
            for i in nlist:
                indlist.append(i.Value)

            self.Log(f"current_RSI:  {rsiList[0]}, RSI: {RSI} , RSIList: {indlist}, RSIList 1: {indlist[0]}") #, RSIList: {rsiList}v

            #supports2 = self.NextSupport(symbolData.lowWindowD)
            #resistances2 = self.NextResistance(symbolData.highWindowD)
            
            #Combine the 4hour Supports levels with the Daily supports
            #supports = supports1 + supports2
            #resistances = resistances1 + resistances2
            
            #self.Log(f"Symbol: {symbol.Value} , Supports: {supports} , Resistances: {resistances}")
            
           
            #Filtering through the list of supports to be able to get the next support level.
            supports = sorted(supports, key= lambda x:x < current_price, reverse = True)
            
            #Filtering through the list of resistances to be able to get the next resistance level.
            resistances = sorted(resistances, key= lambda x:x > current_price, reverse = False)
            
            #self.Log(f"Symbol: {symbol.Value} , Supports: {supports} , Resistances: {resistances}")
            
            #Getting the next support level
            nextSupportLevel = supports[0]
            
            #Getting the next support level
            nextResistanceLevel = resistances[0]
            
            #if price is close to a support or resistance print or log  that resistance as well as that price
            #self.Log(f"Symbol: {symbol.Value} , nextSupportLevel: {nextSupportLevel} , nextResistanceLevel: {nextResistanceLevel} ,current price:{current_price}")
            
            #s = np.mean(symbolData.highWindow) - np.mean(symbolData.lowWindow)
            if self.Portfolio[symbol].Invested:
                
                if self.isLong:
                    
                    condStopProfit = (current_price - self.buyInPrice)/self.buyInPrice > self.stopProfitLevel
                    condStopLoss = (current_price - self.buyInPrice)/self.buyInPrice < self.stopLossLevel
                    if condStopProfit:
                        self.Liquidate(symbol)
                        self.Log(f"{self.Time} Long Position Stop Profit at {current_price}")
                        
                    if condStopLoss:
                        self.Liquidate(symbol)
                        self.Log(f"{self.Time} Long Position Stop Loss at {current_price}")
                else:
                    condStopProfit = (self.sellInPrice - current_price)/self.sellInPrice > self.stopProfitLevel
                    condStopLoss = (self.sellInPrice - current_price)/self.sellInPrice < self.stopLossLevel
                    if condStopProfit:
                        self.Liquidate(symbol)
                        self.Log(f"{self.Time} Short Position Stop Profit at {current_price}")
                        
                    if condStopLoss:
                        self.Liquidate(symbol)
                        self.Log(f"{self.Time} Short Position Stop Loss at {current_price}")
            
            
            
            if not self.Portfolio[symbol].Invested:
                
            
               
                AboveSupport = current_price > nextSupportLevel * self.toleranceS
                BelowResistance = current_price < nextResistanceLevel * self.toleranceR
                #tolerance = will be dependent on the minimum number of pips before a r/s level
                
                if BelowResistance:
                    self.SetHoldings(symbol, 1)
                    # get buy-in price for trailing stop loss/profit
                    self.buyInPrice = current_price
                    # entered long position
                    self.isLong = True
                    self.Log(f"{self.Time} Entered Long Position at {current_price}")
                        
                if AboveSupport: 
                       
                    self.SetHoldings(symbol, -1)
                    # get sell-in price for trailing stop loss/profit
                    self.sellInPrice = current_price
                    # entered short position
                    self.isLong = False
                    self.Log(f"{self.Time} Entered Short Position at {current_price}")
                    
                    
      
    def NextResistance(self, window, variation = 0.005, h = 3):
        
        series = window
        resistances = []
        
        maxima = []
        
        # finding maxima and minima by looking for hills/troughs locally
        for i in range(h, series.Size-h):
            if series[i] > series[i-1] and series[i] > series[i+1]  and series[i+1] > series[i+2] and series[i-1] > series[i-2] :
                maxima.append(series[i])
       
        # identifying maximas which are resistances
        for m in maxima:
            r = m * variation
            # maxima which are near each other
            commonLevel = [x for x in maxima if x > m - r and x < m + r]
            # if 2 or more maxima are clustered near an area, it is a resistance
            if len(commonLevel) > 1:
                # we pick the highest maxima if the cluster as our resistance
                level = max(commonLevel)

                if level not in resistances:
                    resistances.append(level)

        return resistances
                    
                    
    def NextSupport(self, window, variation = 0.005, h = 3): 
        
        series = window
        supports = []
       
        minima = []
        
        # finding maxima and minima by looking for hills/troughs locally..........
        for i in range(h, series.Size-h):
            if series[i] < series[i-1] and series[i] < series[i+1] and series[i+1] < series[i+2] and series[i-1] < series[i-2]:
                minima.append(series[i])
        
        # identify minima which are supports
        for l in minima:
            r = l * variation
            # minima which are near each other
            commonLevel = [x for x in minima if x > l - r and x < l + r]
            # if 2 or more minima are clustered near an area, it is a support.
            if len(commonLevel) > 1:
                # We pick the lowest minima of the cluster as our support
                level = min(commonLevel)
                if level not in supports:
                    supports.append(level)
                    
        return supports

    def calculate_rsi(self, window):
        series = window
        # Initialize variables
        gain = 0
        loss = 0
        rsi_list = []
        # Iterate through the data to calculate the gain and loss
        for i in range(1, series.Size):
            if series[i] > series[i-1]:
                gain += series[i] - series[i-1]
            else:
                loss += series[i-1] - series[i]
        # Calculate the relative strength
        avg_gain = gain / 14
        avg_loss = loss / 14

        avg_loss = round(avg_loss, 10)
        rs = avg_gain / avg_loss
        # Calculate the RSI
        rsi = 100 - (100 / (1 + rs))
        rsi_list.append(rsi)
        for i in range(14, series.Size):
            if series[i] > series[i-1]:
                avg_gain = ((avg_gain * 13) + (series[i] - series[i-1])) / 14
                avg_loss = ((avg_loss * 13) + 0) / 14
            else:
                avg_gain = ((avg_gain * 13) + 0) / 14
                avg_loss = ((avg_loss * 13) + (series[i-1] - series[i])) / 14
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
            rsi_list.append(rsi)
        return rsi_list#[::-1]
    
 class SymbolData:
    def __init__(self, algorithm, symbol):
        self.rsi = RelativeStrengthIndex(14)
        
        self.rsiWindow = RollingWindow[IndicatorDataPoint](10)   #setting the Rolling Window for the slow SMA indicator, takes two values
        algorithm.RegisterIndicator(symbol, self.rsi, timedelta(hours=1))
        self.rsi.Updated += self.RsiUpdated                    #Updating those two valuesv
             
        self.closeWindow = RollingWindow[float](200)       
        
        #Add consolidator to track rolling close prices..
        self.consolidator = QuoteBarConsolidator(1)
        self.consolidator.DataConsolidated += self.CloseUpdated
        algorithm.SubscriptionManager.AddConsolidator(symbol, self.consolidator)

            
    def CloseUpdated(self, sender, bar):
        '''Event holder to update the 4 hour Close Rolling Window values'''
        self.closeWindow.Add(bar.Close)
    
    def RsiUpdated(self, sender, updated):
        '''Event holder to update the RSI Rolling Window values'''
        if self.rsi.IsReady:
            self.rsiWindow.Add(updated)
        
  
    @property 
    def IsReady(self):
        return  self.closeWindow.IsReady  and self.rsi.IsReady                       
                    
        
        ######## Logs :  Output #######
        
        2019-12-27 15:00:00 :	Launching analysis for 268a1d235d281643ced48e52f44f953c with LEAN Engine v2.5.0.0.15052
2019-12-27 15:00:00 :	Algorithm starting warm up...
2020-01-01 19:00:00 :	Algorithm finished warming up.
2020-01-09 22:00:00 :	current_RSI: 50.327504975021945, RSI: 53.49885270867954 , RSIList: [53.49885270867954, 55.81908920231306, 56.543628819671135, 54.91334203757303, 53.28602298570815, 50.88206217227009, 58.75574829911107, 67.08791964978705, 67.93028602435466, 75.28702830897068], RSIList 1: 53.49885270867954
2020-01-09 22:00:00 :	2020-01-09 22:00:00 Entered Short Position at 1.3062
2020-01-09 23:00:00 :	current_RSI: 51.030227070453414, RSI: 54.54702219621018 , RSIList: [54.54702219621018, 53.49885270867954, 55.81908920231306, 56.543628819671135, 54.91334203757303, 53.28602298570815, 50.88206217227009, 58.75574829911107, 67.08791964978705, 67.93028602435466], RSIList 1: 54.54702219621018
2020-01-10 00:00:00 :	current_RSI: 50.97638877750151, RSI: 54.35299300218888 , RSIList: [54.35299300218888, 54.54702219621018, 53.49885270867954, 55.81908920231306, 56.543628819671135, 54.91334203757303, 53.28602298570815, 50.88206217227009, 58.75574829911107, 67.08791964978705], RSIList 1: 54.35299300218888
2020-01-10 01:00:00 :	current_RSI: 50.71060122267736, RSI: 52.54154422258856 , RSIList: [52.54154422258856, 54.35299300218888, 54.54702219621018, 53.49885270867954, 55.81908920231306, 56.543628819671135, 54.91334203757303, 53.28602298570815, 50.88206217227009, 58.75574829911107], RSIList 1: 52.54154422258856
2020-01-10 02:00:00 :	current_RSI: 50.9990032975048, RSI: 48.986137008611514 , RSIList: [48.986137008611514, 52.54154422258856, 54.35299300218888, 54.54702219621018, 53.49885270867954, 55.81908920231306, 56.543628819671135, 54.91334203757303, 53.28602298570815, 50.88206217227009], RSIList 1: 48.986137008611514
2020-01-10 03:00:00 :	current_RSI: 50.7861060329068, RSI: 51.98529065023212 , RSIList: [51.98529065023212, 48.986137008611514, 52.54154422258856, 54.35299300218888, 54.54702219621018, 53.49885270867954, 55.81908920231306, 56.543628819671135, 54.91334203757303, 53.28602298570815], RSIList 1: 51.98529065023212
2020-01-10 04:00:00 :	current_RSI: 49.97401247401252, RSI: 58.777767005793045 , RSIList: [58.777767005793045, 51.98529065023212, 48.986137008611514, 52.54154422258856, 54.35299300218888, 54.54702219621018, 53.49885270867954, 55.81908920231306, 56.543628819671135, 54.91334203757303], RSIList 1: 58.777767005793045
2020-01-10 05:00:00 :	current_RSI: 49.84889537307203, RSI: 58.601847589058984 , RSIList: [58.601847589058984, 58.777767005793045, 51.98529065023212, 48.986137008611514, 52.54154422258856, 54.35299300218888, 54.54702219621018, 53.49885270867954, 55.81908920231306, 56.543628819671135], RSIList 1: 58.601847589058984
2020-01-10 06:00:00 :	current_RSI: 49.61622207478746, RSI: 61.43008255427422 , RSIList: [61.43008255427422, 58.601847589058984, 58.777767005793045, 51.98529065023212, 48.986137008611514, 52.54154422258856, 54.35299300218888, 54.54702219621018, 53.49885270867954, 55.81908920231306], RSIList 1: 61.43008255427422
2020-01-10 07:00:00 :	current_RSI: 49.92248883804244, RSI: 57.091228323980744 , RSIList: [57.091228323980744, 61.43008255427422, 58.601847589058984, 58.777767005793045, 51.98529065023212, 48.986137008611514, 52.54154422258856, 54.35299300218888, 54.54702219621018, 53.49885270867954], RSIList 1: 57.091228323980744
2020-01-10 08:00:00 :	current_RSI: 50.123520535763184, RSI: 50.33054612588009 , RSIList: [50.33054612588009, 57.091228323980744, 61.43008255427422, 58.601847589058984, 58.777767005793045, 51.98529065023212, 48.986137008611514, 52.54154422258856, 54.35299300218888, 54.54702219621018], RSIList 1: 50.33054612588009
2020-01-10 09:00:00 :	current_RSI: 51.78471091180272, RSI: 38.45451930619346 , RSIList: [38.45451930619346, 50.33054612588009, 57.091228323980744, 61.43008255427422, 58.601847589058984, 58.777767005793045, 51.98529065023212, 48.986137008611514, 52.54154422258856, 54.35299300218888], RSIList 1: 38.45451930619346
2020-01-10 10:00:00 :	current_RSI: 51.59991847549157, RSI: 40.59492720596854 , RSIList: [40.59492720596854, 38.45451930619346, 50.33054612588009, 57.091228323980744, 61.43008255427422, 58.601847589058984, 58.777767005793045, 51.98529065023212, 48.986137008611514, 52.54154422258856], RSIList 1: 40.59492720596854
2020-01-10 11:00:00 :	current_RSI: 51.06426243981251, RSI: 45.40211229757603 , RSIList: [45.40211229757603, 40.59492720596854, 38.45451930619346, 50.33054612588009, 57.091228323980744, 61.43008255427422, 58.601847589058984, 58.777767005793045, 51.98529065023212, 48.986137008611514], RSIList 1: 45.40211229757603
2020-01-10 12:00:00 :	current_RSI: 51.01015238783769, RSI: 46.033856242141184 , RSIList: [46.033856242141184, 45.40211229757603, 40.59492720596854, 38.45451930619346, 50.33054612588009, 57.091228323980744, 61.43008255427422, 58.601847589058984, 58.777767005793045, 51.98529065023212], RSIList 1: 46.033856242141184
2020-01-10 13:00:00 :	current_RSI: 51.04245939439441, RSI: 42.83153552572885 , RSIList: [42.83153552572885, 46.033856242141184, 45.40211229757603, 40.59492720596854, 38.45451930619346, 50.33054612588009, 57.091228323980744, 61.43008255427422, 58.601847589058984, 58.777767005793045], RSIList 1: 42.83153552572885
