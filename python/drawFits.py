#!/bin/py

import ROOT, commands, math
from ROOT import *

from python.ufPlotTools import *
setTDRStyle()

tex = TLatex()
tex.SetNDC()
tex.SetTextFont(42)


can = TCanvas("can","can",600,600)

sname = "qcd_dataB_dec22_notwist"
sname = "qcd_dataB_dec22"
sname = "qcd_dataB_nov04"
sname = "zmumu_mc_414"
sname = "massptplots_nov04_cuts"


infile0 = TFile("out/%s.root"%sname,"open") # for testing


infile1 = TFile("out/massptplots_zmumu_v0.root"		,"open")
infile2 = TFile("out/massptplots_nov04_cuts.root"	,"open")
infile3 = TFile("out/massptplots_dec22_cuts.root"	,"open")
infile4 = TFile("out/massptplots_april29rereco.root","open")

outfile = TFile("out/fits/%s.root"%sname,"recreate")


sdir = "trkAll"

hzmassVsPhiPosDT = infile0.Get(sdir+"/hzmassVsPhiPos")
hzmassVsPhiPosDT.Draw("colz")

can.Update()

fitVoigt = TF1("fitVoigt", "[0]*TMath::Voigt(x-[1],[2],[3])")
fitVoigt.SetParNames("Norm","mass","#sigma","#Gamma")
fitVoigt.FixParameter(3,2.4952)

hists = []

def GetYProjections(hist2,soutname,stit = ""):
	nbins = hist2.GetNbinsX()
	print "number of x bins to project: %d"%nbins

	gre = TGraphErrors()
	gre.SetName("%s"%soutname)
	gre.GetXaxis().SetTitle("#phi")
	gre.GetYaxis().SetTitle("mean invariant mass")
	

	for ibin in range(1,nbins+1):
		hist = hist2.ProjectionY("%s%d"%(soutname,ibin),ibin,ibin)
		hist.Sumw2()
		fitVoigt.SetParameter(0,hist.GetMaximum())
		fitVoigt.SetParameter(1,hist.GetMean())
		fitVoigt.SetParameter(2,hist.GetRMS())
		fitVoigt.SetRange(80,100)
		hist.Fit("fitVoigt","qr")
		hist.Fit("fitVoigt","qr")
		print "%d\t%f\t%f\t%f"%(ibin,hist2.GetXaxis().GetBinCenter(ibin),fitVoigt.GetParameter(1),fitVoigt.GetParError(1))
		
		gre.SetPoint(ibin-1,hist2.GetXaxis().GetBinCenter(ibin), fitVoigt.GetParameter(1))
		gre.SetPointError(ibin-1,0,fitVoigt.GetParError(1))
	
		hists.append(hist)
#	gre.SetTitle("%s;#phi;mean M_{#mu#mu} [GeV/c^{2}]"%(stit))
	gre.SetTitle("%s"%(stit))
	outfile.cd()
	gre.Write(gre.GetName())	
	gre.SetMinimum(88)
	gre.SetMaximum(93.5)
	gre.Draw("ape")
	can.Update()
#	can.SaveAs("png/april21/weakmode/%s_%s.png"%(sname,gre.GetName()))
	return gre	



def drawDataSet(stitDataset,infile,soutname):

	sdir = "trkAll"
	stit= stitDataset+" All Detector"


	grePos		= GetYProjections(infile.Get(sdir+"/hzmassVsPhiNeg") 	,soutname+"posProj"	, stit+";#phi^{+}(#mu_{lead});mean M_{#mu#mu} [GeV/c^{2}]"	)
	greNeg		= GetYProjections(infile.Get(sdir+"/hzmassVsPhiNeg") 	,soutname+"negProj"	, stit+";#phi^{-}(#mu_{lead});mean M_{#mu#mu} [GeV/c^{2}]"	)
	grePos.Draw("ape")
	tex.DrawLatex(0.15,0.03, "tracker fit")
	can.SaveAs("png/drawFits/%s/%sposProj.png"%(sdir,soutname))
	greNeg.Draw("ape")
	tex.DrawLatex(0.15,0.03, "tracker fit")
	can.SaveAs("png/drawFits/%s/%snegProj.png"%(sdir,soutname))

	sdir = "trkDTDT"
	stit= stitDataset+" DT-DT"
	grePos		= GetYProjections(infile.Get(sdir+"/hzmassVsPhiNeg") 	,soutname+"posProj"	, stit+";#phi^{+}(#mu_{lead});mean M_{#mu#mu} [GeV/c^{2}]"	)
	greNeg		= GetYProjections(infile.Get(sdir+"/hzmassVsPhiNeg") 	,soutname+"negProj"	, stit+";#phi^{-}(#mu_{lead});mean M_{#mu#mu} [GeV/c^{2}]"	)
	grePos.Draw("ape")
	tex.DrawLatex(0.15,0.03, "tracker fit")
	can.SaveAs("png/drawFits/%s/%sposProj.png"%(sdir,soutname))
	greNeg.Draw("ape")
	tex.DrawLatex(0.15,0.03, "tracker fit")
	can.SaveAs("png/drawFits/%s/%snegProj.png"%(sdir,soutname))

#
	sdir = "trkDTCSCpos"
	stit= stitDataset+" DT_{lead}-CSC(#eta>0)"
	grePos		= GetYProjections(infile.Get(sdir+"/hzmassVsPhiNeg") 	,soutname+"posProj"	, stit+";#phi^{+}(#mu_{lead});mean M_{#mu#mu} [GeV/c^{2}]"	)
	greNeg		= GetYProjections(infile.Get(sdir+"/hzmassVsPhiNeg") 	,soutname+"negProj"	, stit+";#phi^{-}(#mu_{lead});mean M_{#mu#mu} [GeV/c^{2}]"	)
	grePos.Draw("ape")
	tex.DrawLatex(0.15,0.03, "tracker fit")
	can.SaveAs("png/drawFits/%s/%sposProj.png"%(sdir,soutname))
	greNeg.Draw("ape")
	tex.DrawLatex(0.15,0.03, "tracker fit")
	can.SaveAs("png/drawFits/%s/%snegProj.png"%(sdir,soutname))

