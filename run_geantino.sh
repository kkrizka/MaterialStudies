#!/bin/bash

NAME=MuColl_v1
INDIR=data
OUTDIR=/data/geant4

OPTSTRING="o:"
while getopts "${OPTSTRING}" opt; do
    case ${opt} in
	o)
	    OUTDIR=${OPTARG}
	    ;;
    esac
done

INDIR=${@:OPTIND:1}
NAME=${@:OPTIND+1:1}

echo "INDIR = ${INDIR}"
echo "OUTDIR = ${OUTDIR}"
if [ ! -e ${OUTDIR} ]; then
    mkdir -p ${OUTDIR}
fi

for i in ${INDIR}/${NAME}*
do
    # Check if this is 
    ./material_recording.py --input ${i}/${NAME}.xml --output ${OUTDIR}/geant4_material_tracks-$(basename ${i}).root --events 10000
done
