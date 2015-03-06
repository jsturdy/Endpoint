#ifndef __ToyMCSamplerHist_h_
#define __ToyMCSamplerHist_h_

#include "TF1.h"
#include "TH1.h"
#include "TFile.h"
#include "TRandom3.h"
#include "TTree.h"
#include "include/Format.h"


class ToyMCSamplerHist {

  private:

	TRandom3* _rand3;
	int _seed;
	
	TH1F* _fgen; 


  public:

	ToyMCSamplerHist(){};
	ToyMCSamplerHist(int const seed, TH1F const* fgen);
	void setSeed(int const seed) { this->_seed = seed; _rand3->SetSeed(seed);}

	double genEvent();
	TH1F* getFuncNeg(){ return this->_fgen;}

	TTree* getTree(int ngen);
	TTree* getTree(int ngen,float biasflat); 
	TTree* getTreeSepPosNegShapes(int ngen,float biaspos, float biasneg, TH1F* fpos, TH1F* fneg);
};
//
// main constructor
//
ToyMCSamplerHist::ToyMCSamplerHist(int const seed, TH1F const* fgen){

	_rand3 = new TRandom3();
	_seed = seed;
	_rand3->SetSeed(seed);
		
	_fgen = (TH1F*)fgen->Clone("fgenNeg");
}
//
// generate a single event
//
double ToyMCSamplerHist::genEvent() {
	double k = _fgen->GetRandom();
	if (_rand3->Rndm() < 0.5) k *= -1.;
	return k;
}
//
// get a tree
//

TTree* ToyMCSamplerHist::getTree(int ngen) {
	 
	TTree* toytree = new TTree("toytree","toytree");
//	typedef struct {
//		float k;
//	} outtype;
//	outtype trk1;
	_OutType trk1;
	toytree->Branch("trk1",&trk1,trk1.contents().c_str());
//	toytree->Branch("trk1",&trk1,"k/F");

	for (int igen = 0; igen < ngen; ++igen){
		trk1.k = this->genEvent();
		toytree->Fill();

	}

	return toytree;
}
//
// get a tree with a flat bias assumption
//
TTree* ToyMCSamplerHist::getTree(int ngen,float biasflat) {
	
	TTree* toytree = new TTree("toytree","toytree");
	_OutType trk1;
	toytree->Branch("trk1",&trk1,trk1.contents().c_str());

	for (int igen = 0; igen < ngen; ++igen){
		trk1.k = this->genEvent()-biasflat;
		toytree->Fill();

	}

	return toytree;
}
//
//
//
TTree* ToyMCSamplerHist::getTreeSepPosNegShapes(int ngen,float biaspos, float biasneg, TH1F* fpos, TH1F* fneg) {
	
	TTree* toytree = new TTree("toytree","toytree");
	_OutType trk1;
	toytree->Branch("trk1",&trk1,trk1.contents().c_str());

//	fpos->SetRange(1./3000,1./100);
//	fneg->SetRange(-1./100.,-1./3000);

	for (int igen = 0; igen < ngen; ++igen){

		double p =_rand3->Rndm();
		if (p < 0.5) {
			trk1.k = -1.*fpos->GetRandom() - biaspos;
		} else {
			trk1.k = fneg->GetRandom() - biasneg;
			
		}
		
//		trk1.k = this->genEvent()-biasflat;
		toytree->Fill();

	}

	return toytree;
}


#endif
