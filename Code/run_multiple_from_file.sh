#!/bin/bash

#Run through all seeds in file
i=1

#Neutrons
while read -r line
do
  #Grab seeds from file  
  seedOne=`echo $line | cut -d' ' -f1`
  seedTwo=`echo $line | cut -d' ' -f2`
   
  #Get line to replace
  line=`grep "/random/setSeeds" neutron.mac`

  #Now replace with new seeds
  sed -i "s|$line|/random/setSeeds $seedOne $seedTwo|g" neutron.mac

  #Run now
  ./compile.sh nomake piconovis neutron move "18mm_$i"

  #Increment current iteration
  (( i++ ))
done < neutron_seeds_18mm.txt

#Reset count
i=1

#Gammas
while read -r line
do
  #Grab seeds from file  
  seedOne=`echo $line | cut -d' ' -f1`
  seedTwo=`echo $line | cut -d' ' -f2`
  
  #Get line to replace
  line=`grep "/random/setSeeds" gamma.mac`

  #Now replace with new seeds
  sed -i "s|$line|/random/setSeeds $seedOne $seedTwo|g" gamma.mac

  #Run now
  ./compile.sh nomake piconovis gamma move "18mm_$i"

  #Increment current iteration
  (( i++ ))
done < gamma_seeds_18mm.txt
