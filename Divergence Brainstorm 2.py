
pls = [None, None, None, None, None, None, None, None, 33.09129073595548, None, None, None, None, None, None, None, None, None, None, 45.83761605808045, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 34.46838617012884, None, None, None, None, None, None, None, None, 27.76239574519889, None, None, None, None, None, None, None, 45.47519913916435, None, None, None, None, None, 47.51447343755902, None, None, None, None, None, None, 35.20881642211308, None, None, None, None, None, None, None, None, None, None, None, 54.60223503638465, None, None, None, None, None, None, 49.60598040181985, None, None, None, None, None, None, 53.61216495927917, None, None, None, None, 53.71533435803753, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 46.86892658693192, None, None, None, None, None, None, None, 51.823666940711405, None, None, None, None, None, None, None, 61.17623729746359, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 35.093026245697715, None, None, None, None, None, None, 23.839029743727547, None, None, None, None, None, None, None, None, None, 18.60804752994565, None, None, None, None, None, None, None, None, 31.723516509494168, None, None, None, None, None, None, None, None, 29.318776482984692, None, None, None, None, 11.014429783438906]

Plfound = [ True  True  True  True  True  True  True  True False  True  True  True
  True  True  True  True  True  True  True False  True  True  True  True
  True  True  True  True  True  True  True  True  True  True False  True
  True  True  True  True  True  True  True False  True  True  True  True
  True  True  True False  True  True  True  True  True False  True  True
  True  True  True  True False  True  True  True  True  True  True  True
  True  True  True  True False  True  True  True  True  True  True False
  True  True  True  True  True  True False  True  True  True  True False
  True  True  True  True  True  True  True  True  True  True  True  True
  True  True False  True  True  True  True  True  True  True False  True
  True  True  True  True  True  True False  True  True  True  True  True
  True  True  True  True  True  True  True  True  True  True  True  True
  True False  True  True  True  True  True  True False  True  True  True
  True  True  True  True  True  True False  True  True  True  True  True
  True  True  True False  True  True  True  True  True  True  True  True
 False  True  True  True  True False]


def second_false_values(values):
  lst = list(values)
  my_lst = []
  count = 0
  for i in lst:
    if i != None:
       my_lst.append(i)
  y = my_lst[1]
  for h in values:
    if h != y:
      count += 1
  return count

print(second_false_values(pls)) #Output: 185 Not quite Accurate

def second_false_values(values):
    lst = list(values)
    my_lst = []
    count = 0
    for i in lst:
        if i != None:
            my_lst.append(i)
    y = my_lst[1]
    index = lst.index(y)
    return index 
  
