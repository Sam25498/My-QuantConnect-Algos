mports import * #endregion from datetime import datetime,timedelta import numpy as np import pandas as pd import math from typing import List, Tuple, Optional class SwimmingFluorescentPinkShark(QCAlgorithm): def Initialize(self): self.SetStartDate(2021, 1, 1) # Set Start Date self.SetEndDate(2021, 12, 31) self.SetCash(10000) # Set Strategy Cash self.ticker = "EURUSD" # Rolling Windows to hold bar close data keyed by symbol. self.Data = {} #for self.ticker in self.tickers: symbol = self.AddForex(self.ticker, Resolution.Hour, Market.Oanda).Symbol self.Data[symbol] = SymbolData(self, symbol) self.tolerance = 0.0025 self.toleranceR = 0.986761994 self.toleranceS = 1.004000555 self.stopLossLevel = -0.05 # stop loss percentage self.stopProfitLevel = 0.01# stop profit percentage self.SetWarmUp(50, Resolution.Hour) def OnData(self, data): #if self.IsWarmingUp: #Data to warm up the algo is being collected. # return for symbol, symbolData in self.Data.items(): #Return the dictionary's key-value pairs: if not (data.ContainsKey(symbol) and data[symbol] is not None and symbolData.IsReady): continue if self.IsWarmingUp or not all([symbolData.IsReady for symbolData in self.Data.values()]): return current_price = data[symbol].Close #symbolData.closeWindow[0] # RSI = symbolData.rsi.Current.Value lwlist = symbolData.lowWindow hwlist = symbolData.highWindow nlist = symbolData.rsiWindow #list(symbolData.rsiWindow) indlist = [] Lowlist = [] Highlist = [] for i in nlist: indlist.append(i.Value) for l in lwlist: Lowlist.append(l) for q in hwlist: Highlist.append(q) pls = self.pivot_low(indlist) phs = self.pivot_high(indlist) pli = self.pivot_low_index(indlist) phi = self.pivot_high_index(indlist) plls = self.pivot_low(Lowlist) plhs = self.pivot_high(Lowlist) phls = self.pivot_low(Highlist) phhs = self.pivot_high(Highlist) plFound = pd.isnull(pls) phFound = pd.isnull(phs) newpls = [i for i in pls if i != None] #Taking out the None values out of the list newphs = [j for j in phs if j != None] #Taking out the None values out of the list newlwpls = [r for r in plls if r != None] newlwphs = [u for u in plhs if u != None] newphls = [h for h in phls if h != None] newphhs = [j for j in phhs if j != None] r = self.second_false_values(pls, 1) dk = self.InRanges(pls, 1) self.Log(f"Rsi data: {indlist}, Quantity RSI: {len(indlist)}")#dk: {dk}, bars since pl1 happend: {r} pls: {pls} , newlwpls1: {newlwpls[1]}, newphs: {newphs}, newpls1: {newpls[1]} ") #LowList: {Lowlist}, plls: {plls}, phs: {phs},pls: {pls},phs: {phs}, phFound: {phFound}, LowList: {Lowlist}, #newpls: {newpls}, newphs: {newphs}, RSI: {RSI}, RSI value when pl is found: {ts}, Low Value when pl is found: {yq} , pls: {pls}, plFound: {plFound}, self.Log(f"Low Values: {Lowlist}, Quantity Lows: {len(Lowlist)}") self.Log(f"High Values: {Highlist}, Quantity Highs: {len(Highlist)}") #if dk: # self.Log(f"dk: {dk}") #self.Log(f"Symbol: {symbol.Value} , Supports: {supports} , Resistances: {resistances}") #if price is close to a support or resistance print or log that resistance as well as that price # #s = np.mean(symbolData.highWindow) - np.mean(symbolData.lowWindow) #oscHL = indlist[5] > self.valuewhen(plFound, newpls, 1) and self.InRange(plFound[1],plFound) #if oscHL: #self.Log(f"Time: {self.Time}, RSIhigh: {oscHL}") if self.Portfolio[symbol].Invested: if self.isLong: condStopProfit = (current_price - self.buyInPrice)/self.buyInPrice > self.stopProfitLevel condStopLoss = (current_price - self.buyInPrice)/self.buyInPrice < self.stopLossLevel if condStopProfit: self.Liquidate(symbol) self.Log(f"{self.Time} Regular Bull, Long Position Stop Profit at {current_price}") if condStopLoss: self.Liquidate(symbol) self.Log(f"{self.Time} Regular Bull, Long Position Stop Loss at {current_price}") else: condStopProfit = (self.sellInPrice - current_price)/self.sellInPrice > self.stopProfitLevel condStopLoss = (self.sellInPrice - current_price)/self.sellInPrice < self.stopLossLevel if condStopProfit: self.Liquidate(symbol) self.Log(f"{self.Time} Regular Bear, Short Position Stop Profit at {current_price}") if condStopLoss: self.Liquidate(symbol) self.Log(f"{self.Time} Regular Bear, Short Position Stop Loss at {current_price}") if not self.Portfolio[symbol].Invested: #Regular Bullish #// Osc/Rsi: Higher Low oscHL = indlist[5] > newpls[1] and dk # Price: Lower Low ll = self.extract_value_by_element(self, indlist, Lowlist, element = newpls[1]) priceLL = lwlist[5] < lwlist[pli[newlwpls[1]]] #yq = value of low when 2nd most recent pivot low is found bullCond = priceLL and oscHL and plFound[0] #Regular Bearish #// Osc/Rsi: Lower High oscLH = indlist[5] < newphs[1] and dk # Price: Higher High hh = self.extract_value_by_element(self, indlist, Highlist, element = newphs[1]) priceHH = hwlist[5] < hwlist[phi[newphs[1]]]#yq = value of low when 2nd most recent pivot low is found bearCond = priceHH and oscLH and phFound[0] if bullCond :#and not self.Portfolio[symbol].Invested self.SetHoldings(symbol, 1) # get buy-in price for trailing stop loss/profit self.buyInPrice = current_price # entered long position self.isLong = True self.notHidden = True self.Log(f"{self.Time} Regular BullCond Met, Entered Long Position at {current_price}") if bearCond : #and not self.Portfolio[symbol].Invested self.SetHoldings(symbol, -1) #get sell-in price for trailing stop loss/profit self.sellInPrice = current_price # entered short position self.isLong = False self.notHidden = True self.Log(f"{self.Time} Regular BearCond Met, Entered Short Position at {current_price}") def pivot_low(self, source, bars_left: int = 5, bars_right: int = 5, fill_null_values: bool = False) -> List[Optional[float]]: result = [] for i in range(len(source)): if i < bars_left + bars_right: result.append(None) continue is_pivot = True subset = source[i - bars_left - bars_right : i + bars_right + 1] value_to_check = subset[bars_left] for left_pivot in range(bars_left): if subset[left_pivot] < value_to_check: is_pivot = False break if is_pivot: for right_pivot in range(bars_left + 1, len(subset)): if subset[right_pivot] <= value_to_check: is_pivot = False break if is_pivot: x = subset.index(value_to_check) + 5 result.append(subset[x]) else: result.append(None) else: result.append(None) if fill_null_values: return fill_pivot_nulls(result) return result def pivot_low_index(source, bars_left: int = 5, bars_right: int = 5, fill_null_values: bool = False): """Gets the index of the pivot lows in the series source """ result = {} for i in range(len(source)): if i < bars_left + bars_right: pass continue is_pivot = True subset = source[i - bars_left - bars_right : i + bars_right + 1] value_to_check = subset[bars_left] for left_pivot in range(bars_left): if subset[left_pivot] < value_to_check: is_pivot = False break if is_pivot: for right_pivot in range(bars_left + 1, len(subset)): if subset[right_pivot] <= value_to_check: is_pivot = False break if is_pivot: ######## New Update ############ x = subset.index(value_to_check) + 5 ######## ****************** ############ result[subset[x]] = source.index(subset[x]) else: pass else: pass if fill_null_values: return fill_pivot_nulls(result) return result def pivot_high(self, source, bars_left: int = 5, bars_right: int = 5, fill_null_values: bool = False): #-> List[Optional[float]]: result = [] for i in range(len(source)): if i < bars_left + bars_right: result.append(None) continue is_pivot = True subset = source[i - bars_left - bars_right : i + bars_right + 1] value_to_check = subset[bars_left] for left_pivot in range(bars_left): if subset[left_pivot] > value_to_check: is_pivot = False break if is_pivot: for right_pivot in range(bars_left + 1, len(subset)): if subset[right_pivot] >= value_to_check: is_pivot = False break if is_pivot: x = subset.index(value_to_check) + 5 result.append(subset[x]) else: result.append(None) else: result.append(None) if fill_null_values: return fill_pivot_nulls(result) return result def pivot_high_index(source, bars_left: int = 5, bars_right: int = 5, fill_null_values: bool = False): """Gets the index of the pivot lows in the series source """ result = {} for i in range(len(source)): if i < bars_left + bars_right: pass continue is_pivot = True subset = source[i - bars_left - bars_right : i + bars_right + 1] value_to_check = subset[bars_left] for left_pivot in range(bars_left): if subset[left_pivot] < value_to_check: is_pivot = False break if is_pivot: for right_pivot in range(bars_left + 1, len(subset)): if subset[right_pivot] <= value_to_check: is_pivot = False break if is_pivot: ######## New Update ############ x = subset.index(value_to_check) + 5 ######## ****************** ############ result[subset[x]] = source.index(subset[x]) else: pass else: pass if fill_null_values: return fill_pivot_nulls(result) return result def barssince(self, condition, occurrence=0): ''' Impl of barssince RETURNS Number of bars since condition was true. REMARKS If the condition has never been met prior to the current bar, the function returns na. ''' cond_len = len(condition) occ = 0 since = 0 res = float('nan') while cond_len - (since + 1) >= 0: cond = condition[cond_len-(since+1)] # check for nan cond != cond == True when nan if cond and not cond != cond: if occ == occurrence: res = since break occ += 1 since += 1 return res def valuewhen(self, condition, source, occurrence=0): #print(valuewhen(plFound, Candle[5], 1)) ''' Impl of valuewhen + added occurrence RETURNS Source value when condition was true ''' res = float('nan') since = self.barssince(condition, occurrence) if since is not None: res = source[-(since + 1)] return res def fill_pivot_nulls(result: List[Optional[float]]) -> List[Optional[float]]: values = [] null_counter = 0 for item in result: if item is not None: values.append((item, null_counter)) null_counter = 0 else: null_counter += 1 final_list = [] is_first = True for i in range(len(values)): if is_first: for j in range(values[i][1]): final_list.append(None) final_list.append(values[i][0]) is_first = False else: current = values[i] previous = values[i - 1] count = current[1] for x in range(1, count + 1): if current[0] > previous[0]: amount_to_use = (current[0] - previous[0]) / (count + 1) final_list.append(round(previous[0] + (amount_to_use * x), 8)) else: final_list.append(previous[0]) return final_list def count_bars_since_condition(self, condition, dt): count = 0 condition_met = False for bar in dt: if condition: condition_met = True count = 0 elif condition_met: count += 1 return count def InRange(self, cond, data, rangeLower = 5, rangeUpper = 60): bars = self.count_bars_since_condition(cond, data) return rangeLower <= bars and bars <= rangeUpper def second_false_values(self, values, occurrence): lst = list(values) #my_lst = [] count = 0 my_lst = [i for i in lst if i != None] y = my_lst[occurrence] x = my_lst[0] indexY = lst.index(y) indexX = lst.index(x) diff = indexY - indexX return diff def InRanges(self, values, occurrence, rangeLower = 5, rangeUpper = 60): bars = self.second_false_values(values, occurrence) return rangeLower <= bars and bars <= rangeUpper def extract_value_by_element(self, list1, list2, element): """ Extract a value from list2 corresponding to the element in list1. Args: list1 (list of float): The list of elements to compare against. list2 (list of float): The list from which to extract the value. element (float): The element in list1 to use for comparison. Returns: float: The value from list2 corresponding to the element in list1. """ if element in list1: index = list1.index(element) if 0 <= index < len(list2): return list2[index] else: raise IndexError("Index out of range") else: raise ValueError("Element not found in list1") class SymbolData: def __init__(self, algorithm, symbol): self.rsi = RelativeStrengthIndex(14) self.rsiWindow = RollingWindow[IndicatorDataPoint](200) #setting the Rolling Window for the slow SMA indicator, takes two values algorithm.RegisterIndicator(symbol, self.rsi, timedelta(hours=1)) self.rsi.Updated += self.RsiUpdated #Updating those two valuesv self.closeWindow = RollingWindow[float](200) #Add consolidator to track rolling close prices.. self.consolidator = QuoteBarConsolidator(1) self.consolidator.DataConsolidated += self.CloseUpdated algorithm.SubscriptionManager.AddConsolidator(symbol, self.consolidator) self.lowWindow = RollingWindow[float](200) #Add consolidator to track rolling low prices.. self.consolidator = QuoteBarConsolidator(1) self.consolidator.DataConsolidated += self.LowUpdated algorithm.SubscriptionManager.AddConsolidator(symbol, self.consolidator) self.highWindow = RollingWindow[float](200) #Add consolidator to track rolling low prices.. self.consolidator = QuoteBarConsolidator(1) self.consolidator.DataConsolidated += self.HighUpdated algorithm.SubscriptionManager.AddConsolidator(symbol, self.consolidator) def CloseUpdated(self, sender, bar): '''Event holder to update the 4 hour Close Rolling Window values''' self.closeWindow.Add(bar.Close) def LowUpdated(self, sender, bar): '''Event holder to update the 4 hour low Rolling Window values''' self.lowWindow.Add(bar.Low) def HighUpdated(self, sender, bar): '''Event holder to update the 4 hour high Rolling Window values''' self.highWindow.Add(bar.High) def RsiUpdated(self, sender, updated): '''Event holder to update the RSI Rolling Window values''' if self.rsi.IsReady: self.rsiWindow.Add(updated) @property def IsReady(self): return self.closeWindow.IsReady and self.rsi.IsReady and self.lowWindow.IsReady and self.highWindow.IsReady #Backtest Results #risk to reward ratio self.stopLossLevel = -0.005 # stop loss percentage self.stopProfitLevel = 0.01# stop profit percentage #FY 2022 PSR 48.255% Sharpe Ratio0.731Total Trades 225 Average Win 1.10% Average Loss-0.56% 
Compounding Annual Return 9.752% Drawdown 3.800% Expectancy 0.149 Net Profit9.716% Loss Rate61%Win Rate39%Profit-Loss Ratio 1.96 Alpha0.045 Beta-0.046 Annual Standard Deviation 0.069Annual Variance 0.005 Information Ratio 0.817 Tracking Error0.222Treynor Ratio-1.096 Total Fees $0.00 Estimated Strategy Capacity $870000.00Lowest Capacity Asset EURUSD 8G Portfolio Turnover 63.50% #FY 2021 PSR 21.364% Sharpe Ratio 0.288 Total Trades 84Average Win 1.01% Average Loss-0.51% Compounding Annual Return2.106%Drawdown3.400% Expectancy0.106 Net Profit2.104%Loss Rate 63% Win Rate37%Profit-Loss Ratio1.97 Alpha 0.017 Beta-0.021 Annual Standard Deviation 0.045 Annual Variance0.002 Information Ratio-1.527 Tracking Error0.119Treynor Ratio-0.615Total Fees $0.00 Estimated Strategy Capacity $620000.00Lowest Capacity AssetEURUSD 8G Portfolio Turnover 23.76% #FY 2019 PSR 31.276% Sharpe Ratio-0.176 Total Trades 65 Average Win 1.05% Average Loss-0.53% Compounding Annual Return3.034%Drawdown4.200% Expectancy0.177 Net Profit3.031% 
#region imports
from AlgorithmImports import *
#endregion
from datetime import datetime,timedelta
import numpy as np
import pandas as pd
import math
from typing import List, Tuple, Optional



