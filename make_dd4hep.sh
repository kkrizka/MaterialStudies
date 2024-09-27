#!/bin/bash

GEO=${MUCOLL_GEO}

# Steering options
OPTSTRING="i:"
while getopts "${OPTSTRING}" opt; do
    case ${opt} in
        i)
            GEO=$(realpath ${OPTARG})
            ;;
    esac
done

GEODIR=$(dirname ${GEO})
GEONAME=$(basename ${GEODIR})
GEOFILE=$(basename ${GEO})

if [ "${GEONAME}.xml" != "${GEOFILE}" ]; then
    echo "Expecting geometry to be located in GEONAME/GEONAME.xml"
    exit 1
fi

# Indiviual subdetectors
DETECTORS=(VertexBarrel VertexEndcap InnerTrackerBarrel InnerTrackerEndcap InnerTrackerBarrelSupport InnerTrackerEndcapSupport OuterTrackerBarrel OuterTrackerEndcap OuterTrackerBarrelSupport OuterTrackerEndcapSupport)

for DET in ${DETECTORS[@]}
do
    python keep_detector.py ${DET} -i ${GEO} -o ${GEONAME}_${DET}
done

# Subdetectors
Interlink="InnerTrackerVertexCable VertexVerticalCable"
Beampipe="BeampipeInner BeampipeOuter BeampipeShell BeampipeShell2 BeampipeShell3"
Nozzle="NozzleW_right NozzleW_left NozzleBCH_right NozzleBCH_left"
Tracker="Vertex VertexBarrel VertexEndcap VertexVerticalCable InnerTrackers InnerTrackerBarrel InnerTrackerEndcap InnerTrackerBarrelSupport InnerTrackerEndcapSupport InnerTrackerInterlink InnerTrackerVertexCable OuterTrackers OuterTrackerBarrel OuterTrackerEndcap OuterTrackerBarrelSupport OuterTrackerEndcapSupport"
ECal="ECalBarrel ECalEndcap"
HCal="HCalBarrel HCalEndcaps HCalEndcap HCalRing"
Solenoid="Solenoid SolenoidBarrel SolenoidEndcaps"
Yoke="YokeBarrel YokeEndcap"

SUBDETECTORS=(Interlink Beampipe Nozzle Tracker ECal HCal Solenoid Yoke)
for SUBDETECTOR in ${SUBDETECTORS[@]}; do
    python keep_detector.py ${!SUBDETECTOR} -i ${GEO} -o ${GEONAME}_${SUBDETECTOR}
done
