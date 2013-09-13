import types

def checkType(isType=type(''), *arg):
	if len(arg) == 0:
		return False
	for a in arg:
		if type(a) != isType:
			return False
	return True
