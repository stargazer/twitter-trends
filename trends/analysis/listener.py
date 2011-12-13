from trends.api.stream import Stream, Tweet
import threading
import urllib2
import os, signal

class Tweet:

	stopsigns = (
		".", ",",":","?", ";", "!", "-", "_", "(", ")", "&", "*", "'", "`"
	)
	MIN_TOKEN_LENGTH = 3
	
	def __init__(self, **kwargs):
		self.text = kwargs.get('text', None)

	def process(self):
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

		for token in final_tokens:
			"""
			Put them in global dictionary
			update frequencies
			"""
			Collection.add(token)			


class Collection:
	"""
	Wrapper around the ``_tokens`` dictionary, which will contain all the
	tokens and their frequencies.
	"""

	# Class attribute, so accessible by all 
	_tokens = {}

	@classmethod
	def add(cls, token):
		"""
		Increases the frequency of token ``token``
		"""
		freq = cls._tokens.setdefault(token, 0)
		cls._tokens[token] = freq + 1

	@classmethod
	def load(cls, redis_instance):
		"""
		Prepopulate the collection with already gathered data from previous
		runs.
		"""
		pass


class Listener(threading.Thread):

	def __init__(self, terminate_please):
		super(Listener, self).__init__()
		self.terminate_please = terminate_please

	def request_termination(self):
		"""
		In any case that the thread can't keep on doing its work, and needs to
		terminate, we SHOULD end up here. This method will make sure that the
		main thread gets a termination signal, and from that point on, will
		handle termination of the remaining threads.
		"""
		print "Thread Listener: Signaling Termination"
		# Generating SIGINT
		os.kill(os.getpid(), signal.SIGINT)
		self.stream.close()
		

	def run(self):
		print "Thread Listener"

		self.stream = Stream()

		try:
			self.stream.connect()
		except urllib2.URLError:
			print "Thread Listener: Error connecting to Twitter API"
			self.request_termination()

		# Got the stream successfully. Let's get down to business
		else:
			try:
				# Going to do some actual work
				self.work()
			except (EOFError, IOError):
				self.request_termination()

		print "Thread Listener: Terminating"

	def work(self):
		 # As long as termination hasn't been asked
		while not self.terminate_please.isSet():
			try:
				tweet = self.stream.get_tweet()

				tokens = tweet.get_tokens()
				for token in tokens:
					Collection.add(token)

			except (EOFError, IOError): 
				raise
