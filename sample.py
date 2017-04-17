# Utilities for sampling parameter values

import numpy as np

# pre-computed
# redo these if we change range, number of buckets, or kill_var
buckets = [(0.006, 0.010159999999999999), (0.010159999999999999, 0.01432), (0.01432, 0.01848), (0.018479999999999996, 0.022639999999999997), (0.02264, 0.0268), (0.026799999999999997, 0.030959999999999998), (0.030959999999999994, 0.03511999999999999), (0.03512, 0.039279999999999995), (0.039279999999999995, 0.04343999999999999), (0.04343999999999999, 0.04759999999999999), (0.047599999999999996, 0.051759999999999994), (0.051759999999999994, 0.05591999999999999), (0.05591999999999999, 0.06007999999999999), (0.060079999999999995, 0.06423999999999999), (0.06423999999999999, 0.06839999999999999), (0.0684, 0.07256), (0.07256, 0.07672), (0.07672, 0.08088), (0.08088, 0.08503999999999999), (0.08504, 0.0892), (0.0892, 0.09336), (0.09336, 0.09752), (0.09752, 0.10167999999999999), (0.10167999999999999, 0.10583999999999999), (0.10583999999999999, 0.10999999999999999)]
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
	return -1 * 8.2672 * x**2 + 1.0741 * x + 0.031086

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
