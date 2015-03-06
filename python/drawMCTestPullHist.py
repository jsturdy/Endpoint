#!/bin/py

import ROOT
from ROOT import *

def fillHistCurv(tree,sbr,hist,mmax=3000,kmin=0.0001):
	

	br1 = tree.GetBranch(sbr+"1")
	br2 = tree.GetBranch(sbr+"2")
	lf1 = br1.GetLeaf("k")
	lf2 = br2.GetLeaf("k")
	
	htemp = hist.Clone("htemp")
	htemp.Reset()
	for jentry in tree:
		if tree.massRECO > mmax: continue
		k1 = lf1.GetValue()
		k2 = lf2.GetValue()

		if abs(k1)<kmin: continue
		if abs(k2)<kmin: continue
		htemp.Fill(-abs(k1)) 
		htemp.Fill(-abs(k2)) 
	
#	htemp.Scale(tree.weight)
	hist.Add(htemp,tree.weight)
#	hist.Add(htemp,1)

if __name__ == '__main__':
	
	infile	= TFile("root/compactMCTrees1.root","open")

	outfile = TFile("root/pullBaseHist1.root","recreate")

#	hist = TH1F("htrue",";q/p_{T} [c/GeV]",100,-1./20,1./20)
	hist = TH1F("htrue",";q/p_{T} [c/GeV]",100,-1./43,-1./3000)
	hist.Sumw2()
	histfsr = hist.Clone("hfsr")
#	histfsr = TH1F("hfsr",";q/p_{T} [c/GeV]",1000,-1,1)


#	fillHistCurv(infile.dy0020,"true",hist,200,0.026)	
	fillHistCurv(infile.dy0020,"true",hist,200)#,0.02)	
	fillHistCurv(infile.dy0120,"true",hist,500)	
	fillHistCurv(infile.dy0200,"true",hist,800)	
	fillHistCurv(infile.dy0500,"true",hist,1000)	
	fillHistCurv(infile.dy0800,"true",hist)	

#	fillHistCurv(infile.dy0020,"fsr",histfsr,0.026)	
#	fillHistCurv(infile.dy0020,"fsr",histfsr)	
#	fillHistCurv(infile.dy0120,"fsr",histfsr)	
#	fillHistCurv(infile.dy0200,"fsr",histfsr)	
#	fillHistCurv(infile.dy0500,"fsr",histfsr)	
#	fillHistCurv(infile.dy0800,"fsr",histfsr)	
	
	can = TCanvas("can","can",600,600)


	histfsr.Write()
	hist.Write()

	hist.Draw("pe")
	can.SetLogy(1)

	can.Update()

