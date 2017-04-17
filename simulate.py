#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from scipy import ndimage
from matplotlib import image
import subprocess

# params
IMAGE_FILE = 'output.gif'
N_X = 256
GRID_SIZE = (N_X, N_X)
MAX_ITERS = 10000
R_U = 0.2097 #2e-5
R_V = 0.105 #1e-5
#H = 0.01 #1.0 / 143
D_T = 0.8 #0.9 * H**2 / (4 * R_U)

# range of legal values (should abs val & div 10 till we get to this range)
F_RANGE = (0.006, 0.11)
K_RANGE = (0.02, 0.07)

ONES = np.ones(GRID_SIZE)


def generate_image(feed, kill):
	U, V = init(feed, kill)

	for i in range(MAX_ITERS):
		du = du_dt(U, V, feed, kill)
		dv = dv_dt(U, V, feed, kill)

		if i % 100 == 0:
			image.imsave('images/U_{:05d}.png'.format(i), U, cmap='plasma')

		U += du * D_T
		V += dv * D_T

	subprocess.call(['convert',
		'-delay', '10',
		'-loop', '0',
		'images/U_*.png',
		IMAGE_FILE])

	return IMAGE_FILE


def laplace(A):
	return ndimage.filters.laplace(A, mode='wrap')

def du_dt(U, V, f, k):
	return R_U * laplace(U) - U * V**2 + f * (ONES - U)

def dv_dt(U, V, f, k):
	return R_V * laplace(V) + U * V**2 - (f + k) * V


# see mrob's paper on u-skate
def init(f, k):

	# background
	if not isinstance(f, np.ndarray) and k < (np.sqrt(f) - 2*f) / 2.0:
		A = np.sqrt(f) / (f + k)
		sqrt = np.sqrt(A**2 - 4.0)
		u_back = (A - sqrt) / (2 * A)
		v_back = np.sqrt(f) * (A + sqrt) / 2.0
	else:
		u_back = 0.0
		v_back = 1.0

	U = np.full(GRID_SIZE, u_back)
	V = np.full(GRID_SIZE, v_back)

	# rectangles
	for i in range(np.random.randint(40)):
		# dimensions
		w = np.random.randint(3, N_X / 8)
		h = np.random.randint(3, N_X / 8)
		# coords of top left corner
		x = np.random.randint(0, N_X - w)
		y = np.random.randint(0, N_X - h)
		# fill values
		u_rect = np.random.random_sample()
		v_rect = np.random.random_sample()

		U[x:x+w, y:y+h] = u_rect
		V[x:x+w, y:y+h] = v_rect

	return U, V

