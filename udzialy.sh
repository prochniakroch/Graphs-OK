#!/bin/bash
# Statystyka udziału grafów całkowitych dla małych n

echo "n | k | Wszystkie | Calkowite | Udzial (%)"
echo "----------------------------------------------"

# Sprawdzamy dla n od 7 do 10 (dla n=15 to by trwalo wieki)
for n in {7..13}
do
    # Dla kazdego n sprawdzamy kilka roznych k (liczba krawedzi)
    # np. od n (minimum dla spojnego) do n+5
    min_k=$((n))
    max_k=$((n + 5))

    for (( k=$min_k; k<=$max_k; k++ ))
    do
        # 1. Liczymy WSZYSTKIE grafy spojne o n wierzcholkach i k krawedziach
        wszystkie=$(geng -c -q $n $k:$k | wc -l)

        # 2. Liczymy tylko CALKOWITE (przepuszczamy przez sito5)
        # Uzywamy sito5 z malym buforem (np. 1), bo geng podaje po kolei
        calkowite=$(geng -c -q $n $k:$k | ./sito5 1 | wc -l)

        # 3. Obliczamy procent (jesli wszystkie > 0)
        if [ "$wszystkie" -gt 0 ]; then
             udzial=$(awk "BEGIN {printf \"%.4f\", ($calkowite/$wszystkie)*100}")
        else
             udzial="0"
        fi

        echo "$n | $k | $wszystkie | $calkowite | $udzial%"
    done
done