#!/bin/bash

Zdock='/data/zusers/vangaves/BIN/zdock3.0.2_linux_mpi_compiled'
#receptor=$1
#ligand=$2
zdockout=$1
curr=`pwd`

#for i in 3 6 7 9
#do
#cd NMDA_AB_model${i}/dock
#Run zdock
#Regular
#$Zdock/zdock -R $receptor -L $ligand -o zdock.out -F
#MPI
#mpiexec -n 16 $Zdock/zdock  -R $receptor -L $ligand -o zdock.out -F

#Create prediction folder
$Zdock/create.pl $zdockout 10

cd $curr

