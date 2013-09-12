ERROR = 'ERROR'
INFO = 'INFO'

def log(level, msg):
	print ''.join((level, ':', msg))