#
	sdir = "trkDTCSCneg"
	stit= stitDataset+" DT_{lead}-CSC(#eta<0)"
	grePos		= GetYProjections(infile.Get(sdir+"/hzmassVsPhiNeg") 	,soutname+"posProj"	, stit+";#phi^{+}(#mu_{lead});mean M_{#mu#mu} [GeV/c^{2}]"	)
	greNeg		= GetYProjections(infile.Get(sdir+"/hzmassVsPhiNeg") 	,soutname+"negProj"	, stit+";#phi^{-}(#mu_{lead});mean M_{#mu#mu} [GeV/c^{2}]"	)
	grePos.Draw("ape")
	tex.DrawLatex(0.15,0.03, "tracker fit")
	can.SaveAs("png/drawFits/%s/%sposProj.png"%(sdir,soutname))
	greNeg.Draw("ape")
	tex.DrawLatex(0.15,0.03, "tracker fit")
	can.SaveAs("png/drawFits/%s/%snegProj.png"%(sdir,soutname))

#

	sdir = "tupAll"
	stit= stitDataset+" All Detector"

	grePos		= GetYProjections(infile.Get(sdir+"/hzmassVsPhiNeg") 	,soutname+"posProj"	, stit+";#phi^{+}(#mu_{lead});mean M_{#mu#mu} [GeV/c^{2}]"	)
	greNeg		= GetYProjections(infile.Get(sdir+"/hzmassVsPhiNeg") 	,soutname+"negProj"	, stit+";#phi^{-}(#mu_{lead});mean M_{#mu#mu} [GeV/c^{2}]"	)
	grePos.Draw("ape")
	tex.DrawLatex(0.15,0.03, "cocktail fit")
	can.SaveAs("png/drawFits/%s/%sposProj.png"%(sdir,soutname))
	greNeg.Draw("ape")
	tex.DrawLatex(0.15,0.03, "cocktail fit")
	can.SaveAs("png/drawFits/%s/%snegProj.png"%(sdir,soutname))

	sdir = "tupDTDT"
	stit= stitDataset+" DT-DT"
	grePos		= GetYProjections(infile.Get(sdir+"/hzmassVsPhiNeg") 	,soutname+"posProj"	, stit+";#phi^{+}(#mu_{lead});mean M_{#mu#mu} [GeV/c^{2}]"	)
	greNeg		= GetYProjections(infile.Get(sdir+"/hzmassVsPhiNeg") 	,soutname+"negProj"	, stit+";#phi^{-}(#mu_{lead});mean M_{#mu#mu} [GeV/c^{2}]"	)
	grePos.Draw("ape")
	tex.DrawLatex(0.15,0.03, "cocktail fit")
	can.SaveAs("png/drawFits/%s/%sposProj.png"%(sdir,soutname))
	greNeg.Draw("ape")
	tex.DrawLatex(0.15,0.03, "cocktail fit")
	can.SaveAs("png/drawFits/%s/%snegProj.png"%(sdir,soutname))


	sdir = "tupDTCSCpos"
	stit= stitDataset+" DT_{lead}-CSC(#eta>0)"
	grePos		= GetYProjections(infile.Get(sdir+"/hzmassVsPhiNeg") 	,soutname+"posProj"	, stit+";#phi^{+}(#mu_{lead});mean M_{#mu#mu} [GeV/c^{2}]"	)
	greNeg		= GetYProjections(infile.Get(sdir+"/hzmassVsPhiNeg") 	,soutname+"negProj"	, stit+";#phi^{-}(#mu_{lead});mean M_{#mu#mu} [GeV/c^{2}]"	)
	grePos.Draw("ape")
	tex.DrawLatex(0.15,0.03, "cocktail fit")
	can.SaveAs("png/drawFits/%s/%sposProj.png"%(sdir,soutname))
	greNeg.Draw("ape")
	tex.DrawLatex(0.15,0.03, "cocktail fit")
	can.SaveAs("png/drawFits/%s/%snegProj.png"%(sdir,soutname))


	sdir = "tupDTCSCneg"
	stit= stitDataset+" DT_{lead}-CSC(#eta<0)"
	grePos		= GetYProjections(infile.Get(sdir+"/hzmassVsPhiNeg") 	,soutname+"posProj"	, stit+";#phi^{+}(#mu_{lead});mean M_{#mu#mu} [GeV/c^{2}]"	)
	greNeg		= GetYProjections(infile.Get(sdir+"/hzmassVsPhiNeg") 	,soutname+"negProj"	, stit+";#phi^{-}(#mu_{lead});mean M_{#mu#mu} [GeV/c^{2}]"	)
	grePos.Draw("ape")
	tex.DrawLatex(0.15,0.03, "cocktail fit")
	can.SaveAs("png/drawFits/%s/%sposProj.png"%(sdir,soutname))
	greNeg.Draw("ape")
	tex.DrawLatex(0.15,0.03, "cocktail fit")
	can.SaveAs("png/drawFits/%s/%snegProj.png"%(sdir,soutname))



	can.Update()
	
drawDataSet("POWHEG ", infile1, "powheg_")
drawDataSet("Nov 04 reprocessing", infile2, "nov04_")
drawDataSet("Dec 22 reprocessing", infile3, "dec22_")
drawDataSet("Apr 19 reprocessing", infile4, "apr19_")


outfile.Write()
can.Update()
