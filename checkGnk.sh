#!/bin/bash
# KTZ 2025 
# plik: checkGnk.sh
#./checkGnk.sh 15 36 $((2**29)) 0 
 
n=$1
e=$2
mod=$3
pierwszy=$4
t=100000
 
echo czas: $(date)  
 
for (( res=$pierwszy; res < $mod ; res+=1 ))
do 
 echo "time python3 generateGnk.py $n $e $res/$mod 2>/dev/null | ./sito5 $t | tee -a wynikGnk$n_$e.txt"
 echo "./checkGnk.sh $n $e $mod $res" > gnk_todo$n_$e.sh
 time python3 generateGnk.py $n $e $res/$mod 2>/dev/null | ./sito5 $t | tee -a wynikGnk$n_$e.txt
done 
 
echo czas: $(date) 
echo "# wszystko zrobione " > gnk_todo$n_$e.sh