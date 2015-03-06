#!/bin/py

import ROOT, commands, math
from ROOT import *

from ufPlotTools import *
setTDRStyle()

from commonGoodies import *
def getChi2(hist1,hist2):

	hist1.Sumw2()
	hist2.Sumw2()
	hchi2 = hist1.Clone("hchi2")

	hchi2.Add(hist2,-1)

	hchi2.SetTitle(";"+hist1.GetXaxis().GetTitle()+";signed #chi^{2}/bin")
	hchi2.SetLineColor(kBlack)	
	hchi2.SetFillColor(856)	
	ts=hchi2.GetYaxis().GetTitleSize()	
	hchi2.GetYaxis().SetTitleSize(ts*2.)
	hchi2.GetYaxis().SetTitleOffset(0.4)
	
	nbinsx = hchi2.GetNbinsX()
	
	totalchi2 = 0	
	validndf = 0
	for ibin in range(1,nbinsx+1):
		v1 = hist1.GetBinContent(ibin)
		v2 = hist2.GetBinContent(ibin)
		v3 = hchi2.GetBinContent(ibin)
		e3 = hchi2.GetBinError(ibin)
		if e3 ==0 : e3=0.01
		val = v3*abs(v3)/(e3**2)
		hchi2.SetBinContent(ibin,val)

		if v1>20 and v2>20:
			totalchi2 += abs(val)
			validndf += 1
	hchi2.SetBinContent(0,totalchi2)
	hchi2.SetBinContent(nbinsx+1,validndf)

	hchi2.GetYaxis().CenterTitle(1)
	return hchi2
#infile1 = TFile("out/data_20100501.root","open")
#infile2 = TFile("out/dataPrompt2011v1.root","open")
#infile3 = TFile("out/april29rereco.root","open")
infile1 = TFile("out/doubleMu_may10_v1.root","open")
infile4 = TFile("out/zmumu.root","open")

can = TCanvas("can","can",600,600)
pad1 = TPad("pad1","pad1",0.02,0.30,0.98,0.98,0)
pad2 = TPad("pad2","pad2",0.02,0.02,0.98,0.32,0)
pad1.Draw()
pad2.Draw()
#
#
#

pad1.cd()
irebin = 25

hist1 = infile1.Get("tupAll/hzmass")
hist2 = infile4.Get("tupAll/hzmass")
hist1.Sumw2()
hist2.Sumw2()
hist1.SetLineWidth(3)

zbins = hist1.FindBin(60),hist1.FindBin(120-0.1)

rescale = hist1.Integral(*zbins) 

lumiest = rescale*3./1000.
rescale /= hist2.Integral(*zbins)
hist2.Scale(rescale)
hist2.SetFillColor(856)
hist2.SetLineColor(856)
print lumiest 

hist1.Rebin(irebin)
hist2.Rebin(irebin)

hist1.SetTitle("May 10, 2011 re-processing #sqrt{s} = 7 TeV")
hist1.GetXaxis().SetRangeUser(60,600)
hist2.GetXaxis().SetRangeUser(60,600)
hist1.SetYTitle("events / %2.1f GeV/c^{2}"%hist1.GetBinWidth(1))
hist1.Draw()
hist2.Draw("same,hist")
hist1.Draw("same")
hist1.Draw("AXIS same")

pad1.SetLogy(1)

#tex.DrawLatex(0.3,0.6, "#Ldt = %.0f pb^{-1}"%(lumiest))
tex.DrawLatex(0.3,0.8,"#int #font[12]{L} dt = %.1f pb^{-1}"%lumiest);
tex.DrawLatex(0.3,0.7,"NO JSON APPLIED");
tex.DrawLatex(0.3,0.6,"CMS Preliminary 2011");

leg.AddEntry(hist1,"data","lp")
leg.AddEntry(hist2,"POWHEG","f")
leg.Draw("same")
#
#
#
pad2.cd()
hres = hist1.Clone("hres")
hres.Add(hist2,-1)
for ibin in range(0,hres.GetNbinsX()+1):
	v = hres.GetBinContent(ibin)
	e = hres.GetBinError(ibin)

	if e != 0: v /= e
	hres.SetBinContent(ibin,v)
	hres.SetBinError(ibin,0)

