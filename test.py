import urllib2
FILE='test.flac'
url = 'http://www.google.com/speech-api/v1/recognize?lang=us-en'
audio=open(FILE,'rb').read()
headers = {'Content-Type' : 'audio/x-flac; rate=22050'}
req = urllib2.Request(url, audio, headers)
response = urllib2.urlopen(req)
print response.read().decode('UTF-8')
