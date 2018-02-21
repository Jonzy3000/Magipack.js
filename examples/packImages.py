#!/usr/bin/env python

import os, sys, getopt
import re
import json

def listFiles(path):
	if not path.endswith('/'): path += '/'
	files = os.listdir(path)
	arr = []
	for f in files:
		if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
			arr.append([path + f, f])
		if os.path.isdir(path + '/' + f):
			arr.extend(listFiles(path + f + '/'))
	return arr

def packImages(files):

	output = None
	data = []
	p = 0
	c = 0
	output = open("images.pack", "wb")
	for fn in files:
		f = open(fn[0], 'rb').read()
		shutil.copyfileobj(open(fn[0], 'rb'), output)
		l = len(f)
		data.append([fn[1], p, p + l, os.path.splitext(fn[1])[-1:][0]])
		p += l
		c += 1


	output.close()
	open('images.json', 'w').write(json.dumps(data))

def main(argv = None):
	path = '.'
	if argv == None:
		argv = sys.argv
	try:
		opts, args = getopt.getopt(argv[1:], "p:k:", [""])
		for option, value in opts:
			if option in ("-p"): path = value
	except Exception, e:
		pass
	if len(path) > 0 and path[-1] != '/': path = path + '/'
	packImages(listFiles(path))

if __name__ == "__main__":
	try:
		main()
	except Exception, e:
		print e
		pass
