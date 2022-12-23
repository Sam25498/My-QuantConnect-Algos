#Setting up condition to only trade during London sessions 

#B4 initializing the algorithm 
 
#B4 initializing the algorithm 
self.LondonSession = None
#After initializing the algo
self.LondonSession = self.Time.hour > 6 and self.Time.hour < 10

# Inserting the condition 
if self.LondonSession and #condition 2 is met:
    #Enter into a trade
