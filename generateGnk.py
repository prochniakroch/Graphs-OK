#!/usr/bin/env python3
#python3 generateGnk.py <n> <k>
import networkx as nx
import sys
import random

# Ustawienie limitu generowanych grafów
LIMIT = 100000

def main():
    n = int(sys.argv[1])
    k = int(sys.argv[2])

    fraction_arg = sys.argv[3]
    if '/' in fraction_arg:
        parts = fraction_arg.split('/')
        seed_val = int(parts[0])
    
    # Ustawienie ziarna generatora liczb losowych, aby nie liczyć tego samego wiele razy
    random.seed(seed_val)
    count = 0

    # Główna pętla generująca grafy
    while count < LIMIT:
        # Generujemy losowy graf G(n,k)
        G = nx.gnm_random_graph(n, k)
        # Sprawdzamy czy jest spójny
        if nx.is_connected(G):
            # Jeśli tak, wypisujemy go w formacie graph6
            sys.stdout.write(nx.to_graph6_bytes(G, header=False).decode('ascii') + '\n')
        count = count + 1

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass