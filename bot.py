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
IMAGE_FILE = 'output.gif'
DAILY_POST_TIME = 8
DELAY_IN_SEC = 60

# simulation params
IMAGE_SIZE = (256, 256)
MAX_ITERS = 20000
R_U = 0.2097
R_V = 0.105
T_STEP = 0.8

# range of legal values (should abs val & div 10 till we get to this range)
F_RANGE = (0.006, 0.11)
K_RANGE = (0.02, 0.07)

ONES = np.ones(IMAGE_SIZE)

# TODO filesize limits from tweepy...


def generate_image(feed, kill):
	U, V = init()

	for i in range(MAX_ITERS):
		du = du_dt(U, V, feed, kill, R_U)
		dv = dv_dt(U, V, feed, kill, R_V)
		U += du * T_STEP
		V += dv * T_STEP
		if i%100 == 0:
			image.imsave('images/U_{:05d}.png'.format(i), U, cmap='plasma')

	subprocess.call(['convert',
		'-delay', '10',
		'-loop', '0',
		#'-resize', '75%',
		'images/U_*.png',
		IMAGE_FILE])


def init():
	# TODO see mrob for initialization
	w = IMAGE_SIZE[0] / 4
	x = 3*w/2

	U = np.ones(IMAGE_SIZE) + image_noise()
	V = np.zeros(IMAGE_SIZE) + image_noise()
	U[x:x+w, x:x+w] -= 0.5
	V[x:x+w, x:x+w] += 0.25

	return U, V

def image_noise():
	return np.random.random_sample(IMAGE_SIZE) * 0.002 - 0.001


def du_dt(U, V, f, k, ru):
	return ru * ndimage.filters.laplace(U) - U * V**2 + f * (ONES - U)

def dv_dt(U, V, f, k, rv):
	return rv * ndimage.filters.laplace(V) + U * V**2 - (f + k) * V


def daily_post():
	feed = 0.090 #np.random.uniform(F_RANGE[0], F_RANGE[1])
	kill = mean(feed) + noise(feed)
	message = 'f={:f}, k={:f}'.format(feed, kill)
	print message
	generate_image(feed, kill)
	#api.update_with_media(IMAGE_FILE, message)


def mean(x):
	#-1 * 10.931 * x**2 + 1.3658 * x + 0.027199
	return -1 * 8.2672 * x**2 + 1.0741 * x + 0.031086

def noise(x):
	var = -1 * 0.13462 * x + 0.016808
	return np.random.random_sample() * var - var / 2.0


if __name__ == '__main__':
	# TODO look for dms and set params
	#now = datetime.now()
	#if now.hour == DAILY_POST_TIME and now.minute < 1:
	daily_post()
	#time.sleep(DELAY_IN_SEC)