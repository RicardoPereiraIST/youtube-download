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

def read_file(file_to_read):
	with open(file_to_read, "r") as f:
		lines = f.read().splitlines()
	f.close()
	return lines

def parse_urls(lines):
	urls = []
	for line in lines:
		if("list=" in line):
			parent_url = ''
			if("watch?v=" in line):
				parent_url = line.split("watch?v=")[0] + "watch?v="
			else:
				parent_url = line.split("playlist?list=")[0] + "watch?v="

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

	return urls

def create_dir(file_to_read):
	dir_path = os.path.dirname(os.path.realpath(file_to_read))
	dir_path = os.path.join(dir_path, "youtube_dl-"+datetime.now().strftime('%Y-%m-%d_%H-%M-%S'))
	if not os.path.exists(dir_path):
		os.makedirs(dir_path)
	return dir_path

def create_threads(n_threads, urls_per_thread, dir_path, format):
	threads = []
	for i in range(0, n_threads):
		if urls_per_thread[i] is not None:
			threads.append(MyThread(urls_per_thread[i], dir_path, format))
		else:
			break
	return threads

def set_urls_per_thread(urls, n_threads):
	urls_per_thread = [] 
	for i in range(0, n_threads):
		max_elements = int(math.ceil(float(len(urls))/(n_threads - i)))
		url_sublist = urls[:max_elements]
		urls = urls[max_elements:]
		urls_per_thread.append(url_sublist or None)
	return urls_per_thread

def run_threads(threads):
	for thread in threads:
	    thread.start()

	for thread in threads:
	    thread.join()

def download_files(file_to_read, format, output = None, n_threads = 1):
	lines = read_file(file_to_read)
	urls = parse_urls(lines)
	dir_path = output if output != None else create_dir(file_to_read)
	n_threads = max(1, min(n_threads, len(urls)))
	urls_per_thread = set_urls_per_thread(urls, n_threads)
	threads = create_threads(n_threads, urls_per_thread, dir_path, format)
	run_threads(threads)

if __name__ == '__main__':
	startTime = datetime.now()

	parser = argparse.ArgumentParser(description='Youtube downloader')
	parser.add_argument('file', help="Name of the file you want to read from.")
	parser.add_argument('format', help="Format you want to download.")
	parser.add_argument('-o', "--output", dest="output", help="Name of the folder you want to download to.", default = None, required=False)
	parser.add_argument('-t', "--threads", dest="n_threads", type=int, help="Number of threads you want.", default=1, required=False)

	args = parser.parse_args()
	download_files(args.file, args.format, args.output, int(args.n_threads))

	print("Time to run script: " + str(datetime.now() - startTime))