#!/usr/bin/env python3
import os
import warnings
from pathlib import Path
import argparse

import acts
from acts.examples import (
    GaussianVertexGenerator,
    ParametricParticleGenerator,
    FixedMultiplicityGenerator,
    EventGenerator,
    RandomNumbers,
)

import acts.examples.dd4hep
import acts.examples.geant4
import acts.examples.geant4.dd4hep

u = acts.UnitConstants

_material_recording_executed = False


def runMaterialRecording(
    detectorConstructionFactory,
    outputPath,
    tracksPerEvent=10000,
    s=None,
    etaRange=(-4, 4),
):
    global _material_recording_executed
    if _material_recording_executed:
        warnings.warn("Material recording already ran in this process. Expect crashes")
    _material_recording_executed = True

    rnd = RandomNumbers(seed=228)

    evGen = EventGenerator(
        level=acts.logging.INFO,
        generators=[
            EventGenerator.Generator(
                multiplicity=FixedMultiplicityGenerator(n=1),
                vertex=GaussianVertexGenerator(
                    stddev=acts.Vector4(0, 0, 0, 0),
                    mean=acts.Vector4(0, 0, 0, 0),
                ),
                particles=ParametricParticleGenerator(
                    pdg=acts.PdgParticle.eInvalid,
                    charge=0,
                    randomizeCharge=False,
                    mass=0,
                    p=(1 * u.GeV, 10 * u.GeV),
                    eta=etaRange,
                    numParticles=tracksPerEvent,
                    etaUniform=True,
                ),
            )
        ],
        outputParticles="particles_initial",
        randomNumbers=rnd,
    )

    s.addReader(evGen)

    g4Alg = acts.examples.geant4.Geant4MaterialRecording(
        level=acts.logging.INFO,
        detectorConstructionFactory=detectorConstructionFactory,
        randomNumbers=rnd,
        inputParticles=evGen.config.outputParticles,
        outputMaterialTracks="material_tracks",
    )

    s.addAlgorithm(g4Alg)

    s.addWriter(
        acts.examples.RootMaterialTrackWriter(
            prePostStep=True,
            recalculateTotals=True,
            collection="material_tracks",
            filePath=outputPath,
            level=acts.logging.INFO,
        )
    )

    return s


def main():
    p = argparse.ArgumentParser()
    p.add_argument(
        "-n", "--events", type=int, default=1000, help="Number of events to generate"
    )
    p.add_argument(
        "-t", "--tracks", type=int, default=100, help="Particle tracks per event"
    )
    p.add_argument(
        "-i", "--input", type=str, default=os.environ.get('MUCOLL_GEO',''), help="XML input file"
    )
    p.add_argument(
        "-o", "--output", type=str, default="geant4_material_tracks.root", help="ROOT output file"
    )

    args = p.parse_args()

    #
    # Create the detector from DD4hep
    dd4hepConfig = acts.examples.dd4hep.DD4hepGeometryService.Config(
        xmlFileNames=[args.input],
        logLevel=acts.logging.INFO,
        dd4hepLogLevel=acts.logging.INFO
    )
    dd4hepGeometryService = acts.examples.dd4hep.DD4hepGeometryService(dd4hepConfig)
    dd4hepDetector = acts.examples.dd4hep.DD4hepDetector(dd4hepGeometryService)

    detectorConstructionFactory = (
        acts.examples.geant4.dd4hep.DDG4DetectorConstructionFactory(dd4hepDetector)
    )

    #
    # Run the material map
    runMaterialRecording(
        detectorConstructionFactory=detectorConstructionFactory,
        tracksPerEvent=args.tracks,
        outputPath=args.output,
        s=acts.examples.Sequencer(events=args.events, numThreads=1),
    ).run()


if "__main__" == __name__:
    main()
