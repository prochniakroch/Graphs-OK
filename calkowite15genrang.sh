#!/bin/bash
# Plik: calkowite15genrang.sh
# Wersja ostateczna: Cicha praca, szukanie n=15 k=36
# Użycie: ./calkowite15genrang.sh 15 36 10000 0

n=$1
e=$2
limit_petli=$3   # Ile razy powtórzyć generowanie paczki
start_seed=$4    # Od jakiego numeru ziarna zacząć
t=640000         # Wielkość bufora dla sito5

# Generujemy 2 miliony grafów w paczce, żeby po odrzuceniu niespójnych
# na pewno starczyło do wypełnienia bufora sito5 (który ma 640k)
ILOSC_W_PACZCE=2000000

echo "=== Start poszukiwań: $(date) ==="
echo "=== Parametry: n=$n, e=$e, Paczka=$ILOSC_W_PACZCE, Bufor=$t ==="
echo "=== Czekaj cierpliwie. Wyniki pojawią się tylko jak coś znajdę. ==="

for (( seed=$start_seed; seed < $limit_petli ; seed+=1 ))
do
    # Wyświetlamy licznik w jednej linii (nadpisuje się), żebyś widział, że program żyje
    echo -ne "Przetwarzanie seed: $seed / $limit_petli ... \r"

    # Zapisujemy plik "resume" w razie przerwania
    echo "./calkowite15genrang.sh $n $e $limit_petli $seed" > genrang_todo${n}_${e}.sh

    # === POTOK (PIPELINE) ===
    # 1. genrang -q: cichy generator, -S: seed, -e: krawędzie
    # 2. pickg -c1: przepuszcza TYLKO grafy spójne (ukrywamy błędy 2>/dev/null)
    # 3. sito5: sprawdza całkowitość
    # 4. grep .: blokuje puste linie, puszcza tylko wyniki
    # 5. tee: wypisuje na ekran I do pliku
    
    genrang -q -S$seed -e$e $n $ILOSC_W_PACZCE 2>/dev/null | pickg -c1 2>/dev/null | ./sito5 $t | grep . | tee -a wynikgenrang${n}_${e}.txt

done

echo ""
echo "Koniec: $(date)"
echo "# wszystko zrobione " > genrang_todo${n}_${e}.sh