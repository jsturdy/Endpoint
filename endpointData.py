#!/bin/py

#
# author: T. Nicholas (Nick) Kypreos
# email: kypt@phys.ufl.edu
# e-mail me or find me on linkedin if there 
# are any future troubles with this
#

#
# file for running the endpoint fit on collision data
#


import os,ROOT
import sys

from ROOT import *
from python.ufPlotTools import *
from python.Utils import *
from python.TreeController import TreeBreakController



ROOT.gROOT.LoadMacro("include/ToyMCSamplerHist.h+") 	# only used for generating toy MC 
ROOT.gROOT.LoadMacro("include/EndpointDataBalance.h+") 	# data-driven endpoint fit 
ROOT.gROOT.LoadMacro("include/EndpointMCScan.h+") 		# MC comparison endpoint fit (can work with the cosmic endpoint as well) 


# used for setting up plot style
# can be commented out if it's causing problems
setTDRStyle() 
can = TCanvas("can","can",600,600) 



#
# string name for the inputted data file
#
sdatafile = "endpoint_dimu_3908"


#
# load in the data and simulation files
# the "bootstrap" aka data-driven method, will always work alone
# MC might need to have multiple samples added together to get statistics
#
infiledata 	= TFile("root/"+sdatafile+".root","open")
#infilemc 	= TFile("root/endpointFormat/efRaw_dy0020.root","open")
infilemc 	= TFile("root/efRaw.root","open")


#
# constants for endpoint binning
#
nbinseta = 5 # number of eta bins
etacut = 2.1 # absolute value of the eta cut-off
nbinsphi = 1 # number of phi bins

# minimum pt for the endpoint fit
# a higher pt cut-off creates a more sensitive probe 
# also becomes less statistically powerful


#ptmin = 200  
#ptmin = 100
#ptmin = 45
ptmin = 50


#
# just chooses which treey I want to get out of the nTuple for 
# simulation
# The nTuple is just dimuon events that have been broken up per-muon
# The endpoint fit uses both muons in the event. It's easier
# to generalize the endpoint fit code when you don't need to feed
# it multple variable names. 
#
#stree = "muonsReco" 
#stree = "muonsTrue" 
stree = "muonsFsr" #post-fsr simulated muons (if I recall correctly) 

#outfile		= TFile("out/endpointData_%s_ptmin%03d_eta%2.0f.root"%(stree,ptmin,etacut*10),"recreate")
# create an output file
outfile		= TFile('gwar.root',"recreate")
#
#
#
treedata = infiledata.muonsTrk # pull the data tree out

treedata.Draw("trk1.k")


#
# histograms to keep track of the binning
#
hbinsEta = TH1F("hBinsEta","#eta bins; #eta", nbinseta, -etacut,etacut);
hbinsPhi = TH1F("hBinsPhi","#phi bins; #phi", nbinsphi, -TMath.Pi(),TMath.Pi());

#
# custom python class to handle dividing up 
# the tree without having to look at
# code that i keep screwing up
# 
tbc=TreeBreakController(treedata)
tbc.initEtaPhiLists(hbinsEta,hbinsPhi)
tbc.fillEtaTrees()
	
#etatreesdata = [treedata] 
etatreesdata = tbc.etatrees

#
# write out initial stuff
# only use if you want to write out how the trees were broken up
#
#for it,t in enumerate(tbc.etatrees): 
#	print t.GetEntries()
#	if True: t.Write("treeEta%d"%it)

hbinsEta.Write()
hbinsPhi.Write()


#
# initialize the data-driven endpoint fit
# I named it derp because I was probably grumpy
# when I wrote this.
# The call tells the EndpointDataBalance fit
# to use 11 bins for breaking up the q/pt distribution
# starting at ptmin = ptmin.  
# it will scann 400 steps ranging from a bias of -1 to 1 

#
edb = EndpointDataBalance("derp",11, ptmin,400,1.)

# create tgraphs for storing anaswers
greEta = TGraphErrors()
graEta = TGraphAsymmErrors()


#
# loop on trees that were broken up earlier
# based on an eta binning
# it's initially more computationally cumbersome to 
# parse out the q/pt distribution in bins of eta/phi before
# putting it into the fitter, but it simplifies the fitter itself.
# Simple fitters don't need to be de-bugged.
#
print 'running the eta loop on the endpoint bootstrap method'

for it,t in enumerate(etatreesdata): 
	print it,t.GetEntries()
		
	edb.reset() # clears all the histograms 
	edb.runEndpointLoop(t) # loop on the tree, named 't', that's fed into the fit
	edb.runChisquareFit() # does the chisquare comparison test
	edb.getChi2().Write("edb_eta_%03d"%it) # writes out the chisquare to a file for double-checking late on
 
# 
# go on and alculate the endpoint values. 
# this really needs to be checked to make sure nothing bad happened  
# 
# getEndpoint takes the chisquare distribution and looks for the minimum on the selected range
# Here, the range is set to (-1,1)
# it returns the value of the endpoint, vep1
# the parabolic errors, eep1 
# and the minos errors, eminos
#
	vep1, eep1, eminos = getEndpoint(edb.getChi2(),-1,1)

# it==0 has no selection on eta/phi
# use the previously defined eta/phi histograms to draw the endpoint with
# whatever external binning is required 
#
	if it>0:
		ec =hbinsEta.GetBinCenter(it)  
		ew =hbinsEta.GetBinWidth(it)
		ipoint = greEta.GetN()

