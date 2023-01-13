# Bullish Divergence
for i in range(len(Data)):
   try:
       if Data[i, 4] < lower_barrier:
           for a in range(i + 1, i + width):
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
