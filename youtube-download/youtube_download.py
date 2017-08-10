#!python

import os
import sys
from datetime import datetime
from time import sleep
import threading
import math
import subprocess
from thread import MyThread
import argparse

def downloadFiles(file, format, output = None, n_threads = 1):
	with open(file, "r") as f:
		lines = f.read().splitlines()
	f.close()

	urls = []
	for line in lines:
		if("list=" in line):
			parent_url = line.split("watch?v=")[0] + "watch?v="
			result = subprocess.check_output(["youtube-dl", "-j", "--flat-playlist", line])
			result = result.decode('utf-8')
			list_of_files = result.split("\n")
			for _files in list_of_files:
				_file = _files.split(',')
				for _ids in _file:
					if "\"url\":" in _ids:
						url = _ids.split("\"url\": ")[1]
						if("}" in url):
							url = url[:-1]
						url = url[1:-1]
						urls.append(parent_url + url)
		else:
			urls.append(line)

	dir_path = output

	if(dir_path is None):
		dir_path = os.path.dirname(os.path.realpath(file))
		dir_path = os.path.join(dir_path, "youtube_dl-"+datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
		if not os.path.exists(dir_path):
			os.makedirs(dir_path)

	if(n_threads > len(urls)):
		n_threads = len(urls)
	if(n_threads < 1):
		n_threads = 1

	threads = []
	
	urls_per_thread = [] 
	for i in range(0, n_threads):
		max_elements = int(math.ceil(float(len(urls))/(n_threads - i)))
		url_sublist = urls[:max_elements]
		urls = urls[max_elements:]
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
