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

# Beampipe
python keep_detector.py BeampipeShell BeampipeShell2 BeampipeShell3 -i ${GEO} -o ${GEONAME}_Beampipe
python keep_detector.py InnerTrackerInterlink InnerTrackerVertexCable VertexVerticalCable -i ${GEO} -o ${GEONAME}_Interlinks
