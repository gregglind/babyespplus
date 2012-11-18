"""
assumptions for now:

* fake events at 1 minute intervals?
* 10 minute intervals for analysis

"""

from __future__ import print_function


INTERVAL = 10 # minutes

def print2(*args,**kwargs):
	myargs = {'end':''}
	myargs.update(kwargs)
	print(*args,**myargs)

from collections import defaultdict
import itertools
import re
import time

# from https://github.com/fabric/fabric/blob/master/fabric/colors.py
def _wrap_with(code):

    def inner(text, bold=False,underline=False):
        c = code
        if bold:
            c = "1;%s" % c
        if underline:
        	c = "4:%s" % c
        return "\033[%sm%s\033[0m" % (c, text)
    return inner

red = _wrap_with('31')
green = _wrap_with('32')
yellow = _wrap_with('33')
blue = _wrap_with('34')
magenta = _wrap_with('35')
cyan = _wrap_with('36')
white = _wrap_with('37')




"""


import calendar
import datetime
calendar.timegm(datetime.date(2012,9,1).timetuple())

"""

"""
Data types

milk
pee
poo
sleep


Diaper,11/16/2012,5:47 PM,Pee and Poop,Caught
"""

class Babyevent(object):
	""" superclass of all baby events"""
	pass

class Milk(Babyevent):
	def str():pass

class Milk(Babyevent):
	def str():pass

def readactivities(fh):
	'''
	does all the parsing... gross!
	'''
	for line in fh.readlines()[2:]:
		if line.strip():
			evt = dict()
			evt['otype'], evt['date'], evt['time'], evt['extra'] = line.strip().split(',',3)
			interval = list(time.strptime(evt['time'], '%I:%M %p'))[3:5] # I is 12 hour time!
			interval[1] = INTERVAL * divmod(interval[1],INTERVAL)[0]
			evt['interval'] = tuple(interval)

			# process events some here....
			otype = evt['otype']
			etype = ''
			if otype == 'Diaper':
				if 'Poop' in evt['extra'].split(',')[0]:
					etype = 'Poop'
				else:
					etype = 'Pee'

				evt['caught'] = bool(re.search('(catch|caught)', evt['extra'],re.I))


			else:
				etype = otype

			evt['etype'] = etype
			yield evt


def fakeevent():
	return {'etype': ' '}


def dominantofinterval(events_in_interval):
	""" """
	#
	#print events_in_interval
	for x in ['Poop','Pee','Diaper','Sleep','Nurse']:
		for e in events_in_interval:
			if e['etype'] == x:
				return e

	return fakeevent()


def group_into_intervals(all_events):
	D = defaultdict(lambda: defaultdict(list))
	# get day of event
	# get time of event
	for evt in all_events:
		D[evt['date']][evt['interval']].append(evt)

	return D


intervals = list(itertools.product(range(24),range(0,60,INTERVAL)))


def cyclereport(data):
	# organize by days
	# print
	print(red("Report!"), " -- ",
		yellow('pee'),green('poop'),blue('nursing'))

	hrfmt = "%%-%ss" % (60/INTERVAL)
	print(" "*14 + "".join([hrfmt % i for i in range(24)]))

	for day in sorted(data,reverse=True):
		print2("%-14s" % day)

		for interval in intervals:
			#print interval
			dom = dominantofinterval(data[day][interval])
			et = dom['etype']
			## gross, formatting should live elsewhere
			if et == 'Poop':
				print2(green('B',underline=dom['caught']))
			elif et == 'Pee':
				print2(yellow('p',underline=dom['caught']))
			elif et == 'Nurse':
				print2(blue('n'))
			else:
				print2(' ')

		print('')

'''
Alt algorithm:
for interval between max / min...
	find events in interval (including pseudo events like milking)
	print


'''

if __name__ == "__main__":
	import sys
	cyclereport(group_into_intervals(readactivities(open(sys.argv[1]))))
