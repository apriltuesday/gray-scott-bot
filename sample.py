#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np

# Strategy:
# set of buckets of f & k values
# choose bucket based on its area
# choose uniformly from f bucket
# choose uniformly from k bucket

buckets = { # f-range -> k-range
	(0.006, 0.010) : (0.031, 0.032),
	(0.010, 0.014) : (0.037, 0.039),
	(0.014, 0.018) : (0.044, 0.055),
	(0.018, 0.022) : (0.046, 0.057),
	(0.022, 0.026) : (0.050, 0.060),
	(0.026, 0.030) : (0.053, 0.063),
	(0.030, 0.034) : (0.055, 0.065),
	(0.034, 0.038) : (0.058, 0.065),
	(0.038, 0.042) : (0.059, 0.066),
	(0.042, 0.078) : (0.061, 0.066),
	(0.078, 0.082) : (0.059, 0.066),
	(0.082, 0.086) : (0.059, 0.063),
	(0.086, 0.090) : (0.059, 0.063),
	(0.090, 0.094) : (0.059, 0.061),
	(0.094, 0.098) : (0.056, 0.061),
	(0.098, 0.102) : (0.056, 0.060),
	(0.102, 0.106) : (0.056, 0.058),
	(0.106, 0.110) : (0.053, 0.057),
	(0.110, 0.114) : (0.052, 0.055)
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

