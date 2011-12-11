from trends.analysis.listener import Collection
import threading

class Statistician(threading.Thread):
	def __init__(self):
		super(Statistician, self).__init__()

	def run(self):	
		print "Thread Statistician"
	
