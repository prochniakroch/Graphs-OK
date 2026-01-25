#!/usr/bin/env python3
#python3 generateZL.py <n> <k>

import networkx as nx
import sys
import random
import numpy as np

LIMIT_KROKOW = 2000 # Liczba prób na jeden graf
LIMIT = 100 # Ile grafów próbujemy wygenerować
EPSILON = 1e-9 # Margines bledu

# --- POBIERANIE WARTOŚCI ---
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

# --- SPRAWDZANIE JAKOŚCI GRAFU ---
def sprawdzanieJakosci(G):
    try:
        macierz = nx.to_numpy_array(G) # Zamiana na macierz sąsiedztwa
        wartosci = np.linalg.eigvalsh(macierz) # Obliczanie wartości własnych (widma)
        blad = sum(abs(w - round(w)) for w in wartosci) # Suma odchyleń od najbliższej liczby całkowitej (im bliżej 0, tym lepiej)
        return blad # Zwracamy jakość
    except:
        return float('inf')

# --- GŁÓWNA FUNKCJA ---
def main():
    # Ustawianie wartości n, k, seed
    n, k, seed_val = zczytywanieWartosci()
    
    # Ustawienie ziarna generatora liczb losowych, aby nie liczyć tego samego wiele razy
    random.seed(seed_val)
    np.random.seed(seed_val)
    licznik = 0

    # Główna pętla generująca grafy (LIMIT)
    while licznik < LIMIT:
        licznik = licznik + 1

        # 1. Start - generuj losowy graf G(n,k)
        G = nx.gnm_random_graph(n, k)
        # Sprawdzanie spójności
        while not nx.is_connected(G):
            G = nx.gnm_random_graph(n, k)
        
        terazJakosc = sprawdzanieJakosci(G)

        # Szybki test na start (rzadki przypadek)
        if(terazJakosc < EPSILON):
            sys.stdout.write(nx.to_graph6_bytes(G, header=False).decode('ascii') + '\n')
            sys.stdout.flush()
        
        iloscPoprawek = 0

        # 2. Pętla Poprawek
        while iloscPoprawek < LIMIT_KROKOW:
            listaKrawedzi = list(G.edges())
            listaNiekrawedzi = list(nx.non_edges(G))

            # Jeśli nie ma krawędzi do zamiany, przerywamy
            if not listaKrawedzi or not listaNiekrawedzi: 
                break
            
            # Wybieramy losowo krawędź do usunięcia i niekrawędź do dodania
            a, b = random.choice(listaKrawedzi)
            c, d = random.choice(listaNiekrawedzi)
            G.remove_edge(a, b)
            G.add_edge(c, d)


            # Sprawdzanie spójności
            if not nx.is_connected(G):
                G.add_edge(a, b)
                G.remove_edge(c, d)
                iloscPoprawek = iloscPoprawek + 1
                continue
            
            # 3. Sprawdzanie jakości
            nowaJakosc = sprawdzanieJakosci(G)
            if nowaJakosc < terazJakosc:
                #jest lepiej, zostawiamy zmiane
                terazJakosc = nowaJakosc
                iloscPoprawek = 0

                if terazJakosc < EPSILON:
                    sys.stdout.write(nx.to_graph6_bytes(G, header=False).decode('ascii') + '\n')
                    sys.stdout.flush()
            else:
                #jest gorzej, cofamy zmiane
                G.add_edge(a, b)
                G.remove_edge(c, d)
                iloscPoprawek = iloscPoprawek + 1

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass