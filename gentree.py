#!/usr/bin/env python3

import random

class Tree:
    def __init__(self, nchar):
        # root of tree is at time -1 with immediate branching
        self.now = 0
        self.nchar = nchar
        self.taxa = [[random.randint(0,1) for i in range(nchar)],
                     [random.randint(0,1) for i in range(nchar)]]
        self.extinct = []
        self.tips = [0, 1]
        self.children = {}
        self.branches = [1, 1]
        self.dates = [0, 0]
    def print_taxa(self, f, with_extinct=False):
        f.write('BEGIN Taxa;\n')
        taxa = self.tips[:]
        if with_extinct:
            taxa += self.extinct
        f.write('DIMENSIONS ntax=%s;\n' % len(taxa))
        f.write('TAXLABELS\n')
        for i in taxa:
            f.write("'Taxon%s'\n" % i)
        f.write(';\nEND;\n\n')
    def print_subtree(self, f, node):
        if node in self.tips or node in self.extinct:
            f.write('Taxon%s' % node)
        else:
            f.write('(')
            for i, n in enumerate(self.children[node]):
                if i != 0:
                    f.write(',')
                self.print_subtree(f, n)
            f.write(')')
        if self.branches[node] > 0:
            f.write(':%s' % self.branches[node])
    def write_tree(self, fname):
        with open(fname, 'w') as f:
            f.write('#nexus\n\n')
            self.print_taxa(f, with_extinct=True)
            f.write('BEGIN trees;\n')
            f.write('tree TREE1 = (')
            self.print_subtree(f, 0)
            f.write(',')
            self.print_subtree(f, 1)
            f.write(');\nEND;\n')
    def write_matrix(self, fname):
        with open(fname, 'w') as f:
            f.write('#nexus\n\n')
            self.print_taxa(f)
            f.write('BEGIN Characters;\n')
            f.write('DIMENSIONS nchar=%s;\n' % self.nchar)
            f.write('FORMAT\n\tdatatype=STANDARD missing=? gap=- symbols="01" labels=left transpose=no interleave=yes;\n')
            f.write('MATRIX\n')
            for i in self.tips:
                f.write("'Taxon%s' %s\n" % (i, ''.join(map(str, self.taxa[i]))))
            f.write(';\nEND;\n')
    def step(self, borrowing_rate, change_rate, branch_rate, extinction_rate):
        self.now += 1
        newtips = []
        for t in self.tips:
            if random.random() < extinction_rate:
                self.extinct.append(t)
            elif random.random() < branch_rate:
                l, r = len(self.taxa), len(self.taxa) + 1
                newtips += [l, r]
                self.taxa += [self.taxa[t][:], self.taxa[t][:]]
                self.children[t] = [l, r]
                self.branches += [1, 1]
                self.dates += [self.now, self.now]
            else:
                self.dates[t] += 1
                self.branches[t] += 1
                newtips.append(t)
        self.tips = newtips
        for t in self.tips:
            other = set(self.tips)
            other.remove(t)
            neighbor = -1
            if len(other) > 0:
                neighbor = random.choice(list(other))
            for i in range(self.nchar):
                if neighbor != -1 and random.random() < borrowing_rate:
                    self.taxa[t][i] = self.taxa[neighbor][i]
                elif random.random() < change_rate:
                    self.taxa[t][i] = 1 - self.taxa[t][i]
    def simulate(self, steps, borrowing_rate, change_rate, branch_rate, extinction_rate):
        for i in range(steps):
            #print('iteration %s (%s live tips)' % (i, len(self.tips)))
            self.step(borrowing_rate, change_rate, branch_rate, extinction_rate)
    def data_loss(self, taxon_rate, character_rate):
        newtips = []
        for t in self.tips:
            if random.random() < taxon_rate:
                self.extinct.append(t)
            else:
                newtips.append(t)
        self.tips = newtips
        for t in self.tips:
            for i in range(self.nchar):
                if random.random() < character_rate:
                    self.taxa[t][i] = '?'
    def select_tips(self, taxon_count, character_rate):
        random.shuffle(self.tips)
        self.extinct += self.tips[taxon_count:]
        self.tips = self.tips[:taxon_count]
        self.data_loss(0, character_rate)

if __name__ == '__main__':
    import sys
    taxa_arg = sys.argv[1]
    change_rate = float(sys.argv[2])
    t = Tree(200)
    t.simulate(100, 0, change_rate, 0.05, 0)
    if '.' in taxa_arg:
        t.data_loss(float(taxa_arg), 0)
    else:
        t.select_tips(int(taxa_arg), 0)
    print('tips\t%s' % len(t.tips), end='\t')
    t.write_tree('random_tree.nex')
    t.write_matrix('random_matrix.nex')
