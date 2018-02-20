from __future__ import division #it's in 2.7, and python2 always has int div
#so set the division to python 3.6 division
import re
import numpy as np
import string
import csv
import math
import twitterdemo
import emoji #clean out emojis with regex bc tkinter dies on emojis

###THIS FILE HAS THE NAIVE BAYES ALGORITHM THAT WILL GIVE OUT SENTIMENT AND COLORS
###TO THE FRONTEND FOR DRAWING 

with open("SentimentAnalysisDataset.csv", 'r') as f:
	csv = [row for row in csv.reader(f.read().splitlines())]
#first row is just definitions
csv = csv[1:]

#sentiment training for nb
train = []
for row in csv:
	train.append(row[0].split("\t")[1:4])
	#[0 = neg 1= pos, 'sentiment140', text]

#return dict of words based on sentiment for the wordcount dictionary
def getWords(sent, data):
	#not relevant to mood, but common
	stopWords = []
	wordCounts = dict()
	for row in data:
		#if it matches the sentiment
		if(len(row) > 0 and row[0] == str(sent)):
			#cleanup the non-ascii
			for i in range(len(row[2])):
				if not row[2][i].isalpha():
					row[2].replace(row[2][i], " ")
				#replace doesn't work with those common punctuation
				if i < len(row[2]) - 1 and row[2][i] in '!?,.@:;':
					row[2] = row[2][:i] + " " + row[2][i+1:]
			#get a list of words
			words = row[2].split()
			#put the words and counts into a dictionary
			for word in words:
				word = word.lower()
				if word not in wordCounts.keys() and word not in stopWords:
					wordCounts[word] = 1
				else:
					if(word not in stopWords):
						wordCounts[word] += 1
	return wordCounts

###WORD COUNTS
#dict of {word : freq}
positiveWords = getWords(1,train[:4000])
negativeWords = getWords(0,train[:4000])


###GLOBAL PROBABILITIES
#probability of a word being negative
negCount = sum(negativeWords.values())
posCount = sum(positiveWords.values())
totalWords = len(positiveWords.keys()) + len(negativeWords.keys())
negFreq = negCount / (negCount + posCount)
posFreq = posCount / (posCount + negCount)

#cleanup a tweet
def cleanup(s):
	#list of common words not related to sentiment
	stopWords = ['the', 'a', 'of', 'from', 'to']
	for i in range(len(s)):
		if (not s[i].isalpha()) and s[i] is not "'":
			s.replace(s[i], " ")
	l = s.split()
	for i in range(len(l)):
		word = l[i]
		if "@" in word or ".com" in word or "://" in word or \
		"-" in word or "..." in word or 'RT' in word or "http" in word:
			l[i] = ''
		if word[-1] == ',' or word[-1] == '.':
			word = word[:-1]
	for word in l:
		if word in stopWords:
			l.remove(word)
	s = " ".join(l)
	return s


###best alg: 3000 char/ 17000 neg, 4000/ neg + total on bottom is good
#P(-|S) = (pi P(S|-))for all words in S * P(-) 
#tweet = string
def getNegativeProbability(tweet):
	tweet = cleanup(tweet)
	#print("Neg: " + tweet)
	if(len(tweet.strip()) < 1):
		return 1
	n = negativeWords
	words = tweet.split()
	powsum = 1
	#set for efficiency (searching set is O(1))
	negWords = set(n.keys())
	for word in words:
		word = word.lower()
		if(word in negWords):
			#print('neg: ' + word + "," + str(n[word]))
			###trying an equalizer assumption of negCount = constant for algorithmic accuracy test
			#before: 17000 or (negCount + totalWords + 1000) FOR DENOM IN POWSUM
			powsum = powsum * (1+n[word]) / (negCount + totalWords) #negCount 
		else:
			#print('nope: ' + word)
			powsum = powsum * 1 / (negCount + totalWords) #negCount
		#print "neg: " + str(n[word])
	return powsum * negFreq

#(+|S) = powsum of P(S|+) * P(+) (same as neg prob but with +)
def getPositiveProbability(tweet):
	tweet = cleanup(tweet)
	#print(tweet)
	#if it's just a link or a blank tweet then it's special case
	if(len(tweet.strip()) < 1):
		return 17
	#print("Pos: " + tweet)
	p = positiveWords
	words = tweet.split()
	powsum = 1
	#set for efficiency
	posWords = set(p.keys())
	for word in words:
		word = word.lower()
		if(word in posWords):
			#print("pos: " + word + "," + str(p[word]))
			#before: poscount + totalWords IN DENOM
			powsum = powsum * (1+p[word]) / (posCount + totalWords)
		else:
			#print word
			powsum = powsum * 1 / (posCount + totalWords)
		#print "pos: " + str(p[word])
	return powsum * posFreq

