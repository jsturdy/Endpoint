#!/bin/py
import ROOT
from ROOT import *

import random 
import array
#
# get list of random events for getEntry
#
def getRandomEntries(randgen,nRand,tree):
	randlist = []
	rmax = tree.GetEntries()
	if nRand >= rmax: 
		print "this is bullshit"
		return tree
	for j in range(0,nRand):
		rnum =randgen.Integer(rmax)
		while rnum in randlist:
			rnum =randgen.Integer(rmax)
		randlist.append(rnum)

	randlist.sort()
#	for r in randlist: print r

	return randlist
#
# get a random subset from a tree
#
def getRandomTree(randgen,nRandd,tree):
	tnew = tree.CloneTree(0)
	tnew.SetName(tree.GetName()+"_new")

	nRand = max(1,randgen.Poisson(nRandd))

	if nRand >= tree.GetEntries():
		print "cannot get random entry list -- not enough MC"
		print nRand,">",tree.GetEntries()
		return tnew
	else: print nRand,"<",tree.GetEntries()

	print tnew.GetName()
	entrylist=getRandomEntries(randgen,nRand,tree)

	for j in entrylist:
		tree.GetEntry(j)
		tnew.Fill()	

	return tnew



if __name__ == "__main__":
	print "testing the randomization of the MC Samples"
	can = TCanvas("can","can",600,600)
	
#
# set up the binning
#
	# put the sample bins into a full-blown array
#	bMassArray = array.array('d',samplebins)
#	hSampleBinsMass= TH1F("hSampleBinsMass","",len(bMassArray)-1,bMassArray)

	infile = TFile("root/compactMCTrees.root","open")
#	outfile = TFile("test/mcSampleController.root","recreate")
	outfile = TFile("temp.root","recreate")

	h = infile.hMassTrueFixedBins
	print h.Integral()
	scalefac = 9e6/h.Integral()
	print "scale factor",scalefac
	h.Scale(100)

	print h.GetNbinsX()
#	return
	print "new integral",h.Integral()
#	h = infile.hMassTrue
#	h.Rebin(10)
#	h.Draw()

	rand3 = TRandom3()
	rand3.SetSeed(42)
	ngen = h.GetBinContent(1)
	print "events to generate",ngen
	t0020 = getRandomTree(rand3,ngen,infile.dy0020)
	t0120= getRandomTree(rand3,h.GetBinContent(2),infile.dy0120)
	t0200= getRandomTree(rand3,h.GetBinContent(3),infile.dy0200)
	t0500= getRandomTree(rand3,h.GetBinContent(4),infile.dy0500)
	t0800= getRandomTree(rand3,h.GetBinContent(5),infile.dy0800)
#	t1000= getRandomTree(rand3,h.GetBinContent(6),infile.dy1000)
	print t0020.GetEntries()
	ltrees = TList()
	ltrees.Add(t0020)
	ltrees.Add(t0120)
	ltrees.Add(t0200)
	ltrees.Add(t0500)
	ltrees.Add(t0800)
#	ltrees.Add(t1000)
	
	tnew = t0020.MergeTrees(ltrees)
	tnew.Write("dimuons")	


'''
	nGen = int(10000)
	
#	print gRandom.GetSeed()
	gRandom.SetSeed(42)
	for i in range(0,nGen):
		m = infile.hMassTrue.GetRandom()	
		print i,m	
	
		hSampleBinsMass.Fill(m)
	

	hSampleBinsMass.Draw()	
	can.Update()
	can.SetLogy(1)
'''