class SwimmingFluorescentPinkShark(QCAlgorithm):


    def Initialize(self):
        self.SetStartDate(2021, 1, 1)  # Set Start Date
        self.SetEndDate(2021, 12, 31)
        self.SetCash(10000)  # Set Strategy Cash
        
        self.ticker = "EURUSD"
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
            
            lwlist = symbolData.lowWindow
            hwlist = symbolData.highWindow
            
            nlist = symbolData.rsiWindow #list(symbolData.rsiWindow)
            indlist = []
            Lowlist = []
            Highlist = []
            for i in nlist:
                indlist.append(i.Value)

            for l in lwlist:
                Lowlist.append(l)
            
            for q in hwlist:
                Highlist.append(q)
                
            pls = self.pivot_low(indlist) 
            phs = self.pivot_high(indlist)
            
            pli = self.pivot_low_index(indlist)
            phi = self.pivot_high_index(indlist)

            plls = self.pivot_low(Lowlist)
            plhs = self.pivot_high(Lowlist)
            
            phls = self.pivot_low(Highlist)
            phhs = self.pivot_high(Highlist)

            plFound = pd.isnull(pls)
            phFound = pd.isnull(phs)
            
            newpls = [i for i in pls if i != None] #Taking out the None values out of the list
            newphs = [j for j in phs if j != None] #Taking out the None values out of the list
            
            newlwpls = [r for r in plls if r != None]
            newlwphs = [u for u in plhs if u != None]
            
            newphls = [h for h in phls if h != None]
            newphhs = [j for j in phhs if j != None]

        
            r = self.second_false_values(pls, 1)
            dk = self.InRanges(pls, 1)

            self.Log(f"Rsi data: {indlist}, Quantity RSI: {len(indlist)}")#dk: {dk}, bars since pl1 happend: {r} pls: {pls} , newlwpls1: {newlwpls[1]}, newphs: {newphs}, newpls1: {newpls[1]}  ") #LowList: {Lowlist}, plls: {plls}, phs: {phs},pls: {pls},phs: {phs}, phFound: {phFound},  LowList: {Lowlist}, #newpls: {newpls}, newphs: {newphs}, RSI: {RSI}, RSI value when pl is found: {ts}, Low Value when pl is found: {yq} , pls: {pls}, plFound: {plFound},
            self.Log(f"Low Values: {Lowlist}, Quantity Lows: {len(Lowlist)}")
            self.Log(f"High Values: {Highlist}, Quantity Highs: {len(Highlist)}")
            #if dk:
             #   self.Log(f"dk: {dk}")
            
            #self.Log(f"Symbol: {symbol.Value} , Supports: {supports} , Resistances: {resistances}")

            #if price is close to a support or resistance print or log  that resistance as well as that price
            #
            
            #s = np.mean(symbolData.highWindow) - np.mean(symbolData.lowWindow)
            #oscHL = indlist[5] > self.valuewhen(plFound, newpls, 1) and self.InRange(plFound[1],plFound)
            #if oscHL:
                #self.Log(f"Time: {self.Time}, RSIhigh: {oscHL}")
            if self.Portfolio[symbol].Invested:
                
                if self.isLong:
                    
                    condStopProfit = (current_price - self.buyInPrice)/self.buyInPrice > self.stopProfitLevel
                    condStopLoss = (current_price - self.buyInPrice)/self.buyInPrice < self.stopLossLevel
                    
                    if condStopProfit:
                        self.Liquidate(symbol)
                        self.Log(f"{self.Time} Regular Bull, Long Position Stop Profit at {current_price}")
                            
                    if condStopLoss:
                        self.Liquidate(symbol)
                        self.Log(f"{self.Time} Regular Bull, Long Position Stop Loss at {current_price}")


                else:
                    condStopProfit = (self.sellInPrice - current_price)/self.sellInPrice > self.stopProfitLevel
                    condStopLoss = (self.sellInPrice - current_price)/self.sellInPrice < self.stopLossLevel
                   
                    if condStopProfit:
                        self.Liquidate(symbol)
                        self.Log(f"{self.Time} Regular Bear, Short Position Stop Profit at {current_price}")
                            
                    if condStopLoss:
                        self.Liquidate(symbol)
                        self.Log(f"{self.Time} Regular Bear, Short Position Stop Loss at {current_price}")

                  
            
            if not self.Portfolio[symbol].Invested:

                #Regular Bullish
                #// Osc/Rsi: Higher Low

                oscHL = indlist[5] > newpls[1] and dk 
                # Price: Lower Low  
                ll = self.extract_value_by_element(self, indlist, Lowlist, element = newpls[1])
                priceLL = lwlist[5] < lwlist[pli[newlwpls[1]]]  #yq = value of low when 2nd most recent pivot low is found
                bullCond = priceLL and oscHL and plFound[0]
       
                
                #Regular Bearish
                #// Osc/Rsi: Lower High

                oscLH = indlist[5] < newphs[1] and dk 
                # Price: Higher High  
                hh = self.extract_value_by_element(self, indlist, Highlist, element = newphs[1])
                priceHH = hwlist[5] < hwlist[phi[newphs[1]]]#yq = value of low when 2nd most recent pivot low is found
                bearCond = priceHH and oscLH and phFound[0]
                
               

             
                
                if bullCond :#and not self.Portfolio[symbol].Invested
                    self.SetHoldings(symbol, 1)
                    # get buy-in price for trailing stop loss/profit
                    self.buyInPrice = current_price
                    # entered long position
                    self.isLong = True
                    self.notHidden = True
                    self.Log(f"{self.Time} Regular BullCond Met, Entered Long Position at {current_price}")
                        
                if bearCond : #and not self.Portfolio[symbol].Invested
                    self.SetHoldings(symbol, -1)
                    #get sell-in price for trailing stop loss/profit
                    self.sellInPrice = current_price
                    # entered short position
                    self.isLong = False
                    self.notHidden = True
                    self.Log(f"{self.Time} Regular BearCond Met, Entered Short Position at {current_price}")
                
              
                   

    def pivot_low(self, source, bars_left: int = 5, bars_right: int = 5, fill_null_values: bool = False) -> List[Optional[float]]:
        result = []
        for i in range(len(source)):
            if i < bars_left + bars_right:
                result.append(None)
                continue
            is_pivot = True
            subset = source[i - bars_left - bars_right : i + bars_right + 1]
            value_to_check = subset[bars_left]
            for left_pivot in range(bars_left):
                if subset[left_pivot] < value_to_check:
                    is_pivot = False
                    break
            if is_pivot:
                for right_pivot in range(bars_left + 1, len(subset)):
                    if subset[right_pivot] <= value_to_check:
                        is_pivot = False
                        break
                if is_pivot:
                    x = subset.index(value_to_check) + 5
                    result.append(subset[x])
                else:
                    result.append(None)
            else:
                result.append(None)
        if fill_null_values:
            return fill_pivot_nulls(result)
        return result
    
    def pivot_low_index(source, bars_left: int = 5, bars_right: int = 5, fill_null_values: bool = False):
        """Gets the index of the pivot lows in the series source """
        result = {}
        for i in range(len(source)):
            if i < bars_left + bars_right:
                pass
                continue
            is_pivot = True
            subset = source[i - bars_left - bars_right : i + bars_right + 1]
            value_to_check = subset[bars_left]
            for left_pivot in range(bars_left):
                if subset[left_pivot] < value_to_check:
                    is_pivot = False
                    break
            if is_pivot:
                for right_pivot in range(bars_left + 1, len(subset)):
                    if subset[right_pivot] <= value_to_check:
                        is_pivot = False
                        break
                if is_pivot:
                    ########        New Update          ############
                    x = subset.index(value_to_check) + 5
                    ########     ******************      ############
                    result[subset[x]] = source.index(subset[x])
                else:
                    pass
            else:
                pass
        if fill_null_values:
            return fill_pivot_nulls(result)
        return result
    
    def pivot_high(self, source, bars_left: int = 5, bars_right: int = 5, fill_null_values: bool = False): #-> List[Optional[float]]:
        result = []
        for i in range(len(source)):
            if i < bars_left + bars_right:
                result.append(None)
                continue
            is_pivot = True
            subset = source[i - bars_left - bars_right : i + bars_right + 1]
            value_to_check = subset[bars_left]
            for left_pivot in range(bars_left):
                if subset[left_pivot] > value_to_check:
                    is_pivot = False
                    break
            if is_pivot:
                for right_pivot in range(bars_left + 1, len(subset)):
                    if subset[right_pivot] >= value_to_check:
                        is_pivot = False
                        break
                if is_pivot:
                    x = subset.index(value_to_check) + 5
                    result.append(subset[x])
                else:
                    result.append(None)
            else:
                result.append(None)
        if fill_null_values:
            return fill_pivot_nulls(result)
        return result
    
    def pivot_high_index(source, bars_left: int = 5, bars_right: int = 5, fill_null_values: bool = False):
        """Gets the index of the pivot lows in the series source """
        result = {}
        for i in range(len(source)):
            if i < bars_left + bars_right:
                pass
                continue
            is_pivot = True
            subset = source[i - bars_left - bars_right : i + bars_right + 1]
            value_to_check = subset[bars_left]
            for left_pivot in range(bars_left):
                if subset[left_pivot] < value_to_check:
                    is_pivot = False
                    break
            if is_pivot:
                for right_pivot in range(bars_left + 1, len(subset)):
                    if subset[right_pivot] <= value_to_check:
                        is_pivot = False
                        break
                if is_pivot:
                    ########        New Update          ############
                    x = subset.index(value_to_check) + 5
                    ########     ******************      ############
                    result[subset[x]] = source.index(subset[x])
                else:
                    pass
            else:
                pass
        if fill_null_values:
            return fill_pivot_nulls(result)
        return result
    
    def barssince(self, condition, occurrence=0):
        '''
        Impl of barssince

        RETURNS
        Number of bars since condition was true.
        REMARKS
        If the condition has never been met prior to the current bar, the function returns na.
        '''
        cond_len = len(condition)
        occ = 0
        since = 0
        res = float('nan')
        while cond_len - (since + 1) >= 0:
            cond = condition[cond_len-(since+1)]
            # check for nan cond != cond == True when nan
            if cond and not cond != cond:
                if occ == occurrence:
                    res = since
                    break
                occ += 1
            since += 1
        return res

    
    def valuewhen(self, condition, source, occurrence=0): #print(valuewhen(plFound, Candle[5], 1))
        '''
        Impl of valuewhen
        + added occurrence

        RETURNS
        Source value when condition was true
        '''
        res = float('nan')
        since = self.barssince(condition, occurrence)
        if since is not None:
            res = source[-(since + 1)]
        return res  


    def fill_pivot_nulls(result: List[Optional[float]]) -> List[Optional[float]]:
        values = []
        null_counter = 0
        for item in result:
            if item is not None:
                values.append((item, null_counter))
                null_counter = 0
            else:
                null_counter += 1
        final_list = []
        is_first = True
        for i in range(len(values)):
            if is_first:
                for j in range(values[i][1]):
                    final_list.append(None)
                final_list.append(values[i][0])
                is_first = False
            else:
                current = values[i]
                previous = values[i - 1]
                count = current[1]
                for x in range(1, count + 1):
                    if current[0] > previous[0]:
                        amount_to_use = (current[0] - previous[0]) / (count + 1)
                        final_list.append(round(previous[0] + (amount_to_use * x), 8))
                    else:
                        final_list.append(previous[0])
        return final_list

    def count_bars_since_condition(self, condition, dt):
        count = 0
        condition_met = False
        for bar in dt:
            if condition:
                condition_met = True
                count = 0

            elif condition_met:
                count += 1
                
        return count

    def InRange(self, cond, data, rangeLower = 5, rangeUpper = 60):
        bars = self.count_bars_since_condition(cond, data)
        return rangeLower <= bars and bars <= rangeUpper

    def second_false_values(self, values, occurrence):
        lst = list(values)
        #my_lst = []
        count = 0
        my_lst = [i for i in lst if i != None]
            
        y = my_lst[occurrence]
        x = my_lst[0]
        indexY = lst.index(y)
        indexX = lst.index(x)
        diff = indexY - indexX
        return diff

    def InRanges(self, values, occurrence, rangeLower = 5, rangeUpper = 60):
        bars = self.second_false_values(values, occurrence)
        return rangeLower <= bars and bars <= rangeUpper  

    def extract_value_by_element(self, list1, list2, element):
        """
        Extract a value from list2 corresponding to the element in list1.

        Args:
        list1 (list of float): The list of elements to compare against.
        list2 (list of float): The list from which to extract the value.
        element (float): The element in list1 to use for comparison.

        Returns:
        float: The value from list2 corresponding to the element in list1.
        """
    
        if element in list1:
            index = list1.index(element)
            if 0 <= index < len(list2):
                return list2[index]
            else:
                raise IndexError("Index out of range")
        else:
            raise ValueError("Element not found in list1")


                    