hres.SetFillColor(856)
hres.SetLineColor(856)
hres.SetTitle("")

hres.Draw("hist")
hres.SetTitle(";;residual (Data-MC)")
hres.GetYaxis().CenterTitle(1)
hres.GetYaxis().SetTitleSize(0.1)
hres.GetYaxis().SetTitleOffset(0.3)
nbins = hist1.GetNbinsX()
#schi2ndf = float(hres.GetBinContent(0)),(hres.GetBinContent(nbins+1))
#stex = ("#chi^{2}/ndf = %.2f/%d"%(schi2ndf))
#tex.DrawLatex(0.20,0.20,stex)

can.Update()
can.SaveAs("dimuons_datamc.png")


#
#
#
#def drawDataMC(hdata,hmc):





'''
	iproj = 25-jproj
	projNeg = hist.ProjectionY("projNeg%d"%(iproj),iproj,iproj)
	projNeg.SetLineWidth(3)
	projNeg.SetLineColor(kRed)
	print hist.GetXaxis().GetBinLowEdge(iproj) 


	iproj = 26+jproj 
	print hist.GetXaxis().GetBinLowEdge(iproj+1) 
	projPos = hist.ProjectionY("projPos%d"%(iproj),iproj,iproj)
	projPos.SetLineWidth(3)
	projPos.SetLineColor(kBlue)
	projPos.SetLineStyle(2)

	skrange = "q/p_{T} #in [%.3f,%.3f]"%(hist.GetXaxis().GetBinLowEdge(iproj),hist.GetXaxis().GetBinLowEdge(iproj+1))
	print skrange

	stit = hist.GetTitle()
	stit=stit.split(",")[0]
	stit+=", "
	stit+=skrange
	projNeg.SetTitle(stit+";#eta;events / %.2f"%(projNeg.GetBinWidth(1)))
	height = max(projNeg.GetMaximum(),projPos.GetMaximum())*1.2


	projNeg.SetMaximum(height)
	projNeg.SetMinimum(0)
	pad1.Draw()
	pad2.Draw()
	pad1.cd()
	projNeg.GetXaxis().SetTitleSize(0.05)
#	projNeg.GetXaxis().CenterTitle()
	projNeg.Draw()
	projPos.Draw("same")

	hh = getChi2(projNeg,projPos)
	pad2.cd()
	hh.Draw("hist")
	can.Update()
	
	nbins = hh.GetNbinsX()
	schi2ndf = float(hh.GetBinContent(0)),(hh.GetBinContent(nbins+1))

	can.Update()
	tex.SetTextSize(0.20)
	stex = ("#chi^{2}/ndf = %.2f/%d"%(schi2ndf))
	tex.DrawLatex(0.20,0.20,stex)
	can.SaveAs("png/%s/posneg%02d.png"%(outdir,jproj))
	return hh
sdir = "trkAll/"
shist= "hzmass"
shist= "leadTCurvVsEtaOnZ"
#infile = infile1


hist1 = infile4.Get(sdir+shist) 
#hist2 = infile2.Get(sdir+shist) 
#hist1.Draw()


#hh = drawEtaCurvBinsChi2(hist1,10)
for i in range(0,25): 
	can.Clear()
	pad1 = TPad("pad1","pad1",0.02,0.30,0.98,0.98,0)
	pad2 = TPad("pad2","pad2",0.02,0.02,0.98,0.32,0)
	hh=drawEtaCurvBinsChi2(hist1,i)
#can.cd()
#hh.Draw("hist")

hist1 = infile1.Get("trkAll/hzmass") 
hist2 = infile2.Get("tupAll/hzmass") 

hh = getChi2((hist1),(hist2))
#hchi2.Draw()
#hist1.Draw()
#hist2.Draw("same")
hh.Draw()
'''


can.Update()

