from trends.api import oauth
import urllib2
import contextlib

class Stream:
	URL = 'https://stream.twitter.com/1/statuses/sample.json'
	
	CONSUMER_KEY = 'eU0DQBRlTtm4Ht3dJ9DDtA'
	CONSUMER_SECRET = 'uER0UOsCbT7BwLm0la6mokP7fjfrrCVTnVU6uGPjKk'
	TOKEN_KEY = '88961589-ZGUU9ntHNxZ3FZ0JVf6R1dqA8GXeA1hePA90EakFE'
	TOKEN_SECRET = 'QdEei39k2CtzYomiu3y97RYCQ5FRYnGgvmS9TxFHm8'

	@classmethod
	def get(cls):
		"""
		Returns an open socket that listens to the Twitter streaming API.
		"""
		consumer = oauth.OAuthConsumer(
			cls.CONSUMER_KEY,
			cls.CONSUMER_SECRET,
		)
		token = oauth.OAuthToken(
			cls.TOKEN_KEY,
			cls.TOKEN_SECRET,
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
					
			
			

		
		

		
	

	
