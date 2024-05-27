#!/bin/bash

# Building podman for the different algorithms 
echo "This may take a while..."

BASEDIR=$(pwd)

# You may remove the -q flag if you want to see the podman build status
cd $BASEDIR/Algorithms/ARBORETO
podman build -q -t arboreto:base .
if [[ "$(podman images -q arboreto:base 2> /dev/null)" != "" ]]; then
    echo "podman container for ARBORETO is built and tagged as arboreto:base"
else
    echo "Oops! Unable to build podman container for ARBORETO"
fi

cd $BASEDIR/Algorithms/CCMNET
podman build -q -t ccmnet:base .
if [[ "$(podman images -q ccmnet:base 2> /dev/null)" != "" ]]; then
    echo "podman container for CCMNET is built and tagged as ccmnet:base"
else
    echo "Oops! Unable to build podman container for CCMNET"
fi


# cd $BASEDIR/Algorithms/GRISLI/
# podman build -q -t grisli:base .
# if [[ "$(podman images -q grisli:base 2> /dev/null)" != "" ]]; then
#     echo "podman container for GRISLI is built and tagged as grisli:base"
# else
#     echo "Oops! Unable to build podman container for GRISLI"
# fi


# cd $BASEDIR/Algorithms/GRNVBEM/
# podman build -q -t grnvbem:base .
# if ([[ "$(podman images -q grnvbem:base 2> /dev/null)" != "" ]]); then
#     echo "podman container for GRNVBEM is built and tagged as  grnvbem:base"
# else
#     echo "Oops! Unable to build podman container for GRNVBEM"
# fi


# cd $BASEDIR/Algorithms/JUMP3/
# podman build -q -t jump3:base .
# if ([[ "$(podman images -q jump3:base 2> /dev/null)" != "" ]]); then
#     echo "podman container for JUMP3 is built and tagged as  jump3:base"
# else
#     echo "Oops! Unable to build podman container for JUMP3"
# fi


# cd $BASEDIR/Algorithms/LEAP/
# podman build -q -t leap:base .
# if ([[ "$(podman images -q leap:base 2> /dev/null)" != "" ]]); then
#     echo "podman container for LEAP is built and tagged as  leap:base"
# else
#     echo "Oops! Unable to build podman container for LEAP"
# fi


# cd $BASEDIR/Algorithms/PIDC/
# podman build -q -t pidc:base .
# if ([[ "$(podman images -q pidc:base 2> /dev/null)" != "" ]]); then
#     echo "podman container for PIDC is built and tagged as pidc:base"
# else
#     echo "Oops! Unable to build podman container for PIDC"
# fi


# cd $BASEDIR/Algorithms/PNI/
# podman build -q -t pni:base .
# if ([[ "$(podman images -q pni:base 2> /dev/null)" != "" ]]); then
#     echo "podman container for PNI is built and tagged as pni:base"
# else
#     echo "Oops! Unable to build podman container for PNI"
# fi


# cd $BASEDIR/Algorithms/PPCOR/
# podman build -q -t ppcor:base .
# if ([[ "$(podman images -q ppcor:base 2> /dev/null)" != "" ]]); then
#     echo "podman container for PPCOR is built and tagged as ppcor:base"
# else
#     echo "Oops! Unable to build podman container for PPCOR"
# fi


# cd $BASEDIR/Algorithms/SINGE/
# podman build -q -t singe:base .
# if ([[ "$(podman images -q singe:base 2> /dev/null)" != "" ]]); then
#     echo "podman container for SINGE is built and tagged as singe:base"
# else
#     echo "Oops! Unable to build podman container for SINGE"
# fi


# cd $BASEDIR/Algorithms/SCNS/
# podman build -q -t scns:base .
# if ([[ "$(podman images -q scns:base 2> /dev/null)" != "" ]]); then
#     echo "podman container for SCNS is built and tagged as scns:base"
# else
#     echo "Oops! Unable to build podman container for SCNS"
# fi


# cd $BASEDIR/Algorithms/SCODE/
# podman build -q -t scode:base .
# if ([[ "$(podman images -q scode:base 2> /dev/null)" != "" ]]); then
#     echo "podman container for SCODE is built and tagged as scode:base"
# else
#     echo "Oops! Unable to build podman container for SCODE"
# fi


# cd $BASEDIR/Algorithms/SCRIBE/
# podman build -q -t scribe:base .
# if [[ "$(podman images -q scribe:base 2> /dev/null)" != "" ]]; then
#     echo "podman container for SCRIBE is built and tagged as scribe:base"
# else
#     echo "Oops! Unable to build podman container for SCRIBE"
# fi


# cd $BASEDIR/Algorithms/SINCERITIES/
# podman build -q -t sincerities:base .
# if ([[ "$(podman images -q sincerities:base 2> /dev/null)" != "" ]]); then
#     echo "podman container for SINCERITIES is built and tagged as sincerities:base"
# else
#     echo "Oops! Unable to build podman container for SINCERITIES"
# fi


# cd $BASEDIR/Algorithms/SCSGL/
# podman build -q -t scsgl:base .
# if ([[ "$(podman images -q scsgl:base 2> /dev/null)" != "" ]]); then
#     echo "podman container for SCSGL is built and tagged as scsgl:base"
# else
#     echo "Oops! Unable to build podman container for SCSGL"
# fi

# cd $BASEDIR