class SymbolData:
    def __init__(self, algorithm, symbol):
        self.rsi = RelativeStrengthIndex(14)
        
        self.rsiWindow = RollingWindow[IndicatorDataPoint](200)   #setting the Rolling Window for the slow SMA indicator, takes two values
        algorithm.RegisterIndicator(symbol, self.rsi, timedelta(hours=1))
        self.rsi.Updated += self.RsiUpdated                    #Updating those two valuesv
             
        self.closeWindow = RollingWindow[float](200)       
        
        #Add consolidator to track rolling close prices..
        self.consolidator = QuoteBarConsolidator(1)
        self.consolidator.DataConsolidated += self.CloseUpdated
        algorithm.SubscriptionManager.AddConsolidator(symbol, self.consolidator)
        
        self.lowWindow = RollingWindow[float](200)
        
        #Add consolidator to track rolling low prices..
        self.consolidator = QuoteBarConsolidator(1)
        self.consolidator.DataConsolidated += self.LowUpdated
        algorithm.SubscriptionManager.AddConsolidator(symbol, self.consolidator)
        
        self.highWindow = RollingWindow[float](200)
        
        #Add consolidator to track rolling low prices..
        self.consolidator = QuoteBarConsolidator(1)
        self.consolidator.DataConsolidated += self.HighUpdated
        algorithm.SubscriptionManager.AddConsolidator(symbol, self.consolidator)
        
            
    def CloseUpdated(self, sender, bar):
        '''Event holder to update the 4 hour Close Rolling Window values'''
        self.closeWindow.Add(bar.Close)
    
    def LowUpdated(self, sender, bar):
        '''Event holder to update the 4 hour low Rolling Window values'''
        self.lowWindow.Add(bar.Low)
        
    def HighUpdated(self, sender, bar):
        '''Event holder to update the 4 hour high Rolling Window values'''
        self.highWindow.Add(bar.High)
        
    def RsiUpdated(self, sender, updated):
        '''Event holder to update the RSI Rolling Window values'''
        if self.rsi.IsReady:
            self.rsiWindow.Add(updated)
        
  
    @property 
    def IsReady(self):
        return  self.closeWindow.IsReady  and self.rsi.IsReady and self.lowWindow.IsReady and self.highWindow.IsReady

