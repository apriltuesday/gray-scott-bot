#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

### for random posting ###

# Strategy:
# sets of f & k buckets
# choose bucket based on its area
# choose uniformly from f bucket
# choose uniformly from k bucket

buckets = { # f-range -> k-range
	(0.006, 0.010) : (0.031, 0.032),
	(0.010, 0.012) : (0.031, 0.039),
	(0.014, 0.016) : (0.037, 0.045),
	(0.018, 0.020) : (0.043, 0.049),
	(0.022, 0.024) : (0.047, 0.051),
	(0.026, 0.028) : (0.049, 0.053),
	(0.030, 0.032) : (0.053, 0.055),
	(0.034, 0.036) : (0.055, 0.057),
	(0.038, 0.040) : (0.057, 0.059),
	(0.042, 0.078) : (0.061, 0.061),
	(0.082, 0.086) : (0.059, 0.061),
	(0.090, 0.092) : (0.059, 0.059),
	(0.094, 0.098) : (0.057, 0.059),
	(0.102, 0.106) : (0.055, 0.057),
	(0.109, 0.112) : (0.053, 0.055),
	(0.114, 0.118) : (0.053, 0.053)
}.items()

probs = [
	(b[0][1] - b[0][0]) * (b[1][1] - b[1][0]) for b in buckets
]
probs /= np.sum(probs)

def sample():
	b_i = np.random.choice(len(buckets), p=probs)
	b = buckets[b_i]
	f = np.random.uniform(b[0][0], b[0][1])
	k = np.random.uniform(b[1][0], b[1][1])
	return f, k


### for images ###
f_range = (0.006, 0.11)

def sample_max_feed():
	return np.random.uniform(f_range[0], f_range[1])

def sample_kill(feed):
	return -1 * 2.937 * feed**2 + 0.6580 * feed + 0.01616

