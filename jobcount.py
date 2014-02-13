#!/usr/bin/env python
# -*- coding: utf-8 -*-

import commands, sys

output = commands.getstatusoutput("qstat -u '*'")
if output[0] != 0:
	print "ERROR"
	sys.exit()

rusers = {}
qwusers = {}

for line in output[1].split("\n"):
	items = line.split()
	if len(items) > 4 and items[4] == "r":
		slots = int(line[100:103])
		if items[3] in rusers.keys():
			rusers[items[3]] += slots
		else:
			rusers[items[3]] = slots

	if len(items) > 4 and items[4] == "qw":
		slots = int(line[100:103])
		if items[3] in qwusers.keys():
			qwusers[items[3]] += slots
		else:
			qwusers[items[3]] = slots

total = 0

users = set(rusers.keys() + qwusers.keys())

# set 0 for non-r user

for user in users:
	if not user in rusers.keys():
		rusers[user] = 0

call = sorted(users, key=lambda user: rusers[user])
call.reverse()

print ""
print "*: r, -: qw"
print ""

for user in call:
	jobs = rusers[user]
	print "*" * jobs + "-" * qwusers[user],
	print "%s : %d (%d)" % (user, jobs, qwusers[user])
	total += jobs

print ""
print "total : %d" % total
print ""

