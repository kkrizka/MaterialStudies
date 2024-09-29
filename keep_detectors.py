#!/usr/bin/env python

import re
import shutil
import pathlib
import os
import argparse

import xml.etree.ElementTree as ET 

import sys
from kkconfig import runconfig


def select_detectors(inpath : pathlib.Path, detectors):
    """
    Modify a DD4hep definition to contain only the specified
    detectors.

    Parameters
    ----------
    inpath : pathlib.Path
      Path to the detector XML definition.
    detectors : list
      Name of the detector to keep.
    """
    re_envvar=re.compile('\$\{[a-zA-Z0-9_]+\}')

    tree = ET.parse(inpath)

    # Remove all unwanted detectors
    for alldetectors in tree.findall('detectors'):
        for detector in alldetectors.findall('detector'):
            if detector.attrib['name'] not in det:
                alldetectors.remove(detector)

    for plugins in tree.findall('plugins'):
        tree.getroot().remove(plugins)
    
    tree.write(inpath, encoding="utf-8")

def load_detector(inpath: pathlib.Path):
    """
    Read DD4hep definitions and build a dictionary listing
    detectors in each XML file.

    Parameters
    ----------
    inpath : pathlib.Path
      Path to the detector XML definition.

    Returns
    -------
    dict
      key: name of XML file, value: set of detector names in the XML file
    """
    re_envvar=re.compile('\$\{[a-zA-Z0-9_]+\}')

    indir = inpath.parent
    tree  = ET.parse(inpath)

    # Get list of current detectors
    mydetectors = set()
    for detectors in tree.findall('detectors'):
        for detector in detectors.findall('detector'):
            mydetectors.add(detector.attrib['name'])
    detmap={inpath.name: mydetectors}

    # Process includes
    for i in tree.findall('include'):
        refpath=i.attrib['ref']

        # Skip global files (contain env variable)
        if re_envvar.search(refpath)!=None:
            continue

        # Paths are relative
        refpath=indir / refpath

        detmap.update(load_detector(refpath))

    return detmap

#
# Check if default detector can be found
MUCOLL_GEO=os.environ.get('MUCOLL_GEO','/opt/ilcsoft/muonc/detector-simulation/geometries/MuColl_v1/MuColl_v1.xml')

#
# Configuration
parser = argparse.ArgumentParser('Remove a subdetector from a DD4hep definition.')
parser.add_argument('runconfig',nargs='+',help='Runconfigs with steering options.')
parser.add_argument('-i','--input',default=MUCOLL_GEO,help='Input DD4hep detector definition.')
parser.add_argument('-o','--outdir',default='./',help='Directory where to store DD4hep detector definitions.')

args = parser.parse_args()

runcfg = runconfig.load(args.runconfig)

#
# Setup input detector
inpath=pathlib.Path(args.input)
outpath=pathlib.Path(args.outdir)

if not outpath.exists():
    outpath.mkdir()

# parse
detmap = load_detector(inpath)

#
# Print available detectors for manual checks
print('-- Found the following detectors --')
for det in detmap:
    print(f'\t{det}')

#
# Loop over selected groups and make new outputs
for group,detectors in runcfg.get('groups',{}).items():
    print(f'-- Creating group {group} --')

    myoutpath = outpath / (inpath.parent.name + '_' + group)

    # Copy the original detector description
    if myoutpath.is_dir():
        shutil.rmtree(myoutpath)
    shutil.copytree(inpath.parent, myoutpath)

    # Get list of detectors
    if detectors is None:
        detectors=[group]
    detectors=set(detectors)

    mydetmap={}
    for k in detmap:
        mydetmap[k] = detmap[k] & detectors

    # Update the dd4hep description
    for k,v in mydetmap.items():
        select_detectors(myoutpath / k, v)
