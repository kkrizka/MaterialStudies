#!/usr/bin/env python

# %%
import sys
import argparse
import ROOT

from math import *

from kkconfig import runconfig

from MaterialStudies import config
from MaterialStudies import style

# %% Prepare configuration
if 'ipykernel' in sys.modules: # running in a notebook
    # %load_ext autoreload
    # %autoreload 2
    runcfgpaths=['runconfigs/id.yaml']
else:
    if len(sys.argv)<2:
        print('usage: {} runconfig.yaml [runconfig.yaml]'.format(sys.argv[0]))
        sys.exit(1)
    runcfgpaths=sys.argv[1:]

runcfg = runconfig.load(runcfgpaths)

# %% Useful functions
def get_df(subdet):
    df=ROOT.RDataFrame("material-tracks",subdet)

    df=df.Define('v_pt','sqrt(v_px*v_px+v_py*v_py)')
    df=df.Define('v_p','sqrt(v_px*v_px+v_py*v_py+v_pz*v_pz)')
    df=df.Define('v_theta', 'acos(v_pz/v_p)')
    df=df.Define('v_theta_deg', 'v_theta*180/M_PI')

    return df

# %% Prepare the histograms
hs_x0=ROOT.THStack('hs_x0','MuColl_v1')
hs_l0=ROOT.THStack('hs_l0','MuColl_v1')

l_x0=ROOT.TLegend(0.2,0.5,0.85,0.8)
l_l0=ROOT.TLegend(0.2,0.5,0.85,0.8)

l_x0.SetNColumns(2)
l_l0.SetNColumns(2)

store=[]
for input in runcfg['inputs']:
    df=get_df(f'{config.datapath}/{input["file"]}')

    hdef=('',input['title'],100,0,180)

    hx0=df.Histo1D(hdef, 'v_theta_deg','t_X0')
    hx0=hx0.GetValue()

    hl0=df.Histo1D(hdef, 'v_theta_deg','t_L0')
    hl0=hl0.GetValue()

    # Take the average
    hcnt=df.Histo1D(hdef, 'v_theta_deg')
    hcnt=hcnt.GetValue()

    hx0.Divide(hcnt)
    hl0.Divide(hcnt)

    # Style the histogram
    hx0.SetLineColor(ROOT.kBlack)
    hx0.SetFillColor(eval(input['color']))

    hl0.SetLineColor(ROOT.kBlack)
    hl0.SetFillColor(eval(input['color']))

    hs_x0.Add(hx0, 'hist')
    hs_l0.Add(hl0, 'hist')

    l_x0.AddEntry(hx0, input['title'], 'F')
    l_l0.AddEntry(hl0, input['title'], 'F')

    store.append(hx0)
    store.append(hl0)

# %% Draw X0 histogram
c_x0=ROOT.TCanvas('c_x0','')

hs_x0.Draw()

hs_x0.GetXaxis().SetTitle('#theta [#circ]')
hs_x0.GetYaxis().SetTitle('Radiation Length [X_{0}]')

hs_x0.SetMaximum(0.5)

l_x0.Draw()

logo_x0=style.logo(xpos=0.4,ypos=0.4)

c_x0.SaveAs(f'x0.{config.format}')

# %% Draw X0 histogram
c_l0=ROOT.TCanvas('c_l0','')

hs_l0.Draw()

hs_l0.GetXaxis().SetTitle('#theta [#circ]')
hs_l0.GetYaxis().SetTitle('Hadronic Interaction Length [L_{0}]')

hs_l0.SetMaximum(0.25)

l_l0.Draw()

logo_l0=style.logo(xpos=0.4,ypos=0.4)

c_l0.SaveAs(f'l0.{config.format}')

# %% Save all output to a ROOT file
fh=ROOT.TFile.Open('x0l0.root','RECREATE')

hs_x0.Write()
hs_l0.Write()

c_x0.Write()
c_l0.Write()

fh.Close()