#Backtest Results 
#risk to reward ratio 
self.stopLossLevel = -0.005 # stop loss percentage 
self.stopProfitLevel = 0.01# stop profit percentage
#FY 2022
PSR 48.255% Sharpe Ratio0.731Total Trades 225 Average Win 1.10% Average Loss-0.56% Compounding Annual Return 9.752% Drawdown 3.800% Expectancy 0.149 Net Profit9.716% Loss Rate61%Win Rate39%Profit-Loss Ratio 1.96 Alpha0.045
Beta-0.046 Annual Standard Deviation 0.069Annual Variance 0.005 Information Ratio 0.817 Tracking Error0.222Treynor Ratio-1.096 Total Fees $0.00 Estimated Strategy Capacity $870000.00Lowest Capacity Asset EURUSD 8G
Portfolio Turnover 63.50%

#FY 2021
PSR 21.364% Sharpe Ratio 0.288 Total Trades 84Average Win 1.01% Average Loss-0.51% Compounding Annual Return2.106%Drawdown3.400% Expectancy0.106 Net Profit2.104%Loss Rate 63% Win Rate37%Profit-Loss Ratio1.97 Alpha 0.017
Beta-0.021 Annual Standard Deviation 0.045 Annual Variance0.002 Information Ratio-1.527 Tracking Error0.119Treynor Ratio-0.615Total Fees $0.00 Estimated Strategy Capacity $620000.00Lowest Capacity AssetEURUSD 8G
Portfolio Turnover 23.76%

#FY 2019
PSR 31.276% Sharpe Ratio-0.176 Total Trades 65 Average Win 1.05% Average Loss-0.53% Compounding Annual Return3.034%Drawdown4.200% Expectancy0.177 Net Profit3.031% Loss Rate 61% Win Rate 39% Profit-Loss Ratio 1.99 Alpha-0.006
Beta0.001 Annual Standard Deviation 0.036 Annual Variance 0.001 Information Ratio-1.742 Tracking Error 0.11 Treynor Ratio-7.132 Total Fees$0.00 Estimated Strategy Capacity$ 880000.00 Lowest Capacity AssetEURUSD 8G
Portfolio Turnover 18.02%
Rolling Statistics
