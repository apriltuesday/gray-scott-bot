#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
from scipy import ndimage
from matplotlib import image
import os
import subprocess

# params
IMAGE_FILE = 'output.gif'
IMAGE_DIR = 'images'
MAX_ITERS = 10000
R_U = 0.2097
R_V = 0.105
D_T = 0.8


def generate_image(feed, kill, frame_offset=0):
	if not os.path.exists(IMAGE_DIR):
		os.makedirs(IMAGE_DIR)

	if isinstance(feed, np.ndarray):
		grid_size = feed.shape
	else:
		grid_size = (256, 256)
	U, V = init(feed, kill, grid_size)

	for i in range(MAX_ITERS+frame_offset):
		du = du_dt(U, V, feed, kill, grid_size)
		dv = dv_dt(U, V, feed, kill, grid_size)

		if i > 900+frame_offset and i % 200 == 0:
			image.imsave('{}/U_{:05d}.png'.format(IMAGE_DIR, i), U, cmap='plasma')

		U += du * D_T
		V += dv * D_T

	return save_image()


def laplace(A):
	return ndimage.filters.laplace(A, mode='wrap')

def du_dt(U, V, f, k, grid_size):
	return R_U * laplace(U) - U * V**2 + f * (np.ones(grid_size) - U)

def dv_dt(U, V, f, k, grid_size):
	return R_V * laplace(V) + U * V**2 - (f + k) * V


# see mrob's paper on u-skate
def init(f, k, grid_size):
	# background
	if not isinstance(f, np.ndarray) and k < (np.sqrt(f) - 2*f) / 2.0:
		A = np.sqrt(f) / (f + k)
		sqrt = np.sqrt(A**2 - 4.0)
		u_back = (A - sqrt) / (2 * A)
		v_back = np.sqrt(f) * (A + sqrt) / 2.0
	else:
		u_back = 1.0
		v_back = 0.0

	U = np.full(grid_size, u_back)
	V = np.full(grid_size, v_back)

	# rectangles
	nx, ny = grid_size
	for i in range(np.random.randint(5, high=40)):
		# dimensions
		w = np.random.randint(10, nx / 8)
		h = np.random.randint(10, ny / 8)
		# coords of top left corner
		x = np.random.randint(0, nx - w)
		y = np.random.randint(0, ny - h)
		# fill values
		u_rect = np.random.random_sample()
		v_rect = np.random.random_sample()

		U[x:x+w, y:y+h] = u_rect
		V[x:x+w, y:y+h] = v_rect

	return U, V


def save_image():
	fuzz = 0
	while fuzz < 20: #fuzzing over 20% looks terrible
		subprocess.call(['convert',
			'-delay', '10',
			'-loop', '0',
			'-layers', 'optimize',
			'-fuzz', '{}%'.format(fuzz),
			'-resize', '256',
			'{}/U_*.png'.format(IMAGE_DIR),
			IMAGE_FILE])
		if os.path.getsize(IMAGE_FILE) < 3000000L:
			break
		fuzz += 2
	subprocess.call(['rm', '-r', IMAGE_DIR])
	return IMAGE_FILE
