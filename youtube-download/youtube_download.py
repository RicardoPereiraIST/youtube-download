#!python

import os
import sys
from datetime import datetime
from time import sleep
import threading
import math
from thread import MyThread
import argparse

def downloadFiles(file, format, output = None, n_threads = 1):
	with open(file, "r") as f:
		lines = f.read().splitlines()
	f.close()

	dir_path = output

	if(dir_path is None):
		dir_path = os.path.dirname(os.path.realpath(file))
		dir_path = os.path.join(dir_path, "youtube_dl-"+datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
		if not os.path.exists(dir_path):
			os.makedirs(dir_path)

	if(n_threads > len(lines)):
		n_threads = len(lines)

	threads = []
	
	urls_per_thread = [] 
	for i in range(0, n_threads):
		max_elements = int(math.ceil(float(len(lines))/(n_threads - i)))
		url_sublist = lines[:max_elements]
		lines = lines[max_elements:]
		urls_per_thread.append(url_sublist or None)

	for i in range(0, n_threads):
		if(urls_per_thread[i] is not None):
			threads.append(MyThread(urls_per_thread[i], dir_path, format))
		else:
			break

	for thread in threads:
	    thread.start()

	for thread in threads:
	    thread.join()

if __name__ == '__main__':
	startTime = datetime.now()

	parser = argparse.ArgumentParser(description='Youtube downloader')
	parser.add_argument('file', help="Name of the file you want to read from.")
	parser.add_argument('format', help="Format you want to download.")
	parser.add_argument('-o', "--output", dest="output", help="Name of the folder you want to download to.", default = None, required=False)
	parser.add_argument('-t', "--threads", dest="n_threads", type=int, help="Number of threads you want.", default=1, required=False)

	args = parser.parse_args()
	downloadFiles(args.file, args.format, args.output, int(args.n_threads))

	print("Time to run script: " + str(datetime.now() - startTime))
