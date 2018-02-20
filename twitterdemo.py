import tweepy
from tweepy import OAuthHandler

#this is the twitter basic functionality that gets tweets from the api

q = "Facebook"

class TwitterClient(object):
	def __init__(self):
		#keys from 'test15112' twitter app
		consumer_key = 'sQzgs9DX1AmX8gCZeAkZjfWps'
		consumer_secret = 'fPTlLkW77SgeVkAwsr9BU9Ym6lG9CucXHOGwyojOgDvkCiL0Qt'
		access_token = '932057687344517122-u8xUwIPOmfVjVZdtEslPr553dUgo6fq'
		access_token_secret = 'F9fVMezHVuyEcYYhwAPA2OnCuBlYlFaB7pnZkCM32uupK'
		try:
			#authorize the api
			self.auth = OAuthHandler(consumer_key, consumer_secret)
			self.auth.set_access_token(access_token, access_token_secret)
			self.api = tweepy.API(self.auth)
		except:
			#if it didn't work
			print("fk it didn't authorize")

	#actually get the texts from tweets
	def get_tweets(self, query, count=10):
		tweets = []
		try:
			#search twitter for count amount of tweets under q
			fetched_tweets = self.api.search(q = query, count = count, result_type = 'popular')
			#attach the text of each tweet onto an array
			for tweet in fetched_tweets:
				if tweet.retweet_count > 0:
					#if it's not a duplicate append
					if tweet not in tweets:
						tweets.append("@" + tweet.author.screen_name + ": " + tweet.text)
			return tweets
		#if it didn't work
		except tweepy.TweepError as e:
			print("Error is: " +  e)

	def get_user_tweets(self, username, count=10):
		tweets = []
		try:
			#search twitter for count amount of tweets under q
			fetched_tweets = self.api.user_timeline(screen_name = username, count = count)
			#if it doesn't have tweets
			if(len(fetched_tweets) < 1):
				return "Username not found!"
			#attach the text of each tweet onto an array
			for tweet in fetched_tweets:
				if tweet.retweet_count > 0:
					#if it's not a duplicate append
					if tweet not in tweets:
						tweets.append("@" + tweet.author.screen_name + ": " + tweet.text)
			return tweets
		#if it didn't work
		except tweepy.TweepError as e:
			return "Username not found!"

def main():
	api = TwitterClient()
	tweets = api.get_user_tweets('realDonaldTrump')
	if(type(tweets) != type('')):
		for t in tweets:
			print(t)

if __name__ == '__main__':
	main()