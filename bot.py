#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tweepy
import requests
from PIL import Image
import matplotlib
import numpy as np
from scipy import misc

from credentials import *
from simulate import generate_image, sample_feed, sample_kill

# twitter auth
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

PIC_FILE = 'tmp.jpg'
BOT_NAME = 'GrayScottBot'


class GrayScottBot(tweepy.StreamListener):

	def on_status(self, status):
		username = status.author.screen_name
		if username == BOT_NAME:
			return
		# stop if someone just retweeted you, gets obnoxious
		if (hasattr(status, 'retweeted_status')
			and status.retweeted_status != None
			and status.retweeted_status.author.screen_name == BOT_NAME):
			return

		print 'status received'
		try:
			media = status.entities['media'][0]
			if media['type'] == 'photo':
				img_url = media['media_url']
		except: #get profile pic if no image in message
			img_url = api.get_user(username).profile_image_url_https
			img_url = ''.join(img_url.split('_normal'))
		self.direct_message(username, img_url)


	def get_feed_matrix_from_image(self, img_url):
		response = requests.get(img_url, stream=True)
		if response.status_code != 200:
			print 'didn\'t get image :('
			return 0.5
		with open(PIC_FILE, 'w') as f:
			f.write(response.raw.read())
		img = Image.open(PIC_FILE).convert(mode='L')
		if img.size[0] > 256:
			ratio = 256.0 / img.size[0]
			img = img.resize((256, int(img.size[1] * ratio)))
		return matplotlib.image.pil_to_array(img) / 255.0


	def random_post(self):
		# TODO if we want to do this, need to fix sampling or simulation
		feed = sample_feed()
		kill = sample_kill(feed)
		message = 'f={:f}, k={:f}'.format(feed, kill)
		print message
		output_file = generate_image(feed, kill)
		api.update_with_media(output_file, message)


	def direct_message(self, username, img_url):
		try:
			max_f = sample_feed()
			kill = sample_kill(max_f)
			feed = max_f * self.get_feed_matrix_from_image(img_url)
			message = 'f={}, k={} @{}'.format(max_f, kill, username)
			print message
			output_file = generate_image(feed, kill)
			api.update_with_media(output_file, message)
			print 'done!'
		except:
			print 'couldn\'t create status :('


def main():
	bot = GrayScottBot()

	stream = tweepy.Stream(auth, bot)
	print 'up and running!'
	stream.userstream(_with='user')


if __name__ == '__main__':
	main()
