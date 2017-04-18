# Utilities for sampling parameter values – not used currently

import numpy as np

# pre-computed
# redo these if we change range, number of buckets, or kill_var
buckets = [(0.006, 0.01016), (0.01016, 0.01432), (0.01432, 0.01848), (0.01848, 0.02264), (0.02264, 0.0268), (0.0268, 0.03096), (0.03096, 0.03512), (0.03512, 0.03928), (0.03928, 0.04344), (0.04344, 0.0476), (0.0476, 0.05176), (0.05176, 0.05592), (0.05592, 0.06008), (0.06008, 0.06424), (0.06424, 0.0684), (0.0684, 0.07256), (0.07256, 0.07672), (0.07672, 0.08088), (0.08088, 0.08504), (0.08504, 0.0892), (0.0892, 0.09336), (0.09336, 0.09752), (0.09752, 0.10168), (0.10168, 0.10584), (0.10584, 0.111)]
bucket_probs = [ 0.13324688, 0.01928208, 0.00673609, 0.18157023, 0.00838415, 0.02262627, 0.03113476, 0.00532367, 0.03577068, 0.02129174, 0.03319034, 0.04954116, 0.01754561, 0.02340251, 0.06973399, 0.07774243, 0.01412673, 0.05870618, 0.05894262, 0.04487461, 0.03307027, 0.00528693, 0.03512063, 0.01243449, 0.00091496]

def reset_buckets(F_RANGE):
	num_buckets = 25
	bucket_width = (F_RANGE[1] - F_RANGE[0]) / num_buckets
	buckets = get_buckets(F_RANGE[0], num_buckets, bucket_width)
	bucket_probs = bucket_distribution(buckets, bucket_width)
	print buckets
	print bucket_probs
	return buckets, bucket_probs

def get_buckets(min, n, w):
	buckets = []
	for i in range(n):
		lower = min + i * w
		upper = lower + w
		buckets.append((lower, upper))
	return buckets

def bucket_distribution(buckets, w):
	p = []
	for b in buckets:
		h = abs(kill_var(b[0]) + kill_var(b[1])) / 2.0
		p.append(w * h)
	return p / np.sum(p)

def kill_mean(x):
	#-1 * 10.931 * x**2 + 1.3658 * x + 0.027199
	#-1 * 8.2672 * x**2 + 1.0741 * x + 0.031086
	return -1 * 2.937 * x**2 + 0.6580 * x + 0.01616

def kill_var(x):
	var = -1 * 0.13462 * x + 0.016808
	return np.random.random_sample() * var - var / 2.0

def sample_feed():
	# split range into buckets, select bucket weighted by kill_var
	b_i = np.random.choice(len(buckets), p=bucket_probs)
	b = buckets[b_i]
	# choose feed uniformly within bucket
	return np.random.uniform(b[0], b[1])

def sample_kill(feed):
	return kill_mean(feed) + kill_var(feed)
