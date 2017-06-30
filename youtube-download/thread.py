import threading
import os

class MyThread(threading.Thread):
  def __init__(self, sublist, dir_path, format):
      threading.Thread.__init__(self)
      self.sublist = sublist
      self.path = dir_path
      self.format = format

  def run(self):
    for url in self.sublist:
      if(self.format == "mp3"):
        os.system("youtube-dl --output " + self.path + "\\%(title)s.%(ext)s --extract-audio --audio-format mp3 --audio-quality 0 " + url)
      if(self.format == "mp4"):
        os.system("youtube-dl --output " + self.path + "\\%(title)s.%(ext)s -f bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio --merge-output-format mp4 " + url)