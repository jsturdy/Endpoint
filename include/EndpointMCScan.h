#ifndef __EndpointMCScan_h_
#define __EndpointMCScan_h_
#include <iostream>
#include "TTree.h"
#include "TLorentzVector.h"
#include "TH1.h"
#include "TH2.h"
#include "include/Format.h"

class EndpointMCScan {


  private:
	TString _sname;

	TH1F* _kdata;
	TH2F* _kmcVsBias;
	TH1F* _chi2;

	TH1F* _kdataPos;
	TH1F* _kdataNeg;
	TH2F* _kmcVsBiasPos;
	TH2F* _kmcVsBiasNeg;
	TH1F* _chi2Pos;
	TH1F* _chi2Neg;
	TH1F* _chi2Sum;

	double _minPt;
	int _nbinsFill;
	_OutType getBiasTrack(_OutType trk,double bias);

  public:
//	EndpointMCScan();
	EndpointMCScan(TString const sname= "derp",int const _nkbins=100, double const _minpt=40, int const _nbiasBins=400, double const _biasRange = 5);
	void fillData(TTree* tree);
	void fillMC(TTree* tree);
	void appendMCWeighted(TTree* tree);//,double const weight);
	void runChisquareFit();
	void runChisquareFitPosNeg();
//	void runChisquareFitPosNeg(TH2F* hproj,TH1F* hchi2);
	void runChisquareFitPosNeg(TH2F* hproj,TH1F* hdata, TH1F* hchi2);
	void reset();

	TH1F* getHistData() { return _kdata;}
	TH1F* getHistDataPos() { return _kdataPos;}
	TH1F* getHistDataNeg() { return _kdataNeg;}
	TH2F* getHistMCScan() { return _kmcVsBias;}
	TH2F* getHistMCScanPos() { return _kmcVsBiasPos;}
	TH2F* getHistMCScanNeg() { return _kmcVsBiasNeg;}
	TH1F* getChi2() { return _chi2;}
	TH1F* getChi2Pos() { return _chi2Pos;}
	TH1F* getChi2Neg() { return _chi2Neg;}
	TH1F* getChi2Sum() { return _chi2Sum;}
	
};
//
//
//

EndpointMCScan::EndpointMCScan(TString const sname,int const _nkbins, double const _minpt, int const _nbiasBins, double const _biasRange){

	_sname 	= sname;
	_minPt	= _minpt;

	int nkbins 		 = _nkbins;
	int nbiasBins 	 = _nbiasBins;
	double biasRange = _biasRange*1e-3;
	_nbinsFill = _nkbins; 

	_kdata 		= new TH1F(TString::Format("%s__kdata",_sname.Data()),";#kappa",nkbins,-1./_minPt,1./_minPt);
	_kdata->SetLineWidth(3);
	_kdata->GetXaxis()->SetNdivisions(105);
//	_kdataPos 	= new TH1F(TString::Format("%s__kdataPos",_sname.Data()),";#kappa",nkbins,-1./_minPt,1./_minPt);
//	_kdataNeg 	= new TH1F(TString::Format("%s__kdataNeg",_sname.Data()),";#kappa",nkbins,-1./_minPt,1./_minPt);
	_kdataPos 	= (TH1F*)_kdata->Clone(TString::Format("%s__kdataPos",_sname.Data()));	
	_kdataNeg 	= (TH1F*)_kdata->Clone(TString::Format("%s__kdataNeg",_sname.Data()));	
	_kdataPos->SetLineColor(kBlue);
	_kdataNeg->SetLineColor(kRed);



	_kmcVsBias 	= new TH2F(TString::Format("%s__kmcVsBias",_sname.Data()),";#kappa [c/GeV];q/p_{T} [c/GeV]",nbiasBins,-biasRange,biasRange,	nkbins,-1./_minPt,1./_minPt);
	_kmcVsBias->GetXaxis()->SetNdivisions(105);
	_kmcVsBias->Sumw2();
	_kmcVsBiasPos = (TH2F*)_kmcVsBias->Clone(TString::Format("%s__kmcVsBiasPos",_sname.Data()));
//	_kmcVsBiasPos = new TH2F(TString::Format("%s__kmcVsBiasPos",_sname.Data()),";#kappa [c/GeV];q/p_{T} [c/GeV]",nbiasBins,-biasRange,biasRange,	int(nkbins/2),0,1./_minPt);
//	_kmcVsBiasPos->GetXaxis()->SetNdivisions(105);
//	_kmcVsBiasPos->Sumw2();
//	_kmcVsBiasNeg = (TH2F*)_kmcVsBiasPos->Clone(TString::Format("%s__kmcVsBiasNeg",_sname.Data()));
	_kmcVsBiasNeg = (TH2F*)_kmcVsBias->Clone(TString::Format("%s__kmcVsBiasNeg",_sname.Data()));

	_chi2		= new TH1F(TString::Format("%s_chi2",_sname.Data()),";#kappa;#chi^{2}",nbiasBins,-biasRange*1e3,biasRange*1e3);
	_chi2->SetLineWidth(3);
	_chi2Pos		= (TH1F*)_chi2->Clone(TString::Format("%s_chi2Pos",_sname.Data()));
	_chi2Neg		= (TH1F*)_chi2->Clone(TString::Format("%s_chi2Neg",_sname.Data()));
	_chi2Sum		= (TH1F*)_chi2->Clone(TString::Format("%s_chi2Sum",_sname.Data()));
	_chi2Pos->SetLineColor(kBlue);
	_chi2Neg->SetLineColor(kRed);

}

