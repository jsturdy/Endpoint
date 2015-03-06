#!/bin/py
import ROOT
from ROOT import *


class TreeBreakController:
	def __init__(self,tree):

		self.info ='''
TreeBreakController v1.0
T. Nicholas kypreos, 13 July 2012
kypt@phys.ufl.edu
'''
		print self.info 

		self.mastertree = tree
		print "size of master tree: ",self.mastertree.GetEntries()
		self.hasEta = False
		self.hasPhi = False


		self.lfeta 	= self.mastertree.GetBranch("trk1").GetLeaf("eta")
		self.lfk 	= self.mastertree.GetBranch("trk1").GetLeaf("k")
		self.lfphi 	= self.mastertree.GetBranch("trk1").GetLeaf("phi")
		
		
#
# set values
#
	def setEtaHist(self,heta): 
		self.etabins = heta
		self.hasEta = True

	def setPhiHist(self,hphi): 
		self.phibins = hphi
		self.hasPhi = True

	def setTree(self,tree):
		self.mastertree = tree
		self.lfeta 	= self.mastertree.GetBranch("trk1").GetLeaf("eta")
		self.lfk 	= self.mastertree.GetBranch("trk1").GetLeaf("k")
		self.lfphi 	= self.mastertree.GetBranch("trk1").GetLeaf("phi")
		print "new tree size: ", tree.GetEntries()
		
#
# return values
#
	def getEtaHist(self):
		if self.hasEta: return self.etabins
		else:
			print "eta bins are not defined"
			return -1
	
	def getPhiHist(self):
		if self.hasPhi: return self.phibins
		else:
			print "phi bins are not defined"
			return -1
#
#
#
	def createTreeList(self,hist):
		nbins = hist.GetNbinsX()
		hname = hist.GetName()
		print hname,nbins
		
		print hist.GetXaxis().GetXmax()
		print hist.GetXaxis().GetXmin()

		trees = []
		for i in range(0,nbins+1):
			newtree = self.mastertree.CloneTree(0)
			newtree.SetName("%s_%d"%(hname,i))
			trees.append(newtree)
			
		return trees

	def initEtaPhiLists(self,heta,hphi):
		print "initializing eta and phi lists"
		self.setEtaHist(heta)
		self.setPhiHist(hphi)

		self.etatrees =self.createTreeList(self.etabins)
		self.phitrees =self.createTreeList(self.phibins)


	def fillEtaTrees(self):
		
		etamin = self.etabins.GetXaxis().GetXmin()
		etamax = self.etabins.GetXaxis().GetXmax()
		
		for jentry in self.mastertree:
			eta = self.lfeta.GetValue()
			k = self.lfk.GetValue()
			if eta < etamin or eta > etamax: continue	
			ibin = self.etabins.FindBin(eta)
			self.etatrees[0].Fill()
			self.etatrees[ibin].Fill()

	def fillPhiTrees(self,etamin,etamax):
		
		phimin = self.phibins.GetXaxis().GetXmin()
		phimax = self.phibins.GetXaxis().GetXmax()
		
		for jentry in self.mastertree:
			eta = self.lfeta.GetValue()
			phi = self.lfphi.GetValue()
			k = self.lfk.GetValue()
			if eta < etamin or eta > etamax: continue	
			if phi < phimin or phi > phimax: continue	
			ibin = self.phibins.FindBin(phi)
			self.phitrees[0].Fill()
			self.phitrees[ibin].Fill()


	
if __name__ == "__main__":

	print 'testing the endpoint controller'
	nbinseta = 5
	nbinsphi = 6 
	ptmin = 100
	ptmin = 45
	etacut = 2.4
	stree = "muonsOpt"
	stree = "muonsTrk"
	sinfile = "endpoint_dimu_3908" 

	infile = TFile("root/%s.root"%(sinfile),"open")
	outfile = TFile("temp.root","recreate")
	tree = infile.Get(stree)

	hbinsEta = TH1F("hBinsEta","#eta bins; #eta", nbinseta, -etacut,etacut);
	hbinsPhi = TH1F("hBinsPhi","#phi bins; #phi", nbinsphi, -TMath.Pi(),TMath.Pi());

	print tree.GetEntries()
	
	tbc=TreeBreakController(tree)
#	etatrees=tbc.createTreeList(hbinsEta)
	tbc.initEtaPhiLists(hbinsEta,hbinsPhi)
	tbc.fillEtaTrees()
	
	for t in tbc.etatrees: print t.GetEntries()
	
		
		
	
