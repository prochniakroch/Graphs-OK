#!/bin/bash
# KTZ 2025 
# plik: checkGnkNauty.sh
#./checkGnkNauty.sh 15 36 $((2**29)) 0 

n=$1
e=$2
ilosc=$3
pierwszy=$4
t=640000
 
echo czas: $(date)  
 
for (( res=$pierwszy; res < $ilosc ; res+=1 ))
do 
    # Logowanie komendy, ktora za chwile sie wykona
    echo "time genrang -g -S$res $n $t -e$e 2>/dev/null | ./sito5 $t | tee -a wynikGnkNauty$n_$e.txt"
    
    # Wykonanie wlasciwe:
    # -S$res : Ustawia seed (ziarno) na numer pętli, zeby kazda paczka byla inna
    time genrang -g -S$res $n $t -e$e 2>/dev/null | ./sito5 $t | tee -a wynikGnkNauty$n_$e.txt
    
    # Aktualizacja pliku todo (zapis stanu)
    # POPRAWKA: Zmienilem $ilosc_partii na $ilosc
    echo "./checkGnkNauty.sh $n $e $ilosc $((res+1))" > gnkNauty_todo$n_$e.sh
done
#for (( res=$pierwszy; res < $mod ; res+=1 ))
#do 
# echo "time genrang -c $n $e:$e $res/$mod 2>/dev/null | ./sito5 $t | tee -a wynikGnkNauty$n_$e.txt"
# echo "./checkGnkNauty.sh $n $e $mod $res" > gnkNauty_todo$n_$e.sh
# time genrang -c $n $e:$e $res/$mod 2>/dev/null | ./sito5 $t | tee -a wynikGnkNauty$n_$e.txt
#done 
 
echo czas: $(date) 
echo "# wszystko zrobione " > gnkNauty_todo$n_$e.sh