###NOTE: Figure out how the ratio of pos/neg or neg/pos can 
#influence the 'color' - numerical values -> color (G -> R)
#Sentiment should be on log scale (bc NB is powsum): log(1/1) = 0 -> log(10/1) = 1

#takes string, returns tuple(string of sentiment, RGB value of color)
def classify(tweet):
	'''remove emojis before it hits the frontend - credit to random dude outside doherty 
	who told me emojis were in unicode after overhearing me talk about emojis in python
	'''
	#use regex to find all the emoji ranges
	emoji_pattern = re.compile(u'('
        u'\ud83c[\udf00-\udfff]|'
        u'\ud83d[\udc00-\ude4f\ude80-\udeff]|'
        u'[\u2600-\u26FF\u2700-\u27BF])+', 
        re.UNICODE)
	#substitute emojis with blank strings to remove
	tweet = emoji_pattern.sub(r'', tweet)
	#remove non-USC-2 emojis - non-ascii LOL WORKS BETTER THAN REGEX
	tweet = ''.join(c for c in tweet if ord(c) < 128)
	if(len(tweet.strip()) < 1):
		return ''
	f = lambda x: 1 / (1 + np.exp(-x/100))
	pos = getPositiveProbability(tweet)
	neg = getNegativeProbability(tweet)
	'''print("Positive sentiment: " + str(pos))
	print("Negative sentiment: " + str(neg))'''
	#NOTE: this is a very specific case for a link
	if(pos/neg == 17):
		return "'" + tweet + "' is a link.\n\n"
	#this is if there's no hits for either side
	if(abs(1.3 - pos/neg) < .07):
		return "'" + tweet + "' doesn't have enough identifiable words.\n\n"
	if(pos > neg):
		return "'" + tweet + "' is positive" + "\nPos/neg ratio: " + str((pos/neg)) + \
		"\nSigmoid: " + str(f(pos/neg)) + "\n\n"
	else:
		return "'" + tweet + "' is negative" + "\nNeg/pos ratio: " + str((neg/pos)) + \
		"\nSigmoid: " + str(f(neg/pos)) + "\n\n"


#get tweets from twitter from search
def analyze(tweet, count=5):
	#get some tweets from twitter
	api = twitterdemo.TwitterClient()
	tweets = api.get_tweets(tweet,count)
	results = ''
	for t in tweets:
		results = results + classify(t) + "\n"
	return results

#get tweets from twitter from user
def analyzeUser(user, count=5):
	#get some tweets from twitter
	api = twitterdemo.TwitterClient()
	tweets = api.get_user_tweets(user,count)
	results = ''
	if(type(tweets) != type('')):
		for t in tweets:
			results = results + classify(t) + "\n"
	else:
		results = ''
	return results

#classify, but return the 1/0, text, sigmoid as tuple
#2 means that either there wasn't enough words to id or it's a link
def classifyColor(tweet):
	#remove non-ascii from tweet
	tweet = ''.join(c for c in tweet if ord(c) < 128)
	f = lambda x: 1 / (1 + np.exp(-x/100))
	pos = getPositiveProbability(tweet)
	neg = getNegativeProbability(tweet)
	#print("Positive sentiment: " + str(pos))
	#print("Negative sentiment: " + str(neg))
	#NOTE: this is a very specific case for a link
	if(pos/neg == 17):
		#print(tweet)
		return 2, tweet, 0.5
	#this is if there's no hits for either side
	if(abs(1.3 - pos/neg) < .07):
		return 2, tweet, 0.5
	#NOTE: if bigger/lower < 1.x, would that be neutral???
	if(pos > neg):
		return 1, tweet, f(pos/neg)
	else:
		return 0, tweet, f(neg/pos)

#classify but with multiple tweets put together for an array of (pos=1/neg=0,text,sigmoid)
def analyzeColor(tweet, count = 5):
	#get some tweets from twitter
	api = twitterdemo.TwitterClient()
	tweets = api.get_tweets(tweet,count)
	results = []
	for t in tweets:
		results = results + [classifyColor(t)]
	return results

#classify but with multiple tweets from user put together for an array of (pos=1/neg=0,text,sigmoid)
def analyzeUserColor(user, count = 5):
	#get some tweets from twitter
	api = twitterdemo.TwitterClient()
	tweets = api.get_user_tweets(user,count)
	results = []
	if(type(tweets) != type('')):
		for t in tweets:
			results = results + [classifyColor(t)]
	else:
		return None
	return results

#NOTE: python2 printing is awesome
#print classify(u"chance\U0001f602")
#print analyzeUser('KingJames',1)
print "pos:" + str(posCount)
print "neg:" + str(negCount)





