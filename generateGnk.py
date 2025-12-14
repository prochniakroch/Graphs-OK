#!/usr/bin/env python3
#python3 generateGnk.py <n> <k>

import networkx as nx
import sys
import random

LIMIT = 100000

def main():
    n = int(sys.argv[1])
    k = int(sys.argv[2])

    fraction_arg = sys.argv[3]
    if '/' in fraction_arg:
        parts = fraction_arg.split('/')
        seed_val = int(parts[0])
    
    random.seed(seed_val)
    count = 0

    while count < LIMIT:
        G = nx.gnm_random_graph(n, k)
        if nx.is_connected(G):
            sys.stdout.write(nx.to_graph6_bytes(G, header=False).decode('ascii') + '\n')
        count = count + 1

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass