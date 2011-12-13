from trends.api import oauth
from trends.api import credentials
import urllib2
import contextlib

class Stream:
	URL = 'https://stream.twitter.com/1/statuses/sample.json'
	
	@classmethod
	def get(cls):
		"""
		Returns an open socket that listens to the Twitter streaming API.
		"""
		consumer = oauth.OAuthConsumer(
			credentials.CONSUMER_KEY,
			credentials.CONSUMER_SECRET,
		)
		token = oauth.OAuthToken(
			credentials.TOKEN_KEY,
			credentials.TOKEN_SECRET,
		)

		oauth_request = oauth.OAuthRequest.from_consumer_and_token(
			consumer,
			token,
			http_url=cls.URL,
		)

		signature_method_hmac_sha1 = oauth.OAuthSignatureMethod_HMAC_SHA1()
		oauth_request.sign_request(
			signature_method_hmac_sha1,
			consumer,
			token,
		)

		try:
			response = urllib2.urlopen(
				oauth_request.to_url(),
				timeout=10,
			)	
			return response
		except urllib2.URLError, err:
			print err
			raise 
					
			
			

		
		

		
	

	
