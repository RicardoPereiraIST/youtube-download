# youtube-download

# **Description**
Using [youtube-dl](https://github.com/rg3/youtube-dl), downloads multiple files at once, with the possibility of using threads.
It's a command-line program to download multiple videos at once, by passing it a file with urls.
It requires the Python interpreter, and it should not be platform specific.

Only mp3 and mp4 formats are accepted, for now.
```
youtube-download.py input_file format [Options]
```

# **Options**
```
-h, --help                Print help text
-o, --output              Name the output folder (creates it, where the program is being run)
-t, --threads             Number of threads to run (default is 1)
```


Special thanks to [Rúben Anágua](https://github.com/rubenanagua) for quickly teaching me argparse and threads in python, and for the help in the division for each thread.
