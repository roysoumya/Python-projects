'''
This program demonstrates how to create a Simple Stop-watch Timer and illustrates how to include Keyboard inputs like in our case
: Enter, to control as well as calculate the time elapsed from the last time Enter was hit and also shows the time elapsed from
the beginning of the program.
NOTE : These codes are strictly for educational purposes. Use them sensibly.
'''

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
