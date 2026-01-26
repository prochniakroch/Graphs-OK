#!/usr/bin/env python3
#python3 generateZL.py <n> <k>

import networkx as nx
import sys
import random
import numpy as np
import os

LIMIT_KROKOW = 2000 # Liczba prób na jeden graf
LIMIT = 100 # Ile grafów próbujemy wygenerować
EPSILON = 1e-9 # Margines bledu

NAJBLIZSZE_GRAFY = [] # Przechowuje (jakosc, graf w formacie graph6)

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

# --- SPRAWDZANIE ENERGII GRAFU ---
def sprawdzanieEnergii(G):
    try:
        macierz = nx.to_numpy_array(G) # Zamiana na macierz sąsiedztwa
        wartosci = np.linalg.eigvalsh(macierz) # Obliczanie wartości własnych (widma)
        blad = sum(abs(w - round(w)) for w in wartosci) # Suma odchyleń od najbliższej liczby całkowitej (im bliżej 0, tym lepiej)
        return blad # Zwracamy energię
    except:
        return float('inf')

# --- NAJBLIZSZE GRAFY TOP3 ---
def top3(G, energia, n, k):
    global NAJBLIZSZE_GRAFY

    graf = nx.to_graph6_bytes(G, header=False).decode('ascii').strip()

    # Sprawdzamy czy graf już jest zapisany, aby nie było duplikatów
    for j, zapisaneGrafy in NAJBLIZSZE_GRAFY:
        if zapisaneGrafy == graf:
            return
    
    # Dodajemy do listy, jeśli jest miejsce lub jeśli energia jest lepsza niż najgorsza w top3
    if len(NAJBLIZSZE_GRAFY) < 3 or energia < NAJBLIZSZE_GRAFY[-1][0]:
        NAJBLIZSZE_GRAFY.append((energia, graf))

        NAJBLIZSZE_GRAFY.sort(key=lambda x: x[0]) # Sortujemy po energii
        NAJBLIZSZE_GRAFY = NAJBLIZSZE_GRAFY[:3] # Trzymamy tylko top 3

        nazwa_pliku = f"TOP3_ZL_N={n}_K={k}.txt"
        with open(nazwa_pliku, "w") as x:
            x.write(f"# TOP 3 grafy o najniższej energii dla N={n}, K={k}\n")
            x.write(f"# Format: energia grafu, graf w formacie graph6\n")
            for j, g in NAJBLIZSZE_GRAFY:
                x.write(f"{j:.8f} {g}\n")

# --- WCZYTYWANIE TOP3 Z PLIKU (aby nie czyściło go po zmianie ziarna) ---
def wczytajtop3(n, k):
    global NAJBLIZSZE_GRAFY
    nazwa_pliku = f"TOP3_ZL_N={n}_K={k}.txt"

    if not os.path.exists(nazwa_pliku): # Sprawdzamy czy plik istnieje
        return

    try:
        with open(nazwa_pliku, "r") as x:
            lines = x.readlines()[2:] # Pomijamy nagłówki
            for line in lines:
                parts = line.strip().split()
                energia = float(parts[0])
                graf = parts[1]
                NAJBLIZSZE_GRAFY.append((energia, graf))
        NAJBLIZSZE_GRAFY.sort(key=lambda x: x[0]) # Sortujemy po jakości
        NAJBLIZSZE_GRAFY = NAJBLIZSZE_GRAFY[:3] # Trzymamy tylko top 3
    except Exception as e:
        sys.stderr.write(f"\rBłąd przy wczytywaniu pliku TOP3: {e}\n")

# --- GŁÓWNA FUNKCJA ---
def main():
    # Ustawianie wartości n, k, seed
    n, k, seed_val = zczytywanieWartosci()

    # Wczytujemy poprzednie top3
    wczytajtop3(n, k)
    
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
        
        terazEnergia = sprawdzanieEnergii(G)

        # Zapisywanie do top3
        top3(G, terazEnergia, n, k) 

        # Szybki test na start (rzadki przypadek)
        if(terazEnergia < EPSILON):
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

            # 3. Sprawdzanie energii
            nowaEnergia = sprawdzanieEnergii(G)

            # Zapisywanie do top3
            top3(G, nowaEnergia, n, k)

            if nowaEnergia < terazEnergia:
                #jest lepiej, zostawiamy zmiane
                terazEnergia = nowaEnergia
                iloscPoprawek = 0

                if terazEnergia < EPSILON:
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