"""
assumptions for now:

* fake events at 1 minute intervals?
* 10 minute intervals for analysis

"""



from collections import defaultdict
import itertools
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
			evt['etype'], evt['date'], evt['time'], evt['extra'] = line.strip().split(',',3)
			interval = list(time.strptime(evt['time'], '%I:%M %p'))[3:5] # I is 12 hour time!
			interval[1] = 15 * divmod(interval[1],15)[0]
			evt['interval'] = tuple(interval)
			yield evt


def fakeevent():
	return {'etype': ' '}


def dominantofinterval(events_in_interval):
	""" """
	#
	#print events_in_interval
	for x in ['Diaper','Sleep','Nurse']:
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


# 10 minute intervals
intervals = list(itertools.product(range(24),range(0,51,15)))


def cyclereport(data):
	# organize by days
	# print
	report_header = red("Report!",bold=True) + '\n'
	print report_header
	for day in sorted(data,reverse=True):
		print "%10s" % day,

		for interval in intervals:
			#print interval
			print dominantofinterval(data[day][interval])['etype'][0],

		print '\n',

'''
Alt algorithm:
for interval between max / min...
	find events in interval (including pseudo events like milking)
	print


'''

if __name__ == "__main__":
	import sys
	cyclereport(group_into_intervals(readactivities(open(sys.argv[1]))))
