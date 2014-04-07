#!/usr/bin/env python

import api
import gpu
import threads

# Customize these
card = '0'       # Card number, 0 is the first
mem_min = '1400' # The memory clock to start at
mem_max = '1500' # The memory clock to end at
mem_step = '1'   # The interval to try memory clocks at (1 = all, 2 = every other, etc.)
core_min = '1075' # The core clock to start at
core_max = '1100' # The core clock to end at
core_step = '1'  # The interval to try core clocks
desired_accuracy_in_mhs = 0.002 # The desired accuracy of samples in megahashes per second. .002 or .001 is recommended here
half_cycle_write = True # The desired frequency of writes made to file. Half cycle (True) writes at core min and at core max. Full cycle (False) only writes at core min


gpu_id = map(int, card.split(','))
m_min = map(int, mem_min.split(','))
m_max = map(int, mem_max.split(','))
m_step = map(int, mem_step.split(','))
c_min = map(int, core_min.split(','))
c_max = map(int, core_max.split(','))
c_step = map(int, core_step.split(','))

gpu_list = []
thread_list = []
sgminer = api.SGMiner()

for g in xrange(0, len(gpu_id)):
    gpu_list.append(gpu.Instance(sgminer, gpu_id[g], m_min[g], m_max[g], m_step[g], c_min[g], c_max[g], c_step[g], desired_accuracy_in_mhs, half_cycle_write))

for t in xrange(1, len(gpu_list)+1):
    t = threads.myThread(t, 'Thread-%i' % t, gpu_list[t-1])
    t.start()
    thread_list.append(t)

for t in thread_list:
    t.join()
print "Exiting Main Thread"

