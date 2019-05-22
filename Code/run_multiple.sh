#!/bin/bash

#Run n simulations
for i in {1..100}
do
  seedOne=`echo $((1 + RANDOM % 100))`
  seedTwo=`echo $((1 + RANDOM % 100))`
  
  #Get line to replace
  line=`grep "/random/setSeeds" neutron.mac`


  #Now replace with new seeds
  sed -i "s|$line|/random/setSeeds $seedOne $seedTwo|g" neutron.mac

  #Save seeds for later use
  echo $seedOne $seedTwo >> neutron_seeds.txt

  #Run now
  ./compile.sh nomake piconovis neutron move "25x_$i"
done

#Run 100 simulations
#for i in {1..100}
#do
  #Randomly select seeds
#  seedOne=`echo $((1 + RANDOM % 100))`
#  seedTwo=`echo $((1 + RANDOM % 100))`
  
  #Get line to replace
#  line=`grep "/random/setSeeds" gamma.mac`


  #Now replace with new seeds
#  sed -i "s|$line|/random/setSeeds $seedOne $seedTwo|g" gamma.mac

  #Save seeds for later use
#  echo $seedOne $seedTwo >> gamma_seeds.txt

  #Run now
#  ./compile.sh nomake piconovis gamma move "201mm_$i"
#done
