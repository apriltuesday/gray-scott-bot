#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import requests
import time

import matplotlib
import numpy as np
from PIL import Image
from scipy import misc
import tweepy

from simulate import generate_image
from sample import sample

# twitter auth
consumer_key = os.environ['CONSUMER_KEY']
consumer_secret = os.environ['CONSUMER_SECRET']
access_token = os.environ['ACCESS_TOKEN']
access_token_secret = os.environ['ACCESS_TOKEN_SECRET']
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

MAX_IMG_SIZE = 512
PIC_FILE = 'tmp.jpg'
BOT_NAME = 'GrayScottBot'


class GrayScottBot(tweepy.StreamListener):

	def on_status(self, status):
		tweet_id = status.id
		username = status.author.screen_name

		if username == BOT_NAME:
			return
		# stop if someone just retweeted you, gets obnoxious
		if (hasattr(status, 'retweeted_status')
			and status.retweeted_status != None
			and status.retweeted_status.author.screen_name == BOT_NAME):
			return

		print 'status {} received'.format(tweet_id)
		try:
			media = status.entities['media'][0]
			if media['type'] == 'photo':
				img_url = media['media_url']
		except: #get profile pic if no image in message
			img_url = api.get_user(username).profile_image_url_https
			img_url = ''.join(img_url.split('_normal'))
		self.direct_message(username, img_url, tweet_id)


	def get_feed_matrix_from_image(self, img_url):
		response = requests.get(img_url, stream=True)
		if response.status_code != 200:
			print 'didn\'t get image :('
			return 0.5
		with open(PIC_FILE, 'w') as f:
			f.write(response.raw.read())
		img = Image.open(PIC_FILE).convert(mode='L')
		if img.size[0] > MAX_IMG_SIZE:
			ratio = float(MAX_IMG_SIZE) / img.size[0]
			img = img.resize((MAX_IMG_SIZE, int(img.size[1] * ratio)))
		return matplotlib.image.pil_to_array(img) / 255.0


	def random_post(self):
		try:
			feed, kill = sample()
			message = 'f={:f}, k={:f}'.format(feed, kill)
			print message
			output_file = generate_image(feed, kill)
			api.update_with_media(output_file, message)
			print 'done!'
		except Exception as e:
			print 'couldn\'t create status :', e


	def direct_message(self, username, img_url, tweet_id):
		try:
			kill = 0.062
			feed = (1.0 - self.get_feed_matrix_from_image(img_url)) * 0.045 + 0.015
			message = '@{}'.format(username)
			print message
			output_file = generate_image(feed, kill, frame_offset=4000)
			api.update_with_media(output_file, message, in_reply_to_status_id=tweet_id)
			print 'done!'
		except Exception as e:
			print 'couldn\'t create status :', e


def main():
	bot = GrayScottBot()
	print 'up and running!'

	# reply to DMs
	stream = tweepy.Stream(auth, bot)
	stream.filter(track=[BOT_NAME], async=True)

	# post randomly every 4 hours
	while True:
		bot.random_post()
		time.sleep(14400)


if __name__ == '__main__':
	main()
