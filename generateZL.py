#!/usr/bin/env python3
#python3 generateZL.py <n> <k>

import networkx as nx
import sys
import random
import numpy as np

LIMIT_KROKOW = 2000
LIMIT = 100
EPSILON = 1e-9 #margines bledu

def zczytywanieWartosci():
    if len(sys.argv) < 4:
        return 15, 36, 0
    try:
        n = int(sys.argv[1])
        k = int(sys.argv[2])
        arg3 = sys.argv[3]
        if '/' in arg3:
            seed_val = int(arg3.split('/')[0])
        else:
            seed_val = int(arg3)
        return n, k, seed_val
    except:
        return 15, 36, 0

def sprawdzanieJakosci(G):
    try:
        macierz = nx.to_numpy_array(G)
        wartosci = np.linalg.eigvalsh(macierz)
        blad = sum(abs(w - round(w)) for w in wartosci)
        return blad
    except:
        return float('inf')

def main():
    n, k, seed_val = zczytywanieWartosci()
    
    random.seed(seed_val)
    np.random.seed(seed_val)
    licznik = 0

    while licznik < LIMIT:
        licznik = licznik + 1

        G = nx.gnm_random_graph(n, k)
        while not nx.is_connected(G):
            G = nx.gnm_random_graph(n, k)
        
        terazJakosc = sprawdzanieJakosci(G)

        if(terazJakosc < EPSILON):
            sys.stdout.write(nx.to_graph6_string(G) + '\n')
            sys.stdout.flush()
            return G
        
        iloscPoprawek = 0

        while iloscPoprawek < LIMIT_KROKOW:
            listaKrawedzi = list(G.edges())
            listaNiekrawedzi = list(nx.non_edges(G))
            if not listaKrawedzi or not listaNiekrawedzi: 
                break

            a, b = random.choice(listaKrawedzi)
            c, d = random.choice(listaNiekrawedzi)
            G.remove_edge(a, b)
            G.add_edge(c, d)


            #sprawdzanie spojnosci
            if not nx.is_connected(G):
                G.add_edge(a, b)
                G.remove_edge(c, d)
                iloscPoprawek = iloscPoprawek + 1
                continue

            nowaJakosc = sprawdzanieJakosci(G)
            if nowaJakosc < terazJakosc:
                #jest lepiej, zostawiamy zmiane
                terazJakosc = nowaJakosc
                iloscPoprawek = 0

                if terazJakosc < EPSILON:
                    sys.stdout.write(nx.to_graph6_string(G) + '\n')
                    sys.stdout.flush()
                    return G
            else:
                G.add_edge(a, b)
                G.remove_edge(c, d)
                iloscPoprawek = iloscPoprawek + 1

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass