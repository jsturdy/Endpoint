#ifndef __EndpointDataBalance_h_
#define __EndpointDataBalance_h_
#include <iostream>
#include "TTree.h"
#include "TLorentzVector.h"
#include "TH1.h"
#include "TF1.h"
#include "TH2.h"
#include "include/Format.h"
#include "include/EndpointTools.h"

class EndpointDataBalance {

  private:

	TString _sname;

	TH1F* _kpos;
	TH1F* _kneg;
	TH2F* _kposVsBias;
	TH2F* _knegVsBias;
	
	TH1F* _chi2;
	double _minPt;


//	TF1* _funcPtDep;

  public:
	EndpointDataBalance(TString const sname= "derp",int const _nkbins=100, double const _minpt=40, int const _nbiasBins=400, double const _biasRange = 5);
	void runEndpointLoop(TTree* tree);
	void runChisquareFitCut(double const ptcut = 15.);
	void runChisquareFit();

	_OutType getBiasTrack(_OutType trk,double bias);
	void reset();


	TH1F* getHistPos() { return _kpos;}
	TH1F* getHistNeg() { return _kneg;}
	TH1F* getChi2() { return _chi2;}


//	void setPtDepPars(double const omega,double const mu, double const k1, double const k2 ) {_funcPtDep->SetParameters(0.5,omega,mu,k2,k1);}

};
//
// constructor
//
//
//
//
EndpointDataBalance::EndpointDataBalance(TString const sname,int const _nkbins, double const _minpt, int const _nbiasBins, double const _biasRange) {
	_sname 	= sname;
	_minPt			= _minpt;

	int nkbins 		 = _nkbins;
	double minpt 	 = _minpt;
	int nbiasBins 	 = _nbiasBins;
	double biasRange = _biasRange*1e-3;

//	std::cout<<1./minpt<<std::endl;

//	_kpos 			= new TH1F(TString::Format("%s_kpos",_sname.Data()),";q/p_{T}",nkbins,0,1);
	_kpos 			= new TH1F(TString::Format("%s_kpos",_sname.Data()),";q/p_{T}",nkbins,0,1./minpt);
	_kneg 			= new TH1F(TString::Format("%s_kneg",_sname.Data()),";q/p_{T}",nkbins,0,1./minpt);
	_kposVsBias 	= new TH2F(TString::Format("%s_kposVsBias",_sname.Data()),";#kappa;#kappa",nbiasBins,-biasRange,biasRange,	nkbins,0,1./minpt);
	_knegVsBias 	= new TH2F(TString::Format("%s_knegVsBias",_sname.Data()),";#kappa;#kappa",nbiasBins,-biasRange,biasRange,	nkbins,0,1./minpt);
	

	_chi2	= new TH1F(TString::Format("%s_chi2",_sname.Data()),";#kappa;#chi^{2}",nbiasBins,-biasRange*1e3,biasRange*1e3);


}
//
// reset all histograms
//
void EndpointDataBalance::reset() {
	_kpos->Reset();
	_kneg->Reset();
	_kposVsBias->Reset();
	_knegVsBias->Reset();
	_chi2->Reset();
	
}
//
//
//
void EndpointDataBalance::runEndpointLoop(TTree* tree) {

	int numEntries = tree->GetEntries();

	_OutType trk1;
	tree->SetBranchAddress("trk1",&trk1);

	int numBinsk = _kposVsBias->GetNbinsX();

//
//loop on events in the ttree
// 
	for (int jEntry = 0; jEntry < numEntries; ++jEntry) {	
		tree->GetEntry(jEntry);
		if (trk1.k>0) 	_kpos->Fill(trk1.k);	
		else 			_kneg->Fill(fabs(trk1.k));
//
// inject a bias for pull and closure tests
//
	
		for (int ibias = 1; ibias <= numBinsk; ++ibias) {
			double kbias =_kposVsBias->GetXaxis()->GetBinCenter(ibias); 

			_OutType trk1a =  getBiasTrack(trk1,kbias);
			
			if (trk1a.k>0) 	_kposVsBias->Fill(kbias,trk1a.k);	
			else 			_knegVsBias->Fill(kbias,fabs(trk1a.k));

		}
	

	}
}
//
//
//
_OutType EndpointDataBalance::getBiasTrack(_OutType trk,double bias){
	trk.k = trk.k+bias;
	return trk;
}
//
//
//
void EndpointDataBalance::runChisquareFitCut(double const ptcut){

	bool _debug = false;

	int numBinsk = _kposVsBias->GetNbinsX();

	double kmax = 1./ptcut;
	if (_debug) std::cout<<"running the chisquare fit routine"<<std::endl;



	for (int ibin = 1; ibin <= numBinsk; ++ibin) {
		TH1F* hpos = (TH1F*)_kposVsBias->ProjectionY("pypos",ibin,ibin);
		TH1F* hneg = (TH1F*)_knegVsBias->ProjectionY("pyneg",ibin,ibin);

//		std::cout<<hpos->GetEntries()<<"\t"<<hneg->GetEntries()<<std::endl;
		hpos->GetXaxis()->SetRangeUser(0,kmax);
		hneg->GetXaxis()->SetRangeUser(0,kmax);

		float chi2 = hpos->Chi2Test(hneg,"UU,CHI2"); 

		float temp = EndpointTools::Chi2Test(hpos,hneg);

		std::cout<<chi2<<"\t"<<temp<<std::endl;
		_chi2->SetBinContent(ibin,chi2);
			
//		int ndf= hpos->Chi2Test(hneg,"UU,CHI2/NDF"); 
//		std::cout<<chi2/ndf<<std::endl;

	}

}
void EndpointDataBalance::runChisquareFit(){

	bool _debug = false;

	int numBinsk = _kposVsBias->GetNbinsX();

	if (_debug) std::cout<<"running the chisquare fit routine"<<std::endl;


	for (int ibin = 1; ibin <= numBinsk; ++ibin) {
		TH1F* hpos = (TH1F*)_kposVsBias->ProjectionY("pypos",ibin,ibin);
		TH1F* hneg = (TH1F*)_knegVsBias->ProjectionY("pyneg",ibin,ibin);

//		float chi2 = hpos->Chi2Test(hneg,"UU,CHI2"); 
		float chi2 = EndpointTools::Chi2Test(hpos,hneg);
/*
		float temp = EndpointTools::Chi2Test(hpos,hneg);

		std::cout<<chi2<<"\t"<<temp<<std::endl;
			
//		int ndf= hpos->Chi2Test(hneg,"UU,CHI2/NDF"); 
//		std::cout<<chi2/ndf<<std::endl;
*/
		_chi2->SetBinContent(ibin,chi2);
	}

}
#endif

