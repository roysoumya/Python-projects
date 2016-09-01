'''
This is an implementation of a Genetic Algorithm(GA) in Python whose purpose was to 
generate a set of weight vectors and damping coefficients that would optimally 
normalize the data. 
This code was written as a part of the project "Intensity and Track Prediction 
for Cyclones in the North Indian Ocean Basin" during my summer internship at
IIT Kharagpur.
Steps :
1. The data is cleaned by removing certain useless columns.
2. Every GA must have a fitness function using which each chromosome of the 
current population is evaluated, and a fitness score is generated, which
indicates the probability of survival of the chromosome in the next generation.
   Here eval_func is the fitness function
3. Normalize function is used to convert(or normalize) the given weight vectors
(between 0 and 1) and damping coefficients(between 0.1 and 5.0)   
4. The last part of the program specifies the various parameters of the GA

Packages used :
1. Pyevolve for the GA
2. numpy for numpy_array for easier calculation
3. pandas : for the read_csv function
4. matplotlib : Not used here, but could be used to plot the evolution of the GA
plotting the Best, Mean and Median for each generation.
5. scikit-learn : For the k-means clustering, here k=25, i.e, the no. of states
in the Markov model.
'''
from pyevolve import G1DList,GSimpleGA,Consts,Initializators
from math import exp,sqrt
import csv as csv
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
import sklearn.metrics as sm

data =pd.read_csv('data/indian_data.csv',na_values='NA')

removals = [6,8,18,66,67,68,69,70]
data = data.drop(data.columns[removals], axis=1)
row_count, col_count = data.shape

#list(data) : Gives the cloumn names of the data frame

vmax_col = 4
useless_cols = 4
attribute_count = col_count - useless_cols
useful_col_start = useless_cols
cluster_count = 25
train_row_count = 800
genetic_test_row_count = 200
data_normal = data
prediction_interval_length = 21

mean_vector = range(useful_col_start,col_count)
sd_vector = range(useful_col_start,col_count)
min_vector = range(useful_col_start,col_count)
max_vector = range(useful_col_start,col_count)


def Normalize(u,v,x,y):
	a1 = 1 + exp(-1*v*y)
	a2 = exp(-1*v*x) - exp(-1*v*u)
	a3 = exp(-1*v*x) - exp(-1*v*y)
	a4 = 1 + exp(-1*v*u)
	return ((a1*a2)/(a3*a4))

