#
# kmeans_1d_dp.py -- Performs 1-D k-means by a dynamic programming
#                    approach that is guaranteed to be optimal.
#                  
# implemented by Jacky ZL based on prior implementation in R
# IE Department, CUHK
# zl011@ie.cuhk.edu.hk
#				  
# Created on September 3, 2009

import math

def kmeans_1d_dp(X, K):
	"the optimal k-means for 1D data by a dynamic programming approach"
	
	unique_X = set(X)
	if len(unique_X) <= K:
		# the case that unique elements is less than cluster numbers
		r_centroids = sorted(list(unique_X))
		r_clusters  = [(r_centroids.index(item) + 1) for item in X]
		r_withinss  = 0
		r_sizes     = [X.count(item) for item in sorted(list(unique_X))]
		
		return len(unique_X), r_clusters, r_centroids, r_sizes, r_withinss
		
	# the case that operates the dynamic programming
	N = len(X)
	sorted_X = sorted(X)
	
	# define the two matrix D and B to be (K+1)*(N+1)
	D, B = [None]*(K+1), [None]*(K+1)
	for i in range(K+1):
		D[i] = [0, 0] + [None] * (N-1)
		B[i] = [0, 1] + [None] * (N-1)
		
	# fill the two matrix
	for k in range(1, K+1):
		mean_x1 = sorted_X[0]
		for i in range(2, N+1):
			if k == 1:
				D[1][i] = D[1][i-1] + math.pow(sorted_X[i-1] - mean_x1, 2)*(i-1)/i
				mean_x1 = ((i-1)*mean_x1 + sorted_X[i-1])/i
				B[1][i] = 1
			else:
				D[k][i] = -1
				d, mean_xj = 0, 0
				for j in sorted(range(1, i+1), reverse=True):
					d += math.pow(sorted_X[j-1] - mean_xj, 2)*(i-j)/(i-j+1)
					mean_xj = ((i-j)*mean_xj + sorted_X[j-1])/(i-j+1)
					if D[k][i] == -1:
						if j == 1:
							D[k][i] = d
							B[k][i] = j
						else:
							D[k][i] = d + D[k-1][j-1]
							B[k][i] = j
					elif j == 1 and d < D[k][i]:
						D[k][i] = d
						B[k][i] = j
					elif j > 1 and d + D[k-1][j-1] < D[k][i]:
						D[k][i] = d + D[k-1][j-1]
						B[k][i] = j
	
	# backtrack the cluster data points
	r_clusters    = [None] * N
	r_centroids   = [None] * K
	r_withinss    = [0] * K
	r_sizes       = [None] * K
	cluster_right = N
	for k in sorted(range(1, K+1), reverse=True):
		cluster_left = B[k][cluster_right]
		
		r_sizes[k-1] = cluster_right - cluster_left + 1
		sum = 0
		for i in range(cluster_left, cluster_right+1):
			r_clusters[i-1] = k
			sum += sorted_X[i-1]
		r_centroids[k-1] = sum/r_sizes[k-1]
			
		for i in range(cluster_left, cluster_right+1):
			r_withinss[k-1] += math.pow(sorted_X[i-1] - r_centroids[k-1], 2)
			
		if k > 1:
			cluster_right = cluster_left - 1
			
	# map the cluster result to original data input 
	index_dict = {}
	for i in range(N):
		index_dict[sorted_X[i]] = r_clusters[i]
	
	r_clusters = [index_dict[item] for item in X]
	
	return K, r_clusters, r_centroids, r_sizes, r_withinss
