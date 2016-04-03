 # -*- coding: utf-8 -*-
import tweepy
import pickle
from env import CONSUMER_TOKEN, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET





if __name__ == "main":
	# authenticate ********************************************************** #
	auth = tweepy.OAuthHandler(CONSUMER_TOKEN, CONSUMER_SECRET)
	auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
	api = tweepy.API(auth)

	# initialize, or load state if there is one ***************************** #


	# generate next state *************************************************** #


	# tweet it ************************************************************** #
	api.update_status()