//
// fill the data nTuple
//
void EndpointMCScan::fillData(TTree* tree) {

	int numEntries = tree->GetEntries();

	_OutType trk1;

	tree->SetBranchAddress("trk1",&trk1);

	for (int jEntry = 0; jEntry < numEntries; ++jEntry) {	
		tree->GetEntry(jEntry);

		_kdata->Fill(trk1.k);
		if (trk1.k > 0) _kdataPos->Fill(trk1.k);
		else _kdataNeg->Fill(trk1.k); 
	}
}
//
// fill the mc nTuple
//
void EndpointMCScan::fillMC(TTree* tree) {

	int numEntries = tree->GetEntries();

	_OutType trk1;

	tree->SetBranchAddress("trk1",&trk1);

	int numBinsk = _kmcVsBias->GetNbinsX();
	for (int jEntry = 0; jEntry < numEntries; ++jEntry) {	
		tree->GetEntry(jEntry);
	
		for (int ibias = 1; ibias <= numBinsk; ++ibias) {
			double kbias =_kmcVsBias->GetXaxis()->GetBinCenter(ibias); 

			_OutType trk1a =  getBiasTrack(trk1,kbias);
			_kmcVsBias->Fill(kbias,trk1a.k);
			if (trk1a.k > 0) _kmcVsBiasPos->Fill(kbias,trk1a.k);
			else 			_kmcVsBiasNeg->Fill(kbias,trk1a.k);

		}


	}

}
//
// fill the mc nTuple
//
void EndpointMCScan::appendMCWeighted(TTree* tree){//, double const weight) {

	int numEntries = tree->GetEntries();

	_OutType trk1;

	tree->SetBranchAddress("trk1",&trk1);
	float wt;
	tree->SetBranchAddress("weight",&wt);

	TH2F* htemp = (TH2F*)_kmcVsBias->Clone("htemp");
	htemp->Reset();
	TH2F* htempPos = (TH2F*)htemp->Clone("htempPos");
	TH2F* htempNeg = (TH2F*)htemp->Clone("htempNeg");

	int numBinsk = _kmcVsBias->GetNbinsX();

//	double weight = 1.;

	for (int jEntry = 0; jEntry < numEntries; ++jEntry) {	
		tree->GetEntry(jEntry);
//		if (jEntry ==1) weight = wt;
		for (int ibias = 1; ibias <= numBinsk; ++ibias) {
			double kbias =_kmcVsBias->GetXaxis()->GetBinCenter(ibias); 

			_OutType trk1a =  getBiasTrack(trk1,kbias);
			htemp->Fill(kbias,trk1a.k,wt);
//			if (trk1.k > 0)  htempPos->Fill(kbias,trk1a.k);
			if (trk1a.k > 0) htempPos->Fill(kbias,trk1a.k,wt);
			else 			 htempNeg->Fill(kbias,trk1a.k,wt);

		}


	}
/*	
//	std::cout<<htemp->GetEntries()<<"\t"<<weight<<std::endl;
	this->_kmcVsBias		->Add(htemp,weight);
	this->_kmcVsBiasPos	->Add(htempPos,weight);
	this->_kmcVsBiasNeg	->Add(htempNeg,weight);
//	std::cout<<_kmcVsBias->GetEntries()<<std::endl;
*/
	this->_kmcVsBias	->Add(htemp);
	this->_kmcVsBiasPos	->Add(htempPos);
	this->_kmcVsBiasNeg	->Add(htempNeg);
	htemp->Delete();
	htempPos->Delete();
	htempNeg->Delete();
}

//
//
//
void EndpointMCScan::runChisquareFit(){

	int numBinsk = _kmcVsBias->GetNbinsX();


	for (int ibin = 1; ibin <= numBinsk; ++ibin) {
		TH1F* hmc = (TH1F*)_kmcVsBias->ProjectionY("pymc",ibin,ibin);
	
		float chi2 = _kdata->Chi2Test(hmc,"UW,CHI2"); 
		_chi2->SetBinContent(ibin,chi2);
		hmc->Delete();

	}

}

void EndpointMCScan::runChisquareFitPosNeg(TH2F* hproj,TH1F* hdata, TH1F* hchi2){
	int numBinsk = hproj->GetNbinsX();


	double scale = hdata->Integral(1,_nbinsFill);
	for (int ibin = 1; ibin <= numBinsk; ++ibin) {
		TH1F* hmc = (TH1F*)hproj->ProjectionY("pymc",ibin,ibin);
		double scalefac = scale / double(hmc->Integral(1,_nbinsFill));
		hmc->Scale(scalefac);
	
		float chi2 = hdata->Chi2Test(hmc,"UW,CHI2"); 
		hchi2->SetBinContent(ibin,chi2);
		hmc->Delete();

	}

}

void EndpointMCScan::runChisquareFitPosNeg(){

	_chi2Pos->Reset();
	_chi2Neg->Reset();
	_chi2Sum->Reset();
	runChisquareFitPosNeg(this->_kmcVsBiasPos,this->_kdataPos,this->_chi2Pos);
	runChisquareFitPosNeg(this->_kmcVsBiasNeg,this->_kdataNeg,this->_chi2Neg);
	_chi2Sum->Add(_chi2Pos,1.);
	_chi2Sum->Add(_chi2Neg,1.);
	

}
//
//
//
_OutType EndpointMCScan::getBiasTrack(_OutType trk,double bias){
	trk.k = trk.k-bias;
	return trk;
}
//
//
//
void EndpointMCScan::reset() {
	_kdata 			->Reset();	
	_kdataPos 		->Reset();	
	_kdataNeg 		->Reset();	
	_kmcVsBias 		->Reset();
	_kmcVsBiasPos 	->Reset();
	_kmcVsBiasNeg 	->Reset();
	_chi2			->Reset();
	_chi2Neg		->Reset();
	_chi2Pos		->Reset();
	_chi2Sum		->Reset();
	
}
#endif
