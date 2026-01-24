#!/usr/bin/env python3
#python3 generateSW.py <n> <k>

import networkx as nx
import sys
import random
import numpy as np
import math

# --- KONFIGURACJA ---
LIMIT_STARTOW = 100       # Ile razy restartujemy algorytm (Nowe losowanie G)
KROKI_NA_TEMPERATURE = 50  # Ile ruchów robimy dla jednej temperatury (ważne! mała liczba)
                          # Jeśli dasz tu 2000, algorytm będzie bardzo wolny.

TEMP_START = 2.0          # Temperatura początkowa
TEMP_MIN = 0.001          # Temperatura końcowa
TEMPO_OCHLADZANIA = 0.95 # Jak szybko stygnie

EPSILON = 1e-9            # Margines błędu

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

def sprawdzanieEnergii(G):
    """
    Funkcja kosztu (Energia).
    Im blizej 0, tym graf bardziej calkowity.
    """
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

    # Pętla restartów (gdyby algorytm utknął i ostygł nie znajdując rozwiązania)
    while licznik < LIMIT_STARTOW:
        licznik = licznik + 1
        
        # 1. Start losowy
        G = nx.gnm_random_graph(n, k)
        while not nx.is_connected(G):
            G = nx.gnm_random_graph(n, k)
        
        terazEnergia = sprawdzanieEnergii(G)
        
        # Szybki test na start (rzadki przypadek)
        if terazEnergia < EPSILON:
            sys.stdout.write(nx.to_graph6_bytes(G, header=False).decode('ascii') + '\n')
            sys.stdout.flush()
            continue

        temperatura = TEMP_START

        # 2. Pętla Wyżarzania
        while temperatura > TEMP_MIN:
            
            # Pętla równowagi termicznej (zazwyczaj krótka)
            for _ in range(KROKI_NA_TEMPERATURE):
                
                listaKrawedzi = list(G.edges())
                listaNiekrawedzi = list(nx.non_edges(G))
                
                if not listaKrawedzi or not listaNiekrawedzi:
                    break

                # Mutacja: Przełączenie krawędzi
                a, b = random.choice(listaKrawedzi)
                c, d = random.choice(listaNiekrawedzi)

                G.remove_edge(a, b)
                G.add_edge(c, d)

                # Warunek konieczny: Spójność
                if not nx.is_connected(G):
                    G.add_edge(a, b)
                    G.remove_edge(c, d)
                    continue
                
                czyZaakceptowac = False

                nowaEnergia = sprawdzanieEnergii(G)
                delta = nowaEnergia - terazEnergia # O ile zmienił się błąd?

                # --- LOGIKA METROPOLISA ---
                if delta < 0:
                    # Jest lepiej (energia spadła) -> ZAWSZE akceptuj
                    czyZaakceptowac = True
                else:
                    # Jest gorzej (energia wzrosła) -> Akceptuj z p-stwem Boltzmanna
                    prawdopodobienstwo = math.exp(-delta / temperatura)
                    if random.random() < prawdopodobienstwo:
                        czyZaakceptowac = True
                
                # --- WYKONANIE ---
                if czyZaakceptowac:
                    terazEnergia = nowaEnergia

                    # Sprawdzenie sukcesu
                    if terazEnergia < EPSILON:
                        sys.stdout.write(nx.to_graph6_bytes(G, header=False).decode('ascii') + '\n')
                        sys.stdout.flush()
                        temperatura = -1 # Hack żeby wyjść z pętli while temperatura
                        break
                else:
                    # Odrzucamy zmianę -> Cofnij
                    G.add_edge(a, b)
                    G.remove_edge(c, d)
                
            # Schładzanie
            temperatura *= TEMPO_OCHLADZANIA


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass