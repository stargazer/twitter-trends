from trends.analysis.listener import Listener
from trends.analysis.statistician import Statistician

import threading

def main():

	workers = (
		Listener(),   	# Listen to the Streaming API
		Statistician(), # Compute statistics about data
	)
	
	for worker in workers:
		worker.start()

	for worker in workers:
		worker.join()



	# Thread 1
	#	stream.listen()
	#	Instantiate Listener class.
	#	Run

	# Thread 2
	#	Instanstiate Statistician class
	#	run

	pass
