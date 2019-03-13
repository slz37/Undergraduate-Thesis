#!/bin/bash

#Reads the output of a GEANT4 simulation from the command ./PICO250 cm244.mac > out.txt

#Directory + filename
filename="$PWD/$1"

#Read each line and store event #, pos, energy
#---> Begin of event: 1
#
#     Primary Energy: 903.379 keV

#Create data file

while read -r line
do
  #Beginning of each event
  if [[ "$line" = *'Begin of event: '* ]]
  then
    #First cut on : then on space
    eventNum=`echo $line | cut -d":" -f 2`
    eventNum=`echo $eventNum | cut -d" " -f 2`  
  fi  
  
  if [[ "$line" = *'Primary Energy: '* ]]
  then
    #Cut on : then on space
    energyCut=`echo $line | cut -d":" -f 2`
    energy=`echo $energyCut | cut -d" " -f 1`
    unit=`echo $energyCut | cut -d" " -f 2`

    #Convert to MeV if necessary
    if [ "$unit" == "keV" ]
    then
      energy=`echo "$energy / 1000" | bc -l`
    fi
  fi

  #Add to data file
  if [ "$eventNum" != "" ] && [ "$energy" != "" ]
  then
    echo "$eventNum,$energy" >> initial_data.txt
  
    #Reset variables
    eventNum=""
    energy=""
  fi
done < $filename
