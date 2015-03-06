#!/bin/py

import ROOT
from ROOT import *

sdir = "./root/"
sfilenames = ['dy0020','dy0120','dy0200','dy0500','dy0800']
infiles = []

for sfile in sfilenames:
	f = TFile("%s/cmssw/microMC_pt40_%s.root"%(sdir,sfile),"open")
	infiles.append(f)


#for tfile in infiles:
#	print tfile.dimuons.GetEntries()



outfile = TFile("root/compactMCTrees1.root","recreate")

hmass = TH1F("hmass","",3000-50,50,3000)
hmass.Sumw2()
hmassTemp = hmass.Clone("htemp")
import array
samplebins = [50,120,200,500,800,3000]
# put the sample bins into a full-blown array
bMassArray = array.array('d',samplebins)
hSampleBinsMass= TH1F("hSampleBinsMass","",len(bMassArray)-1,bMassArray)
hSampleBinsMass.Sumw2()
hSampleBinsTemp = hSampleBinsMass.Clone("htempFixedBins")


for tfile,sname in zip(infiles,sfilenames):
	print sname,tfile.dimuons.GetEntries()
	ttemp = tfile.dimuons.CloneTree()
	ttemp.SetName(sname)
	ttemp.SetTitle(sname)
	ttemp.Write(sname)
	ttemp.Project("htemp","massTrue")
	ttemp.Project("htempFixedBins","massTrue")
	hmass.Add(htemp,ttemp.weight)
	hSampleBinsMass.Add(hSampleBinsTemp,ttemp.weight)

#	hmass.Fill(ttemp.massTrue,ttemp.weight)


hmass.Write("hMassTrue")
hSampleBinsMass.Write("hMassTrueFixedBins")

