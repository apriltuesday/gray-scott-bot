#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
import tweepy
import time
from datetime import datetime
import numpy as np
from scipy import ndimage
from matplotlib import image
import subprocess

from credentials import *
from sample import *
 
# twitter auth
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# params
DELAY_IN_SEC = 3600
IMAGE_FILE = 'output.gif'
IMAGE_SIZE = (256, 256)
MAX_ITERS = 10000
R_U = 2e-5 #0.2097
R_V = 1e-5 #0.105
T_STEP = 0.5 #0.8
X_STEP = 1.0 / 143

# range of legal values (should abs val & div 10 till we get to this range)
F_RANGE = (0.006, 0.11)
K_RANGE = (0.02, 0.07)

ONES = np.ones(IMAGE_SIZE)
ZEROS = np.zeros(IMAGE_SIZE)
KERNEL = np.array([0, 1, 0, 1, -4, 1, 0, 1, 0]).reshape((3,3)) / X_STEP**2


def generate_image(feed, kill):
	U, V = init(feed, kill)

	for i in range(MAX_ITERS):
		du = du_dt(U, V, feed, kill, R_U)
		dv = dv_dt(U, V, feed, kill, R_V)
		U += du * T_STEP
		V += dv * T_STEP
		if i % 100 == 0:
			image.imsave('images/U_{:05d}.png'.format(i), U, cmap='plasma')

	subprocess.call(['convert',
		'-delay', '10',
		'-loop', '0',
		'images/U_*.png',
		IMAGE_FILE])


# see mrob's paper on u-skate
def init(f, k):
	# background
	if k < (np.sqrt(f) - 2*f) / 2.0:
		A = np.sqrt(f) / (f + k)
		sqrt = np.sqrt(A**2 - 4.0)
		u_back = (A - sqrt) / (2 * A)
		v_back = np.sqrt(f) * (A + sqrt) / 2.0
	else:
		u_back = 0.0
		v_back = 1.0

	U = np.full(IMAGE_SIZE, u_back)
	V = np.full(IMAGE_SIZE, v_back)

	# rectangles
	for i in range(np.random.randint(40)):
		# dimensions
		w = np.random.randint(1, IMAGE_SIZE[0] / 8)
		h = np.random.randint(1, IMAGE_SIZE[0] / 8)
		# coords of top left corner
		x = np.random.randint(0, IMAGE_SIZE[0] - w)
		y = np.random.randint(0, IMAGE_SIZE[0] - h)
		# fill values
		u_rect = np.random.random_sample()
		v_rect = np.random.random_sample()

		U[x:x+w, y:y+h] = u_rect
		V[x:x+w, y:y+h] = v_rect

	return U, V


def laplace(A):
	#A = ndimage.filters.gaussian_filter(A, 1, mode='wrap')
	return ndimage.filters.convolve(A, KERNEL, mode='wrap')

def du_dt(U, V, f, k, ru):
	return ru * laplace(U) - U * V**2 + f * (ONES - U)

def dv_dt(U, V, f, k, rv):
	return rv * laplace(V) + U * V**2 - (f + k) * V


def random_post():
	feed = sample_feed() #   # 0.034 #
	kill = sample_kill(feed) #   #0.063 #
	message = 'f={:f}, k={:f}'.format(feed, kill)
	print message
	generate_image(feed, kill)
	#api.update_with_media(IMAGE_FILE, message)

def sample_feed():
	# split range into buckets, select bucket weighted by kill_var
	b_i = np.random.choice(len(buckets), p=bucket_probs)
	b = buckets[b_i]
	# choose feed uniformly within bucket
	return np.random.uniform(b[0], b[1])

def sample_kill(feed):
	return kill_mean(feed) + kill_var(feed)


if __name__ == '__main__':
	#while True:
	random_post()
	#time.sleep(DELAY_IN_SEC)