#
# greEta and graEta are probably not the best names
# it worked at the time. 
# gre has the parabolic errors
# gra has the minos errors
#
		greEta.SetPoint(ipoint,ec,vep1)
		greEta.SetPointError(ipoint,0.5*ew,eep1)

		graEta.SetPoint(ipoint,ec,vep1)
		graEta.SetPointError(ipoint,0.5*ew,0.5*ew,eminos[0],eminos[1])

greEta.SetTitle(";#eta;#kappa [c/TeV]")
graEta.SetTitle(";#eta;#kappa [c/TeV]")
greEta.Draw("ape")
graEta.Draw("ape")
can.Update()
greEta.Write("gre_edb_parab_eta")
graEta.Write("gre_edb_minos_eta")



# 
# get the MC tree for the comparison 
# 
#treemc = infilemc.muonsFsr
#treemc = infilemc.muonsTrue
treemc = infilemc.Get(stree)
#
# same kind of endpoint as the data-driven endpoint
# works a bit differently to handle data and
# multiple MC samples
#
emcs = EndpointMCScan("duck",20, ptmin, 200, 1);
tbcmc = TreeBreakController(treemc)
tbcmc.initEtaPhiLists(hbinsEta,hbinsPhi)
tbcmc.fillEtaTrees()



greEtaMCS = TGraphErrors()
graEtaMCS = TGraphAsymmErrors()
#for ifit,(tdata,tmc) in zip(tbc.etatrees,tbcmc.etatrees):

for ifit in range(0,len(tbc.etatrees)):
	td = tbc.etatrees[ifit]
	tmc = tbcmc.etatrees[ifit]

	emcs.reset() #reset the distributions just to be safe

	emcs.fillData(td) # fill the data distributions
	emcs.appendMCWeighted(tmc) # add an MC sample to the MC comparison. multiple MC samples can be added


#
# works just like the other endpoint method.  
# the MC method always returns a bias needed in simulation to match data
# the data-driven method always returns a correction required to remove the bias
# from data. The difference will be a negative sign! 
# Make sure you understand when you're getting a BIAS and when you're 
# betting a CORRECTION
#
	emcs.runChisquareFit()
	emcs.runChisquareFitPosNeg()
	emcs.getChi2Sum().Write("emcs_chi2sum_%d"%ifit)
	emcs.getChi2().Write("emcs_chi2_%d"%ifit)
	emcs.getChi2Pos().Write("emcs_chi2pos_%d"%ifit)
	emcs.getChi2Neg().Write("emcs_chi2neg_%d"%ifit)
	vep, eep, eminos = getEndpoint(emcs.getChi2(),-1,1)
	if ifit>0:
		ec =hbinsEta.GetBinCenter(ifit)
		ew =hbinsEta.GetBinWidth(ifit)
		ipoint = greEtaMCS.GetN()
		greEtaMCS.SetPoint(ipoint,ec,vep)
		greEtaMCS.SetPointError(ipoint,0.5*ew,eep)

		graEtaMCS.SetPoint(ipoint,ec,vep)
		graEtaMCS.SetPointError(ipoint,0.5*ew,0.5*ew,eminos[0],eminos[1])
	
greEtaMCS.SetTitle(";#eta;#kappa [c/TeV]")
graEtaMCS.SetTitle(";#eta;#kappa [c/TeV]")
greEtaMCS.Write("gre_emcs_parab_eta")
graEtaMCS.Write("gre_emcs_minos_eta")



# 
# I don't remember what any of this is, but I'm leaving it all commented in case it's helpful in some way
#  
'''
emcs.fillData(treedata);
emcs.appendMCWeighted(treemc)
ifit = 0
emcs.runChisquareFit()
emcs.runChisquareFitPosNeg()
emcs.getChi2Sum().Write("emcs_chi2sum_%d")
emcs.getChi2().Write("emcs_chi2_%d")
emcs.getChi2Pos().Write("emcs_chi2pos_%d")
emcs.getChi2Neg().Write("emcs_chi2neg_%d")
'''

'''
emcs.getChi2Sum().Draw()
emcs.getChi2().Draw()
emcs.getChi2Pos().Draw("same")
emcs.getChi2Neg().Draw("same")
'''


'''
infilemc1 	= TFile("root/endpointFormat/efRaw_dy0020.root","open")
infilemc2 	= TFile("root/endpointFormat/efRaw_dy0120.root","open")
infilemc3 	= TFile("root/endpointFormat/efRaw_dy0200.root","open")
infilemc4 	= TFile("root/endpointFormat/efRaw_dy0500.root","open")
infilemc5 	= TFile("root/endpointFormat/efRaw_dy0800.root","open")

tbcs_mc = []
stree = "muonsTrue"
tbcs_mc.append(TreeBreakController(infilemc1.Get(stree))
tbcs_mc.append(TreeBreakController(infilemc2.Get(stree))
tbcs_mc.append(TreeBreakController(infilemc3.Get(stree))
tbcs_mc.append(TreeBreakController(infilemc4.Get(stree))
tbcs_mc.append(TreeBreakController(infilemc5.Get(stree))

emcs = EndpointMCScan("duck",20, ptmin, 200, 1);

#emcs.fillData(treedata);
#emcs.appendMCWeighted(treemc)

etatreesmc = [infilemc1.Get(stree),infilemc2.Get(stree),infilemc3.Get(stree),infilemc4.Get(stree),infilemc5.Get(stree)]
'''





