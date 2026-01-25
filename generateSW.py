#!/usr/bin/env python3
#python3 generateSW.py <n> <k>

import networkx as nx
import sys
import random
import numpy as np
import math

# --- KONFIGURACJA ---
#LIMIT_STARTOW = 100       # Ile razy restartujemy algorytm (Nowe losowanie G)
#KROKI_NA_TEMPERATURE = 50  # Ile ruchów robimy dla jednej temperatury (ważne! mała liczba)
#                          # Jeśli dasz tu 2000, algorytm będzie bardzo wolny.
#
#TEMP_START = 2.0          # Temperatura początkowa
#TEMP_MIN = 0.001          # Temperatura końcowa
#TEMPO_OCHLADZANIA = 0.95 # Jak szybko stygnie
#
EPSILON = 1e-9            # Margines błędu


# --- KONFIGURACJA "GŁĘBOKIE SZUKANIE" ---
LIMIT_STARTOW = 100000000  # Praktycznie nieskończoność. Wyłączysz ręcznie.
KROKI_NA_TEMPERATURE = 300 # Daj mu czas na eksplorację
                          
TEMP_START = 1.0           # Startujemy spokojniej
TEMP_MIN = 0.0001          # Schodzimy niżej z temperaturą
TEMPO_OCHLADZANIA = 0.99   # Bardzo powolne stygnięcie (klucz do sukcesu)

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

# --- GŁÓWNA FUNKCJA ---
def main():
    # Ustawianie wartości n, k, seed
    n, k, seed_val = zczytywanieWartosci()
    
    random.seed(seed_val)
    np.random.seed(seed_val)

    licznik = 0

    # Główna pętla generująca grafy (LIMIT_STARTOW)
    while licznik < LIMIT_STARTOW:
        licznik = licznik + 1
        
        # 1. Start - generuj losowy graf G(n,k)
        G = nx.gnm_random_graph(n, k)
        # Sprawdzanie spójności (musi być spójny)
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
        # im wyższa temperatura, tym większa szansa na zaakceptowanie gorszego stanu
        # im niższa temperatura, tym bardziej zachłanny algorytm
        while temperatura > TEMP_MIN:
            #sys.stderr.write(f"\r[Seed: {seed_val}] Temp: {temperatura:.6f} | Energia: {terazEnergia:.4f}   ")
            #sys.stderr.flush()

            # Pętla równowagi termicznej (zazwyczaj krótka)
            for _ in range(KROKI_NA_TEMPERATURE):
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

                    # Sprawdzamy czy jest wystarczająco dobrze
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