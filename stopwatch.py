#A Simple Stopwatch timer

import time

#Display the lap number along with the times giving to output for each laps
print('Press Enter to start the game')
raw_input()
print('Timer Started')
time_now = time.time()
last_time = time_now
lapNum=1

#Iterate over the different laps
try:
	while True:
		raw_input()
		lap_time = round(time.time()-last_time,2)
		total_time = round(time.time()-time_now,2)
		print('Lap {0}; Duration {1}; From Start {2}').format(lapNum,lap_time,total_time)
		lapNum+=1
		last_time = time.time()
except KeyboardInterrupt:
	print('\nWork completed.')
	
	

