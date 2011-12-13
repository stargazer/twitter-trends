from trends.api import oauth
from trends.api import credentials
import urllib2
import contextlib
import json     
import socket
from ssl import SSLError

class Stream:
	URL = 'https://stream.twitter.com/1/statuses/sample.json'
	
	def __init__(self):
		"""
		Creates the Stream object, and sets its ``self.oauth_request``
		attribute to the signed request that will be used to connect to
		Twitter's streaming API.
		"""
		consumer = oauth.OAuthConsumer(
			credentials.CONSUMER_KEY,
			credentials.CONSUMER_SECRET,
		)
		token = oauth.OAuthToken(
			credentials.TOKEN_KEY,
			credentials.TOKEN_SECRET,
		)

		self.oauth_request = oauth.OAuthRequest.from_consumer_and_token(
			consumer,
			token,
			http_url=self.URL,
		)

		signature_method_hmac_sha1 = oauth.OAuthSignatureMethod_HMAC_SHA1()
		
		self.oauth_request.sign_request(
			signature_method_hmac_sha1,
			consumer,
			token,
		)

	def connect(self):
		"""
		Connect to the API. Sets the Stream instance'a ``self.handler``
		attribute equal to the file-like object that talks to the API.

		If it fails, the Stream object will not have a ``self.handler``
		attribute.
		"""
		try:
			self.handler = urllib2.urlopen(
				self.oauth_request.to_url(),
				timeout=10,
			)	
		except urllib2.URLError, err:
			raise 
					
	def get_tweet(self):
		"""
		Reads the next line from the stream, transforms it to a Tweet object.

		exceptions: EOFError, IOError
		@return: Tweet object
		"""
		try:
			# It raises SSLError, which cannot be captured (Python bug), so I
			# transform it to an IOError.
			line = 	self.handler.readline()
		except:
			raise IOError

		if not line:
			raise EOFError
	
		dic = json.loads(line.decode('utf-8'))
		tweet = Tweet(**dic)   
		return tweet

			
	def close(self):
		"""
		Close the stream handler
		"""
		if getattr(self, 'handler', None):
			self.handler.close()

class Tweet:
	stopsigns = (
		".", ",",":","?", ";", "!", "-", "_", "(", ")", "&", "*", "'", "`"
	)
	MIN_TOKEN_LENGTH = 3
	
	def __init__(self, **kwargs):
		self.text = kwargs.get('text', None)

	def get_tokens(self):
		"""
		Split into tokens, 
		get rid of shit, 
		place tokens in global dictionary
		with frequencies

		"""
		final_tokens = []
		if self.text:
			initial_tokens = self.text.split()

			for token in initial_tokens:
				if len(token) <= self.MIN_TOKEN_LENGTH:
					continue

				elif token.startswith('http://'):
					continue
			
				elif token[0] in self.stopsigns:
					token = token[1:]
				elif token[-1] in self.stopsigns:
					token = token[0:-1]

				try:				
					final_tokens.append(token.lower())
				except:
					final_tokens.append(token)
		return final_tokens

		
		

		
	

	
