#!/bin/bash

#Set geant and cadmesh source or set in .bashrc
#source /home/salvatore/Documents/pico_simulations/geant4.10.03.p03/bin/geant4.sh
#export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/home/salvatore/Documents/pico_simulations/CADMesh/lib

#Get date and time to append to output filenames if necessary
today=`/bin/date '+%Y_%m_%d__%H_%M_%S'`;

#Get rid of old make files
make clean

#Read variable values from arguments
guiType=$1
runScript=$2
particleScript=$3
moveOutput=$4

#Choose between either pico or guns
if [ "$guiType" == "pico" ]
then
  cmake -DPICO250ENV_GPS_USE=OFF -DGeant4_DIR=/home/salvatore/Documents/pico_simulations/geant4.10.03.p03/share/Geant4-10.3.3 /home/salvatore/Documents/pico_simulations/pico-svn/DBC-from-40
elif [ "$guiType" == "gun" ]
then
  cmake -DPICO250ENV_GPS_USE=ON -DGeant4_DIR=/home/salvatore/Documents/pico_simulations/geant4.10.03.p03/share/Geant4-10.3.3 /home/salvatore/Documents/pico_simulations/pico-svn/DBC-from-40
else
  echo "Need 1st parameter to be either pico or gun"
  exit 1
fi


#Make with all 4 processors
make -j 4

#Execute scripts based on pico or gun chosen, also choose between console or gui
if [ "$guiType" == "pico" ] && [ "$runScript" == "novis" ]
then
  #Run neutron script
  if [ "$particleScript" == "neutron" ]
  then
    #Move root and out file to avoid overwriting/appending
    if [ "$moveOutput" == "move" ]
    then
        #Make archive directory if necessary
        mkdir -p "Archives"

        #Move files
        mv neutron.root "Archives/neutron_$today.root"
        mv neutron_C3F8.out "Archives/neutron_C3F8_$today.out"
    fi
    
    time ./PICO250 neutron.mac --takeyourtime
  #Run gamma script
  elif [ "$particleScript" == "gamma" ]
  then
    #Move root and out file to avoid overwriting/appending
    if [ "$moveOutput" == "move" ]
    then
        #Make archive directory if necessary
        mkdir -p "Archives"

      mv gamma.root "Archives/gamma_$today.root"
      mv gamma_C3F8.out "Archives/gamma_C3F8_$today.out"
    fi

    time ./PICO250 gamma.mac --takeyourtime
  fi
#Use gps
elif [ "$guiType" == "gun" ] && [ "$runScript" == "novis" ]
then
  #Run neutron script
  if [ "$particleScript" == "neutron" ]
  then
    #Move root and out file to avoid overwriting/appending
    if [ "$moveOutput" == "move" ]
    then
        #Make archive directory if necessary
        mkdir -p "Archives"

        #Move files
        mv neutron.root "Archives/neutron_$today.root"
        mv neutron_C3F8.out "Archives/neutron_C3F8_$today.out"
    fi
    
    time ./PICO250 neutron_gps.mac --takeyourtime
  #Run gamma script
  elif [ "$particleScript" == "gamma" ]
  then
    #Move root and out file to avoid overwriting/appending
    if [ "$moveOutput" == "move" ]
    then
        #Make archive directory if necessary
        mkdir -p "Archives"

      mv gamma.root "Archives/gamma_$today.root"
      mv gamma_C3F8.out "Archives/gamma_C3F8_$today.out"
    fi

    time ./PICO250 gamma_gps.mac --takeyourtime
  fi
elif [ "$guiType" == "pico" ] && [ "$runScript" == "norun" ]
then
  :
else
  ./PICO250
fi

echo "Script finished with no errors."
