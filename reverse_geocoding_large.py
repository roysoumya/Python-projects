'''
This program is used to reverse-geocode a large number of lat-long pairs. Reverse-geocoding means given a latitude-longitude
pair, generate the corresponding location's geographical details.
Steps :
1.The list of lat-long pairs are generated using the nested for-loops, where each grid covers a spatial projection of 2.5 x 2.5 
degrees.
2.The rg.search function is used to generate the results of reverse-geocoding the given lat-long pair. The list of results are
written to a Python dictionary.
3.For my own use, I wrote the results to a .csv file.
NOTE : These codes are strictly for educational purposes. Use them sensibly.
'''

import reverse_geocoder as rg
import csv
import time

results = []
for i in range(15):
    coordinates = []
    for j in range(15):
        lat = 40.0 - (i * 2.5)
        lon = 65.0 + (j * 2.5)
        pos_pair = [lat, lon]
        ans = rg.search(pos_pair)
        results = results + ans
        print ans
        time.sleep(0.5)

with open('Location_Grid.csv','wb') as location:
	loc_final = csv.DictWriter(location,results[0].keys())
	loc_final.writeheader()
	loc_final.writerows(results)