def eval_func(chromosome):
	print 'Entering the fitness function'
	score = 0.0
	# Limiting the weight vectors between 0 and 1
	for i in range(len(chromosome)):
		if i < 60 :
			chromosome[i] = chromosome[i]/5.0
	print 'Chromosome : '
	print chromosome
	
	for i in chromosome:
		if i < 2.5 :
			score += 1.0
	
	weight_vector = chromosome[0:attribute_count]
	damping_vector = chromosome[attribute_count:(2*attribute_count)]
	data_normal = data
	for i in range(useful_col_start,col_count):
		arr = np.asarray(data_normal[[i]], dtype=np.float)
		mean_vector[i-useless_cols] = np.nanmean(arr)
		sd_vector[i-useless_cols] = np.nanstd(arr)
		arr = (arr - mean_vector[i-useless_cols])/sd_vector[i-useless_cols]
		min_vector[i-useless_cols] = np.nanmin(arr)
		max_vector[i-useless_cols] = np.nanmax(arr)
		
		for j in range(len(arr)):
			if np.isnan(arr[j]) == False:
				arr[j]= Normalize(arr[j], damping_vector[i-useless_cols], min_vector[i-useless_cols], max_vector[i-useless_cols])
		
		#arr = Normalize(arr, damping_vector[i-useless_cols], min_vector[i-useless_cols], max_vector[i-useless_cols])
		arr = arr*weight_vector[i-useless_cols]
		mean_of_normal = np.nanmean(arr)
		data_normal.iloc[:, i] = arr
		#Fill the missing values with the mean of the column, so that the mean and std. dev remain unchanged
		for j in range(len(data_normal)):
			if np.isnan(data_normal.iloc[j,i]):
				data_normal.iloc[j,i]= mean_of_normal
		
	cluster_input = data_normal.iloc[0:train_row_count,useful_col_start:col_count]
	#print 'Clustering starts'
	cl_res = KMeans(n_clusters=cluster_count, max_iter = 10000, random_state =121291)
	cl_res.fit(cluster_input)
	#print 'Clustering ends'
	#print 'Cluster labels'
	#print cl_res.labels_
	transition_matrix = np.zeros((cluster_count,cluster_count,cluster_count))
	x_prob_matrix = np.zeros((prediction_interval_length,cluster_count,cluster_count,cluster_count))
	
	for i in range(0,(train_row_count-1)):
		#Checking whether it belongs to the same cyclone
		if data_normal.iloc[i,0]==data_normal.iloc[(i+1),0]:
			transition_matrix[:,cl_res.labels_[i],cl_res.labels_[(i+1)]] = transition_matrix[:,cl_res.labels_[i],cl_res.labels_[(i+1)]] + 1
	
	for i in range(0,(train_row_count-2)):
		if (data_normal.iloc[i,0]==data_normal.iloc[(i+1),0]) and (data_normal.iloc[i,0]==data_normal.iloc[(i+2),0]):
			transition_matrix[(cl_res.labels_[i]),(cl_res.labels_[(i+1)]),(cl_res.labels_[(i+2)])] = transition_matrix[(cl_res.labels_[i]),(cl_res.labels_[(i+1)]),(cl_res.labels_[(i+2)])] + 1
	#print 'Original transmission matrix computation complete'
	original_transmission_matrix = transition_matrix
	for i in range(0,cluster_count):
		for j in range(0,cluster_count):
			transition_matrix[i,j,:] = transition_matrix[i,j,:]/np.sum(original_transmission_matrix[i,j,:])
			
	x_prob_matrix[1,:,:,:] = transition_matrix
	x_prob_matrix[2,:,:,:] = transition_matrix
	for i in range(2,prediction_interval_length):
		for q in range(0,cluster_count):
			for e in range(0,cluster_count):
				for o in range(0,cluster_count):
					x_prob_matrix[i,q,e,o] = 0
					for h in range(0,cluster_count):
						x_prob_matrix[i,q,e,o] = x_prob_matrix[i,q,e,o] + x_prob_matrix[(i-1),q,e,h]*x_prob_matrix[(i-1),e,h,o]
						
	#print 'Probability matrix computation complete'
	genetic_error = 0
	genetic_test_count = 0
	for k in range(train_row_count,(train_row_count + genetic_test_row_count)):
		test_row1 = k
		cluster_member1 = 1
		min_dist1 = 100000
		test_row2 = k + 1
		cluster_member2 = 1
		min_dist2 = 100000
		
		for i in range(0,cluster_count):
			dist1 = 0
			dist2 = 0
			for j in range(useful_col_start,col_count):
				dist1 = dist1 + (data_normal.iloc[test_row1,j] - cl_res.cluster_centers_[i, (j-useless_cols)])*(data_normal.iloc[test_row1,j] - cl_res.cluster_centers_[i, (j-useless_cols)])
				dist2 = dist2 + (data_normal.iloc[test_row2,j] - cl_res.cluster_centers_[i, (j-useless_cols)])*(data_normal.iloc[test_row2,j] - cl_res.cluster_centers_[i, (j-useless_cols)])
				if dist1 < min_dist1:
					min_dist1 = dist1
					cluster_member1 = i

				if dist2 < min_dist2:
					min_dist2 = dist2
					cluster_member2 = i

		for b in range(0,prediction_interval_length):
			if data_normal.iloc[test_row1, 0]!=data_normal.iloc[(test_row1 + b-1), 0]:
				break
			expected_intensity = 0
			for i in range(0,cluster_count):
				expected_intensity = expected_intensity + x_prob_matrix[b,cluster_member1,cluster_member2, i]*cl_res.cluster_centers_[i, 0]
				
			genetic_error = genetic_error + ((expected_intensity - data_normal.iloc[(test_row1+b-1),useful_col_start])*(expected_intensity - data_normal.iloc[(test_row1+b-1),useful_col_start]))
			genetic_test_count = genetic_test_count + 1

	res = genetic_error/genetic_test_count
	res = sqrt(res)
	#print 'Leaving the fitness function'
	return (1/res) 
	
#Genome instance
genome = G1DList.G1DList(120)
#genome.setParams(rangemin=0, rangemax=10)

#The evaluator function(i.e, the fitness/objective function)
genome.evaluator.set(eval_func)
#The initialization function, so that the initial population is made of real numbers
genome.initializator.set(Initializators.G1DListInitializatorReal)
genome.setParams(rangemin=0.1, rangemax=5.0)

ga = GSimpleGA.GSimpleGA(genome)
ga.setMinimax(Consts.minimaxType["maximize"])
ga.setPopulationSize(50)
ga.setCrossoverRate(0.80)
ga.setMutationRate(0.1)
ga.setElitism(True)
ga.setElitismReplacement(2)
ga.setGenerations(100)
print ga

#Starting the Genetic algorithm, freq_stats=1 means that the report generated at the end will be for each generation processed.
ga.evolve(freq_stats=1)
print ga.bestIndividual()
