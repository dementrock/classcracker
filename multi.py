#!/usr/bin/env python
# encoding: utf-8

import sys
import os
import tornado.ioloop
import tornado.web
import tornado.httpclient
import json

def main():
	reqs = {}
	results = {}
	parallel = 5
	output = open("result", "w")
	
	def on_finish(response):
		if response.error: result = repr(response.error)
		else: result = json.loads(response.body.decode('UTF-8'))
		for filename in reqs:
			if reqs[filename] == response.request:
				results[filename] = result
				print "Received answer <" + filename + ">"
		
		try:
			filename = filenames.pop(0)
			send_file(filename)
		except IndexError: 
			if len(results) == len(reqs):
				print >> output, json.dumps(results, indent=4)
				output.close()
				tornado.ioloop.IOLoop.instance().stop()
	
	def send_file(filename):
		f = open(filename, "rb")
		content = f.read()
		f.close()
		
		req = tornado.httpclient.HTTPRequest(url="http://www.google.com/speech-api/v1/recognize?lang=us-en", 
											method = "POST", 
											headers = {'Content-Type' : 'audio/x-flac; rate=16000'}, 
											body = content, 
											request_timeout = 60.0,
											)
		client = tornado.httpclient.AsyncHTTPClient()
		client.fetch(req, on_finish)
		reqs[filename] = req
		print "Sending request " + filename
	
	filenames = filter(lambda x:x.endswith(".flac"), os.listdir("."))
	
	for i in xrange(parallel):
		filename = filenames.pop(0)
		send_file(filename)
	
if __name__ == '__main__':
	tornado.ioloop.IOLoop.instance().add_callback(main)
	tornado.ioloop.IOLoop.instance().start()
	tornado.ioloop.IOLoop.instance().close()

