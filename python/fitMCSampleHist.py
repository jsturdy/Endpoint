#!/bin/py

import ROOT
from ROOT import *

if __name__ == '__main__':
	
	infile = TFile("root/pullBaseHist1.root")


	can = TCanvas("can","can",600,600)

	htrue.Draw("hist")
	
	h= htrue.Clone("porkchop")


	h.Draw("pe")
#	can.SetLogy(1)

#	fit = TF1("fit","TMath::Exp([0]-[1]*x)")
#	fit.SetParameters(-7.3,360)

#	fit = TF1("fit","TMath::Exp([0]+[1]*x)*TMath::Power(1+x,[3])")

#	fit = TF1("fit","TMath::Exp([0]+[1]*x)")
#	fit.SetParameters(7.3,360)

#	fit = TF1("fit","TMath::Exp([0]+[1]*x+[2]*x*x+[3]*x*x*x)*[4]+[5]*x+[6]*x*x")
#	fit.SetParameters(-1.3,-100,-2000,-5000)
#	fit = TF1("fit","TMath::Exp([0]+[1]*x-[2]*x*x)")
#	fit.SetParameters(-1.3,-100)

	f1 = TF1("f1","pol5",-1./40,-1./50)
	f2 = TF1("f2","pol3",-1./49,-1./101)
	f3 = TF1("f3","pol3",-1./99,-1./1000)

	fit = TF1("fit","pol5(0)+pol3(6)",-1./40,-1./100)

	f1.SetLineWidth(3)
	f2.SetLineWidth(3)
	f2.SetLineColor(kBlue)
#	fit.SetLineWidth(3)
#	fit.SetRange(-1./45,-1./1500)

	h.Scale(100000)

	h.Fit("f1","rb")
	h.Fit("f2","rb+")
	h.Fit("f3","rb+")

#	for ipar in range(0,12):
#		if ipar <5:val = f1.GetParameter(ipar)
#		elif ipar < 12: val = f2.GetParameter(ipar)
#		print ipar,val
#		fit.SetParameter(ipar,val)

#	h.Fit("fit","rb")
#	h.Fit("fit","rb")
#	fit.Draw("same")
	can.Update()

'''
	outfile = TFile("root/fitMCShape1.root","recreate")
	fit.Write("mcshape")
	fit.SetRange(-1./43,1./43)
	fit1 = TF1("fit1","13*TMath::Exp(([0]+[1]*x+[2]*x*x))")
	fit1.SetParameters(-1*fit.GetParameter(0),fit.GetParameter(1),-1*fit.GetParameter(2))
	fit.Draw()
	fit1.SetLineWidth(3)
	fit1.SetLineColor(kBlue)
	fit1.Draw("same")
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
'''
