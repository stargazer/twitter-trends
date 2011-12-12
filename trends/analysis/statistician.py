from trends.analysis.listener import Collection
import threading

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
		# As long as termination hasn't been asked
		while not self.terminate_please.isSet():
			pass

