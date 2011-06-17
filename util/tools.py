from time import time
from sys import stderr


clocks = {"main":time()}
op = ''

def poke(clockId="", msg=""):
	global clocks, op
	now = time()

	if not clockId:
		clockId = "main"
	if not clocks.get(clockId,False):
		clocks[clockId] = now
	if msg != 'none':
		op += ("%3f:\t%s: %s\n" % ((now-clocks[clockId])*1000, clockId, msg))
	clocks[clockId] = now

def output():
	stderr.write(op)
