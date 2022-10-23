#!/bin/bash

DATADIR=/data/geant4

DETECTORS=(VertexBarrel VertexEndcap VertexVerticalCable InnerTrackerBarrel InnerTrackerEndcap InnerTrackerBarrelSupport InnerTrackerEndcapSupport InnerTrackerInterlink InnerTrackerVertexCable BeampipeShell BeampipeShell2 BeampipeShell3 OuterTrackerBarrel OuterTrackerEndcap OuterTrackerBarrelSupport OuterTrackerEndcapSupport)

for DET in ${DETECTORS[@]}
do
    ./build/bin/ActsExampleMaterialRecordingDD4hep --dd4hep-input MuColl_v1_${DET}/MuColl_v1.xml  -n 100000 -j1 --output-root 1
    mv geant4_material_tracks.root ${DATADIR}/geant4_material_tracks-${DET}.root
done
