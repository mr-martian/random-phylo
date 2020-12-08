#!/usr/bin/env python3

import sys
import numpy

with open(sys.argv[1]) as f:
    lines = f.read().splitlines()
    nums = [[int(x) for x in l.strip().split('\t')] for l in lines[1:] if l]
    print(sys.argv[1])
    print(lines[0])
    for i in range(len(nums[0])):
        col = [x[i] for x in nums]
        print('%s±%s' % (round(numpy.average(col), 2), round(numpy.std(col), 2)), end='\t')
    print('')
