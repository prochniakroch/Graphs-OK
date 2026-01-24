# Graphs-OK
Generowanie spójnych grafów całkowitych (n = 15, k = 36) z użyciem heurystyk i metaheurystyk

Kompilacja:
    1. Zainstalowanie pakietu nauty
    2. Dodanie scieżki do systemu (wymagane do poprawnego działania algorytmu dokładnego)
    3. Kompilacja sito5.c

Sposoby generowania grafów:
    1. Algorytm dokładny (geng)
    2. Algorytm losowy (generateGnk.py)
    3. Algorytm zachłanny ulosowiony (generateZL.py)
    4. Algorytm symulowanego wyżarzania (generateSW.py)

Ogólna zasada działania:
    1. Odpalenie skryptu do danego algorytmu tj. 
        - calkowite15.sh -> dokładny
        - checkGnk.sh -> gnk
        - checkZL.sh -> zachłanny ulusowiony
        - checkSW.sh -> symulowane wyżarzanie
    2. Ustawienie wartości n = 15, k = 36, przesteń 2^29 i od którego momentu ma rozpocząć 0
    3. Skrypt uruchamia dany algorytm aż do przeszukania całej przestrzeni
    4. Algorytmy generują i sprawdzają czy dany graf jest spójny jeśli tak to
    5. sito5 sprawdza czy graf jest całkowity i spójny, generalnie przesiewa nasze wyniki 
    6. Do plików z wynikami zapisywane są tylko i wyłącznie grafy które spełniają nasze założenia
