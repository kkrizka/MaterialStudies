#!/usr/bin/env python

import re
import shutil
import pathlib
import os
import argparse

import xml.etree.ElementTree as ET 

import sys

def select_detector(inpath,det):
    """
    Modify a DD4hep definition to contain only the specified
    detector.

    Removal is done recursively by transversing through all
    include tags.

    Parameters
    ----------
    inpath : str
      Path to the detector XML definition.
    det : str
      Name of the detector to keep.
    """
    re_envvar=re.compile('\$\{[a-zA-Z0-9_]+\}')

    indir =os.path.dirname(inpath)
    tree = ET.parse(inpath)

    # Process includes
    for i in tree.findall('include'):
        refpath=i.attrib['ref']

        # Skip global files (contain env variable)
        if re_envvar.search(refpath)!=None:
            continue

        # Paths are relative
        refpath=indir+'/'+refpath

        select_detector(refpath, det)

    # Remove all unwanted detectors
    for detectors in tree.findall('detectors'):
        for detector in detectors.findall('detector'):
            if detector.attrib['name']!=det:
                detectors.remove(detector)

    for plugins in tree.findall('plugins'):
        tree.getroot().remove(plugins)
    
    tree.write(inpath, encoding="utf-8")

#
# Configuration
parser = argparse.ArgumentParser('Remove a subdetector from a DD4hep definition.')
parser.add_argument('subdetector',help='Detector name to remove')
parser.add_argument('-i','--input',default='/opt/ilcsoft/muonc/detector-simulation/geometries/MuColl_v1',help='Input DD4hep detector definition.')
parser.add_argument('-o','--output',default='MuColl_v1_output',help='Output DD4hep detector definition.')

args = parser.parse_args()

#
# Setup input/output
inpath=pathlib.Path(args.input)
outpath=pathlib.Path(args.output)

if outpath.is_dir():
    shutil.rmtree(outpath)
shutil.copytree(inpath, outpath)

# parse
select_detector(outpath/'MuColl_v1.xml', args.subdetector)
