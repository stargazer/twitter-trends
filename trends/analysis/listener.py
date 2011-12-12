from trends.api.stream import Stream
import json

import threading
import urllib2

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
   		freq = cls._tokens.get(token, None)
		if freq:
			cls._tokens[token] = freq + 1
		else:
			cls._tokens[token] = 1
	
	
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

	def run(self):
		print "Thread Listener"

		try:
			stream = Stream.get()
		except urllib2.URLError:
			print "Thread Listener: Error connecting to Twitter API"

		# Going to do some actual work
		self.work(stream)	   

		print "Thread Listener: Terminating"

	def work(self, stream):
		 # As long as termination hasn't been asked
		while not self.terminate_please.isSet():
			line = stream.readline()
			dic = json.loads(line.decode('utf-8'))
			tweet = Tweet(**dic)
			tweet.process()      
