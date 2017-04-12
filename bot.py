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
 
# twitter auth
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

# params
DELAY_IN_SEC = 3600
IMAGE_FILE = 'output.gif'
IMAGE_SIZE = (256, 256)
MAX_ITERS = 5000
R_U = 0.2097
R_V = 0.105
T_STEP = 0.8

# range of legal values (should abs val & div 10 till we get to this range)
F_RANGE = (0.006, 0.11)
K_RANGE = (0.02, 0.07)

ONES = np.ones(IMAGE_SIZE)


def generate_image(feed, kill):
	U, V = init(feed, kill)
	#image.imsave('U_INIT.png', U, cmap='plasma')
	#image.imsave('V_INIT.png', V, cmap='plasma')

	for i in range(MAX_ITERS):
		du = du_dt(U, V, feed, kill, R_U)
		dv = dv_dt(U, V, feed, kill, R_V)
		U += du * T_STEP
		V += dv * T_STEP
		if i > 500 and i%100 == 0:
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


def du_dt(U, V, f, k, ru):
	return ru * ndimage.filters.laplace(U) - U * V**2 + f * (ONES - U)

def dv_dt(U, V, f, k, rv):
	return rv * ndimage.filters.laplace(V) + U * V**2 - (f + k) * V


def random_post():
	feed = np.random.uniform(F_RANGE[0], F_RANGE[1])
	kill = mean(feed) + noise(feed)
	message = 'f={:f}, k={:f}'.format(feed, kill)
	print message
	generate_image(feed, kill)
	api.update_with_media(IMAGE_FILE, message)


def mean(x):
	#-1 * 10.931 * x**2 + 1.3658 * x + 0.027199
	return -1 * 8.2672 * x**2 + 1.0741 * x + 0.031086

def noise(x):
	var = -1 * 0.13462 * x + 0.016808
	return np.random.random_sample() * var - var / 2.0


if __name__ == '__main__':
	while True:
		random_post()
		time.sleep(DELAY_IN_SEC)

