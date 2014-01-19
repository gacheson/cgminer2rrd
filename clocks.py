#!/usr/bin/env python

from itertools import product
import api
import numpy as np
import os
import scipy as sp
import scipy.stats
import sys
import time

csv='mhs.csv'
card = 1

mem_min = 1250
mem_max = 1460
mem_step = 3
core_min = 830
core_max = 890
core_step = 1
desired_accuracy_in_mhs = 0.002
infinity = 1.0e24

clock_command = 'aticonfig --adapter=all --odsc=%i,%i >/dev/null'

sgminer = api.SGMiner()

def mean_confidence(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    if n == 0:
      print "not enough data"
      return infinity
    m, se = np.mean(a), scipy.stats.sem(a)
    h = se * sp.stats.t._ppf((1+confidence)/2., n-1)
    print "h: " + str(h)
    return h

skip = []
try:
    with open(csv, 'r') as output:
        for mem, core, mhz in [_.split(',') for _ in output]:
            if mem != "mem":
                skip.append((int(mem),int(core)))
except IOError:
    with open(csv, 'w') as output:
    	output.write('mem,core,mhs\n')
    pass

with open(csv, 'a') as output:
    for mem, core in product(
        xrange(mem_min, mem_max+1, mem_step),
        xrange(core_min, core_max+1, core_step)
    ):
        if not (mem, core) in skip:
            os.system(clock_command % (core,mem))
            print 'adjusting clock to %i,%i' % (mem, core)

            samples = []
            time.sleep(10) # wait 15s for first sample, 5s else
            while len(samples) < 3 or mean_confidence(samples) > desired_accuracy_in_mhs:
              time.sleep(5)
              sample = sgminer.devs()[card]['MHS 5s']
              samples.extend([sample])
            mhs = np.mean(np.array(samples))

            output.write('%i,%i,%f\n' % (mem, core, mhs))
            output.flush()

            print '%i,%i,%f' % (mem, core, mhs)
            sys.stdout.flush()
