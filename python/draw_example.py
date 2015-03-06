#!/bin/py

import ROOT, commands, math
from ROOT import *

from python.ufPlotTools import *
setTDRStyle()

leg = TLegend()
leg.SetFillColor(0)
leg.SetTextAlign(12)
leg.SetTextSize(0.04)
leg.SetX1NDC(0.72)
leg.SetY1NDC(0.750)
leg.SetX2NDC(0.82)
leg.SetY2NDC(0.85)
leg.SetBorderSize(0)
leg.SetFillStyle(0)

_leftLegend = False

can = TCanvas("can","can",600,600)

infile1 = TFile("out/data_20100501.root","open")



def drawCurvaturePlot(infile,shname):
	hist2 = infile.Get(shname);
	hist2.Draw("lego2")	
	hist2.GetXaxis().SetTitleOffset(1.9)
	hist2.GetYaxis().SetTitleOffset(1.7)

	can.SaveAs("png/%s.png"%shname)	
	can.Update()


drawCurvaturePlot(infile1,"hkvsphiOnZ")
drawCurvaturePlot(infile1,"hkvsphiOnZDT")
drawCurvaturePlot(infile1,"hkvsphiOnZCSC1")
drawCurvaturePlot(infile1,"hkvsphiOnZCSC2")
drawCurvaturePlot(infile1,"hkvseta")



