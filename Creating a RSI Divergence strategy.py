
#I found this on the next link: Back Testing RSI Divergence Strategy on FX

#The author of the post used the exponential moving average for RSI calculation, using this piece of code:
'''
Assuming you have a pandas OHLC Dataframe downloaded from Metatrader 5 historical data. 
'''
# Get the difference in price from previous step
Data = pd.DataFrame(Data)
delta = Data.iloc[:, 3].diff()
delta = delta[1:]

# Make the positive gains (up) and negative gains (down) Series
up, down = delta.copy(), delta.copy()
up[up < 0] = 0
down[down > 0] = 0
roll_up = pd.stats.moments.ewma(up, lookback)
roll_down = pd.stats.moments.ewma(down.abs(), lookback)

# Calculate the SMA
roll_up = roll_up[lookback:]
roll_down = roll_down[lookback:]
Data = Data.iloc[lookback + 1:,].values

# Calculate the RSI based on SMA
RS = roll_up / roll_down
RSI = (100.0 - (100.0 / (1.0 + RS)))
RSI = np.array(RSI)
RSI = np.reshape(RSI, (-1, 1))

Data = np.concatenate((Data, RSI), axis = 1)

I found this on the next link: Back Testing RSI Divergence Strategy on FX

The author of the post used the exponential moving average for RSI calculation, using this piece of code:

'''
Assuming you have a pandas OHLC Dataframe downloaded from Metatrader 5 historical data. 
'''
# Get the difference in price from previous step
Data = pd.DataFrame(Data)
delta = Data.iloc[:, 3].diff()
delta = delta[1:]

# Make the positive gains (up) and negative gains (down) Series
up, down = delta.copy(), delta.copy()
up[up < 0] = 0
down[down > 0] = 0
roll_up = pd.stats.moments.ewma(up, lookback)
roll_down = pd.stats.moments.ewma(down.abs(), lookback)

# Calculate the SMA
roll_up = roll_up[lookback:]
roll_down = roll_down[lookback:]
Data = Data.iloc[lookback + 1:,].values

# Calculate the RSI based on SMA
RS = roll_up / roll_down
RSI = (100.0 - (100.0 / (1.0 + RS)))
RSI = np.array(RSI)
RSI = np.reshape(RSI, (-1, 1))

Data = np.concatenate((Data, RSI), axis = 1)
"""At this point we have an array with OHLC data and a fifth column that has the RSI in it. Then added the next two columns:

Column 6: Data[:, 5] will be for the bullish divergences and will have values of 0 or 1 (initiate buy).
Column 7: Data[:, 6] will be for the bearish divergences and will have values of 0 or -1 (initiate short).
using this variables:"""

lower_barrier = 30
upper_barrier = 70
width = 10
"""Here is the code:
"""

# Bullish Divergence
for i in range(len(Data)):
   try:
       if Data[i, 4] < lower_barrier: #If RSI < lower_barrier
           for a in range(i + 1, i + width): #for a in range(i + 1, i + 10)
               if Data[a, 4] > lower_barrier:
                    for r in range(a + 1, a + width):
                       if Data[r, 4] < lower_barrier and \
                        Data[r, 4] > Data[i, 4] and Data[r, 3] < Data[i, 3]:
                            for s in range(r + 1, r + width): 
                                if Data[s, 4] > lower_barrier:
                                    Data[s + 1, 5] = 1
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

# Bearish Divergence
for i in range(len(Data)):
   try:
       if Data[i, 4] > upper_barrier:
           for a in range(i + 1, i + width): 
               if Data[a, 4] < upper_barrier:
                   for r in range(a + 1, a + width):
                       if Data[r, 4] > upper_barrier and \
                       Data[r, 4] < Data[i, 4] and Data[r, 3] > Data[i, 3]:
                           for s in range(r + 1, r + width):
                               if Data[s, 4] < upper_barrier:
                                   Data[s + 1, 6] = -1
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
