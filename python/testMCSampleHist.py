#!/bin/py

import ROOT
from ROOT import *

if __name__ == '__main__':
	
	can = TCanvas("can","can",600,600)
	infile = TFile("root/fitMCShape.root")

	hist = TH1F("hist",";q/p_{T} [c/GeV]",1000,-1./43,1./43)

	fmc = infile.mcshape
	for i in range(0,1000000):
		k = fmc.GetRandom()

		if gRandom.Rndm() < 0.5: k *= -1.
		

		hist.Fill(k)

	hist.Draw()
	can.Update()

'''
	infile = TFile("root/pullBaseHist.root")

	htrue.Draw("hist")
	
	h= htrue.Clone("porkchop")


	h.Draw("pe")
	can.SetLogy(1)

#	fit = TF1("fit","TMath::Exp([0]-[1]*x)")
#	fit.SetParameters(-7.3,360)

	fit = TF1("fit","TMath::Exp([0]-[1]*x+[2]*x*x)")
	fit.SetParameters(-7.3,360,0.1)
	fit.SetLineWidth(3)


	fit.SetRange(-1./43,-1./3000)
	h.Scale(100000)
	h.Fit("fit","rb")
'''

	
'''
#	hsample.GetXaxis().SetRangeUser(-1./40,1./40)
	hist = TH1F("hist",";q/p_{T} [c/GeV]",1000,-1./45,1./45)

#	hsample.GetXaxis().SetRangeUser(-1./40,1./40)
	for i in range(0,1000000):
		curv = hsample.GetRandom()
		hist.Fill(curv)


	hsample.Draw()
	hist.Draw()
	can.Update()
'''
