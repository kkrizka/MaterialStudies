# Muon Collider Detector Material Studies
Scripts for studying the material of the Muon Collider Detector.

All inputs and resulting plots are archived on CERN's EOS storage:
```
/eos/user/k/kkrizka/public/MuonCollider/MaterialStudies
```

## Installation
All of the scripts should be run from within the Muon Collider Detector software
image. It is required for loading of the detector geometry via DD4hep. It also
provides many of the other requirements (ROOT, DD4hep, GEANT4).

Start the container using Apptainer. The `/data` volume is used by the scripts
to store large output (ie: output of the Geantino scan).
```shell
apptainer shell -B/my/big/disk:/data /cvmfs/unpacked.cern.ch/gitlab-registry.cern.ch/muon-collider/mucoll-deploy/mucoll:2.9-alma9
```

Then inside the container.
```shell
source /opt/setup_mucoll.sh
python -m venv .venv --system-site-packages
source .venv/bin/activate
cmake -Sacts -Bbuild -DACTS_BUILD_EXAMPLES_PYTHON_BINDINGS=ON -DACTS_BUILD_EXAMPLES_GEANT4=ON -DACTS_BUILD_EXAMPLES_DD4HEP=ON
cmake --build build
pip install .
source build/python/setup.sh
```

Then in any subsequent session, run the following inside your container.
```shell
source /opt/setup_mucoll.sh
source .venv/bin/activate
source build/python/setup.sh
```

## Generating Inputs
The `make_dd4hep.sh` and `run_geantino.sh` implement the following two
subsections over the parts of the tracking detector.

An example of using the scripts is:

```shell
./make_dd4hep.sh -i lcgeo/MuColl/MuSIC_v1/MuSIC_v1.xml
./run_geantino.sh -d ./MuSIC_v1 -n MuSIC_v1
```

### Selecting Subdetectors in DD4hep
A specific subdetector is selected by making a copy of the DD4hep geometry
description and removing all subdetectors that do not match a specific name.

```shell
keep_detector.py VertexBarrel -o MuColl_v1_VertexBarrel
```

### Running Geantino Scan
A modified version of the ACTS `material_recording.py` example script is used to load the DD4hep geometry and run the geantino scan. Note that this program only works with a
single thread.

```shell
./material_recording.py --input MuColl_v1_VertexBarrel/MuColl_v1.xml --output ./geant4_material_tracks-VertexBarrel.root
```

## Making Plots

## Global Configuration
Global aspects of the plotting code can be configured using a configuration file
called `.config.yaml`. This is loaded automatically and overrides input values
inside the `MaterialStudies.config` module.

Configuration keys:
- `datapath`: path to geantino scan ROOT files
- `format`: image format to use for output plots (ie: `png`)

### Plotting Material Distribution
The inputs are specified using a run configuration and passed to
the `plotMaterial.py` script. The run configuration is a YAML file with a list
named `inputs`. Each element of the list is a dictionary with the following
keys:

- `title`: title to use in the legend
- `file`: input ROOT file path relative to `config.datapath`
- `color`: color to use for the fille (converted using `eval()`)

For example, to plot the tracker material:

```shell
plotMaterial.py runconfigs/id.yaml
```