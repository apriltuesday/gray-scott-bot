#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy
import requests
from PIL import Image
import matplotlib
import numpy as np

from credentials import *
from sample import sample_feed, sample_kill
from simulate import generate_image

# twitter auth
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

PIC_FILE = 'tmp.jpg'
N_X = 256 # TODO repeated params between files
MAX_F = 0.1 #0.006
STATIC_K = 0.06 #0.02

class GrayScottBot(tweepy.StreamListener):

	def on_direct_message(self, status):
		author = status.author.screen_name
		self.direct_message(author)


	def get_feed_matrix_from_profile_pic(self, username):
		img_url = api.get_user(username).profile_image_url_https
		img_url = ''.join(img_url.split('_normal'))
		response = requests.get(img_url, stream=True)
		if response.status_code != 200:
			print 'didn\'t get image :('
			return 0.040
		with open(PIC_FILE, 'w') as f:
			f.write(response.raw.read())
		img = Image.open(PIC_FILE).convert(mode='L').resize((N_X, N_X))
		img.save(PIC_FILE)
		return matplotlib.image.pil_to_array(img) / 255.0 * MAX_F


	def random_post(self):
		feed = sample_feed()
		kill = sample_kill(feed)
		message = 'f={:f}, k={:f}'.format(feed, kill)
		print message
		output_file = generate_image(feed, kill)
		#api.update_with_media(output_file, message)


	def direct_message(self, username):
		kill = STATIC_K
		feed = self.get_feed_matrix_from_profile_pic(username)
		message = '@{}'.format(username)
		print message
		output_file = generate_image(feed, kill)
		#api.update_with_media(output_file, message)


def main():
	bot = GrayScottBot()
	bot.direct_message('bachesch')
	#bot.random_post()

	#stream = Stream(auth, bot)
	#stream.userstream()


if __name__ == '__main__':
	main()
