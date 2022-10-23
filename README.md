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
apptainer shell -B/my/big/disk:/data /cvmfs/unpacked.cern.ch/registry.hub.docker.com/infnpd/mucoll-ilc-framework\:1.6-centos8stream/
```

Then inside the container.
```shell
source /opt/ilcsoft/muonc/init_ilcsoft.sh
python -m venv .venv --system-site-packages
source .venv/bin/activate
cmake -Sacts -Bbuild -DACTS_BUILD_EXAMPLES_PYTHON_BINDINGS=ON -DACTS_BUILD_EXAMPLES_GEANT4=ON -DACTS_BUILD_EXAMPLES_DD4HEP=ON 
cmake --build build
pip install .
```

Then in any subsequent session, run the following inside your container.
```shell
source .venv/bin/activate
```

## Generating Inputs
The `make_dd4hep.sh` and `run_geantino.sh` implement the following two
subsections over the parts of the tracking detector.

### Selecting Subdetectors in DD4hep
A specific subdetector is selected by making a copy of the DD4hep geometry
description and removing all subdetectors that do not match a specific name.

```shell
keep_detector.py VertexBarrel -o MuColl_v1_VertexBarrel
```

### Running Geantino Scan
The ACTS `ActsExampleMaterialRecordingDD4hep` program is used to load the DD4hep
geometry and run the geantino scan. Note that this program only works with a
single thread.

```shell
./build/bin/ActsExampleMaterialRecordingDD4hep --dd4hep-input MuColl_v1_VertexBarrel/MuColl_v1.xml  -n 100000 -j1 --output-root 1
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