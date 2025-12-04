#!/bin/bash
# KTZ 2025 
# plik: checkZL.sh
#./checkZL.sh 15 36 $((2**29)) 0 
 
n=$1
e=$2
mod=$3
pierwszy=$4
t=640000
 
echo czas: $(date)  
 
for (( res=$pierwszy; res < $mod ; res+=1 ))
do 
 echo "time python3 generateZL.py $n $e $res/$mod 2>/dev/null | ./sito5 $t | tee -a wynikzl$n_$e.txt"
 echo "./checkZL.sh $n $e $mod $res" > zl_todo$n_$e.sh
 time python3 generateZL.py $n $e $res/$mod 2>/dev/null | ./sito5 $t | tee -a wynikzl$n_$e.txt
done 
 
echo czas: $(date) 
echo "# wszystko zrobione " > zl_todo$n_$e.sh