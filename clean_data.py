#!/usr/bin/env python3

import sys
with open(sys.argv[1]) as f:
    name = 'clean' + sys.argv[1].replace(' 0.', '_')
    num = sys.argv[1].split()[0].split('_')[-1]
    with open(name, 'w') as out:
        lines = f.read().splitlines()
        out.write('\t'.join(lines[0].split('\t')[2::2]) + '\n')
        for line in lines:
            ls = line.split('\t')
            if ls[1] == num:
                out.write('\t'.join(ls[3::2]) + '\n')

