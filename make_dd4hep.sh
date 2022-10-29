#!/bin/bash

# Indiviual subdetectors
DETECTORS=(VertexBarrel VertexEndcap VertexVerticalCable InnerTrackerBarrel InnerTrackerEndcap InnerTrackerBarrelSupport InnerTrackerEndcapSupport InnerTrackerInterlink InnerTrackerVertexCable OuterTrackerBarrel OuterTrackerEndcap OuterTrackerBarrelSupport OuterTrackerEndcapSupport)

for DET in ${DETECTORS[@]}
do
    python keep_detector.py ${DET} -o MuColl_v1_${DET}
done

# Beampipe
python keep_detector.py BeampipeShell BeampipeShell2 BeampipeShell3  -o MuColl_v1_Beampipe
