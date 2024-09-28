#!/bin/bash

DATADIR=/data/geant4
NAME=MuColl_v1

OPTSTRING="d:n:"
while getopts "${OPTSTRING}" opt; do
    case ${opt} in
	d)
	    DATADIR=${OPTARG}
	    ;;
	n)
	    NAME=${OPTARG}
	    ;;
    esac
done

echo "DATADIR = ${DATADIR}"
if [ ! -e ${DATADIR} ]; then
    mkdir ${DATADIR}
fi

DETECTORS=(VertexBarrel VertexEndcap InnerTrackerBarrel InnerTrackerEndcap InnerTrackerBarrelSupport InnerTrackerEndcapSupport OuterTrackerBarrel OuterTrackerEndcap OuterTrackerBarrelSupport OuterTrackerEndcapSupport Interlinks Beampipe Interlinks Beampipe Nozzle Tracker ECal HCal Solenoid Yoke)

for DET in ${DETECTORS[@]}
do
    ./material_recording.py --input ${NAME}_${DET}/${NAME}.xml --output ${DATADIR}/geant4_material_tracks-${DET}.root --events 1000
done
