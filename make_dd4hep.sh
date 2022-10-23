#!/bin/bash

DETECTORS=(VertexBarrel VertexEndcap VertexVerticalCable InnerTrackerBarrel InnerTrackerEndcap InnerTrackerBarrelSupport InnerTrackerEndcapSupport InnerTrackerInterlink InnerTrackerVertexCable BeampipeShell BeampipeShell2 BeampipeShell3 OuterTrackerBarrel OuterTrackerEndcap OuterTrackerBarrelSupport OuterTrackerEndcapSupport)

for DET in ${DETECTORS[@]}
do
    python keep_detector.py ${DET} -o MuColl_v1_${DET}
done
