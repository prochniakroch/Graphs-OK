#!/bin/bash
# KTZ 2025 
# plik: checkSW.sh
#./checkSW.sh 15 36 $((2**29)) 0 
 
n=$1
e=$2
mod=$3
pierwszy=$4
t=1
 
echo czas: $(date)  
 
for (( res=$pierwszy; res < $mod ; res+=1 ))
do 
 echo "time python3 generateSW.py $n $e $res/$mod 2>/dev/null | ./sito5 $t | tee -a wyniksw$n_$e.txt"
 echo "./checkSW.sh $n $e $mod $res" > sw_todo$n_$e.sh
 time python3 generateSW.py $n $e $res/$mod 2>/dev/null | ./sito5 $t | tee -a wyniksw$n_$e.txt
done 
 
echo czas: $(date) 
echo "# wszystko zrobione " > sw_todo$n_$e.sh