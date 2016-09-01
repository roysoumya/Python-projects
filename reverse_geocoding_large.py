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

