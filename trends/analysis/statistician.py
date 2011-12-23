import threading
from math import sqrt

class Statistician(threading.Thread):
	def __init__(self, terminate_please):
		super(Statistician, self).__init__()
		self.terminate_please = terminate_please

	def run(self):	
		print "Thread Statistician"
	
		# Going to do some actual work
		self.work()

		print "Thread Statistician: Terminating"
	
	def work(self):

		def refresh():
			Stats.get_stats()
	
		# As long as termination hasn't been asked
		while not self.terminate_please.isSet():
			cv = threading.Condition()
			cv.acquire()
			cv.wait(180)

			refresh()
			
			cv.release()
 

class Stats:
	"""
	Contains the ``_scores`` dictionary that contains all the tokens and their
	stats, and all the methods around it.
	"""
	
	# Entries of the form:
	# {<token>:  <token_stats>}
	_scores = {}

	# Round of observations
	round = 1.0

	# Total tweets read
	total_tweets = 0

	@classmethod
	def add(cls, token):
		"""
		Increases the frequency of token ``token``
		"""
		token_stats = cls._scores.setdefault(token, TokenStats(cls.round))
		token_stats.increase()

	@classmethod
	def get_stats(cls):
		"""
		Compute the stats for each token, and show the highest-ranked ones.
		"""
		# TODO: More efficient way to get the stats
		# Especially the sort.
		# Keep a threshold, and don't compute scores of tokens that appear less
		# times than threshold
		# Measure the difference of this dictionary from the original
		# Measure how long it takes to sort the dictionary.
		# Measure how long it takes to create the temp_dict
		# 
		# I need to:
		#   Decrease the times of these distinct operations
		#   Decrease the size of the _scores dictionary (is decrease the amount
		#  of tokens that are saved in the dictionary)
		#   Play with the value.observation > <number>
		#   Maybe trim the _scores dic periodically, and remove tokens with a
		#   very low mean? (Does std have anything to do?)
		from operator import itemgetter

		# Here i take a snapshot of the dictionary _scores, in a list of pairs
		# of (token, <stats>).
		items = cls._scores.items()
		
		print "Total Tweets read: %s" % cls.total_tweets
		print "Number of distinct tokens: %s" % len(cls._scores)		
		print "Computing Scores"
		import time
		start = time.time()
		for token, stats in items:
			cls._scores[token].compute_scores(cls.round)					
		print "Time: %s" % (time.time() - start)
		print "\n"

		print "Sorting scores"
		start = time.time()
		_sorted = sorted(items, key=itemgetter(1), reverse=True)
		print "Time: %s" % (time.time() - start)
		print "\n"

		"""
		print "Cleaning up Token dictionary"
		import time
		start = time.time()
		temp_dict = {}
		for key, value in cls._scores.items():
			if value.observation > 5:
				temp_dict[key] = value
			else:
				cls._scores[key].observation = 0
				cls._scores[key].score = 0
		print "Time: %s" % (time.time() - start)

		print "Computing scores"
		start = time.time()
		for token_stats in temp_dict.values():
			token_stats.compute_scores(cls.round)
		print "Time: %s" % (time.time() - start)

		print "Sorting"
		start = time.time()
		_sorted = sorted(temp_dict.items(), key=itemgetter(1), reverse=True)
		print "Time: %s" % (time.time() - start)
		"""
		for token, stats in _sorted[:5]:
			try:
				print token
				print stats
			except:
				pass
			print "\n"

		
		# Zero the score and observation
		for token, stats in items:
			cls._scores[token].zero()

		cls.round += 1


	@classmethod
	def load(cls, redis_instance):
		"""
		Prepopulate the collection with already gathered data from previous
		runs.
		"""
		pass
 

class TokenStats:
	"""
	Stores stats. Every instance of TokenStats corresponds to a single token.
	"""
	
	# How history fades when computing the floating average
	_fade = 0.8

	# If observation < threshold, do not compute scores
	threshold = 10 

	# If a token has been observed < rounds_threshold times, we don't compute
	# its score. We need more data about its history to be able to compute the
	# score confidently.
	rounds_threshold = 5

	def __init__(self, round):
		# Num of appearances in the last round
		self.observation = 1
		self.rounds_observed = 0
		self.mean = 0.0
		self.sqr_mean = 0.0
		self.std = 0.0
		self.score = 0.0


	def increase(self):			
		self.observation += 1

	def compute_scores(self, round):
		"""
		Computes floating point z-scores for token

		http://stackoverflow.com/questions/787496/what-is-the-best-way-to-compute-trending-topics-or-tags/826509#826509 
		"""
		if self.observation > 0:
			self.rounds_observed += 1

		#TODO: Play with different _fade values
		self.mean = self.mean * self._fade + \
			self.observation * (1 - self._fade)

		self.sqr_mean = self.sqr_mean * self._fade + \
			(self.observation ** 2) * ( 1 - self._fade)

		self.std = sqrt(self.sqr_mean - self.mean **2 )

		# Do I need to compute the score for this token?
		if self.rounds_observed > self.rounds_threshold and \
			self.observation > self.threshold:
			compute = True
		else:
			compute = False

		if compute:
			# Compute the score
			if self.std == 0:
				self.score = (self.observation - self.mean) * float("infinity")
			else:
				self.score = (self.observation - self.mean) / self.std
		else:
			# Else set it to zero
			self.score = 0.0



	def zero(self):
		"""
		Zero the observation and score, since this rounds's scores have been
		computed.
		"""
		self.observation = 0
		self.score = 0.0

	def __cmp__(self, other):
		"""
		Comparison operator, for sorting TokenStats objects, based on scores.
		"""
		if self.score > other.score:
			return 1
		elif self.score == other.score:
			return 0
		elif self.score < other.score:
			return -1


	def __str__(self):
		return "Observation: %s,Rounds observed: %s, Mean: %s, Std: %s, Score: %s" % (
			self.observation, self.rounds_observed, self.mean, self.std, self.score,
		)
 
