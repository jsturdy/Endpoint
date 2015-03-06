#ifndef __ToyMCSampler_h_
#define __ToyMCSampler_h_

#include "TF1.h"
#include "TFile.h"
#include "TRandom3.h"
#include "TTree.h"
#include "include/Format.h"


class ToyMCSampler {

  private:

	TRandom3* _rand3;
	int _seed;
	
	TF1* _fgen; 
//	TF1* _fgenPos; 


  public:

	ToyMCSampler(){};
	ToyMCSampler(int const seed, TF1 const* fgen);
	void setSeed(int const seed) { this->_seed = seed; _rand3->SetSeed(seed);}

	double genEvent();
	TF1* getFuncNeg(){ return this->_fgen;}
//	TF1* getFuncPos(){ return this->_fgenPos;}

	TTree* getTree(int ngen);
	TTree* getTree(int ngen,float biasflat); 
	TTree* getTreeSepPosNegShapes(int ngen,float biaspos, float biasneg, TF1* fpos, TF1* fneg);
};
//
// main constructor
//
ToyMCSampler::ToyMCSampler(int const seed, TF1 const* fgen){

	_rand3 = new TRandom3();
	_seed = seed;
	_rand3->SetSeed(seed);
		
	_fgen = (TF1*)fgen->Clone("fgenNeg");
//	_fgenPos = (TF1*)fgen->Clone("fgenPos");
//	_fgenPos->SetRange(-1*_fgen->GetXmax(),-1*_fgen->GetXmin());
//	_fgenPos->SetParameter(1,_fgenPos->GetParameter(1)*-1);
}
//
// generate a single event
//
double ToyMCSampler::genEvent() {
	double k = _fgen->GetRandom();
	if (_rand3->Rndm() < 0.5) k *= -1.;
	return k;
}
//
// get a tree
//

TTree* ToyMCSampler::getTree(int ngen) {
	 
	TTree* toytree = new TTree("toytree","toytree");
	typedef struct {
		float k;
	} outtype;
	outtype trk1;
	toytree->Branch("trk1",&trk1,"k/F");

	for (int igen = 0; igen < ngen; ++igen){
		trk1.k = this->genEvent();
		toytree->Fill();

	}

	return toytree;
}
//
// get a tree with a flat bias assumption
//
TTree* ToyMCSampler::getTree(int ngen,float biasflat) {
	
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
TTree* ToyMCSampler::getTreeSepPosNegShapes(int ngen,float biaspos, float biasneg, TF1* fpos, TF1* fneg) {
	
	TTree* toytree = new TTree("toytree","toytree");
	_OutType trk1;
	toytree->Branch("trk1",&trk1,trk1.contents().c_str());

	fpos->SetRange(1./3000,1./100);
	fneg->SetRange(-1./100.,-1./3000);

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
