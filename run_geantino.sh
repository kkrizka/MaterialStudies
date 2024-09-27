#!/bin/bash

DATADIR=/data/geant4

OPTSTRING="d:"
while getopts "${OPTSTRING}" opt; do
    case ${opt} in
	d)
	    DATADIR=${OPTARG}
	    ;;
    esac
done

echo "DATADIR = ${DATADIR}"

DETECTORS=(VertexBarrel VertexEndcap VertexVerticalCable InnerTrackerBarrel InnerTrackerEndcap InnerTrackerBarrelSupport InnerTrackerEndcapSupport Interlinks Beampipe OuterTrackerBarrel OuterTrackerEndcap OuterTrackerBarrelSupport OuterTrackerEndcapSupport)

for DET in ${DETECTORS[@]}
do
    ./material_recording.py --input MuColl_v1_${DET}/MuColl_v1.xml --output ./geant4_material_tracks-${DET}.root
done
