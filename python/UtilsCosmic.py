#!/bin/py

import ROOT
from ROOT import *

tex = TLatex()
tex.SetNDC()
tex.SetTextFont(42)

#can = TCanvas("can","can",600,600)
#can2 = TCanvas("can2","can2",1200,400)

fit = TF1("fit","pol8")
#fit = TF1("fit","pol6")
fit.SetRange(-5e-4,5e-4)
fit.SetLineWidth(2)
fit.SetLineStyle(1)
fit.SetNpx(100)
def getMinosErrors(fitfunc):
	
	minx = fitfunc.GetMinimumX()
	start = fitfunc.Eval(minx)
	step = 1e-3

#
	istep =0
	diff = 0
	xval = minx 
	while diff < 1.:
		xval= xval+step
		istep = istep+1
		diff = fitfunc.Eval(xval)-start	
		if istep>5000:
			diff = 100
			xval = 1
#		print istep,diff,xval
	xmax = xval	
#
	istep =0
	diff = 0
	xval = minx 
	while diff < 1.:
		xval= xval-step
		istep = istep+1
		diff = fitfunc.Eval(xval)-start	
		if istep>5000:
			diff = 100
			xval = 1
	xmin = xval
	minerr = (abs(minx-xmin),abs(minx-xmax))

	return minerr


def getEndpoint(hist):
	

	fit.SetRange(-0.5,0.5)
	fit.SetRange(-5.,5.)
	fit.SetRange(-2.,2.)
	fit.SetRange(-0.8,0.8)
	fit.SetRange(-0.5,0.5)
	hist.Fit("fit","bQFr")


#	val = fit.GetMinimumX(-0.2,0.2)
	val = fit.GetMinimumX(-0.5,0.5)
	err = sqrt(2./fit.Derivative2(val))
	minosError = getMinosErrors(fit)

	return val,err,minosError
'''
#
# get the minos errors
#
def getMinosErrors(fitfunc):
	
	minx = fitfunc.GetMinimumX()
	start = fitfunc.Eval(minx)
#	print "starting point ", "bias = ",minx, "chi2 = ",start

	step = 1e-3

#
	istep =0
	diff = 0
	xval = minx 
	while diff < 1.:
		xval= xval+step
		istep = istep+1
		diff = fitfunc.Eval(xval)-start	
#		print "","",istep
		if istep>5000:
			diff = 100
			xval = 1
#		print istep,diff,xval
	xmax = xval	
#
	istep =0
	diff = 0
	xval = minx 
	while diff < 1.:
		xval= xval-step
		istep = istep+1
		diff = fitfunc.Eval(xval)-start	
#		print "","",istep
#		print istep,diff,xval
		if istep>5000:
			diff = 100
			xval = 1
	xmin = xval
	minerr = (abs(minx-xmin),abs(minx-xmax))
#	print "bias = %.3f - %.3f + %.3f [c/TeV]"%(minx*1e0,minerr[0]*1e0,minerr[1]*1e0)

	return minerr
#
# get a coars range
#

def getRangeCoarse(infile):
	hpos = infile.Get("posOnlyHist")
	hneg = infile.Get("negOnlyHist")
	bin1 = hneg.GetMaximumBin()
	bin2 = hpos.GetMaximumBin()
	x1 = hneg.GetBinCenter(bin1)
	x2 = hpos.GetBinCenter(bin2)
	return x1,x2
#	return 


def getName(imode,isysmode):

	smode = ""

	if imode == 0: smode = "MC Truth"
	if imode == 1: smode = "MC RECO"
	if imode == 2: smode = "MC CORR RECO"
	if imode == 3: smode = "MC RECO as DATA"
	if imode == 4: smode = "MC CORR RECO as DATA"


sphi = ("#phi <0","#phi < -2.09","-2.09<#phi<-1.05","#phi>-1.05")
phibinsx = list([(-3.14,-2.09),(-2.09,-1.05),(-1.05,0)])

def makeStatsBig(canv,x1=0.7,y1=0.7,x2=0.99):
	statsbox = canv.GetPrimitive("stats")
	statsbox.SetX1NDC(x1)
	statsbox.SetY1NDC(y1)
	statsbox.SetX2NDC(x2)
	canv.Update()

'''

