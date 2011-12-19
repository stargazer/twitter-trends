from trends.api.stream import Stream, Tweet
from trends.analysis.statistician import Stats
import threading
import urllib2
import os, signal




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
				Stats.total_tweets += 1

				tokens = tweet.get_tokens()
				for token in tokens:
					Stats.add(token)

			except (EOFError, IOError): 
				raise
