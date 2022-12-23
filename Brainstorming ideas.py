#Setting up condition to only trade during London sessions 

#B4 initializing the algorithm 
 
#B4 initializing the algorithm 
self.LondonSession = None
self.LondonSession = self.Time.hour > 6 and self.Time.hour < 10
