#ifndef __EndpointTools_h_
#define __EndpointTools_h_

#include <iostream>
#include "TH1F.h"


namespace EndpointTools {

//  public:
//	EndpointTools(){}

//	double Chi2Test(TH1F* h1, TH1F* h2);
	double Chi2Test(TH1F const* h1, TH1F const* h2);
	double Chi2TestPlay(TH1F const* h1, TH1F const* h2);
	double Chi2Test1(TH1F const* h1, TH1F const* h2);

//	double Chi2Statistic(double v1, double v2, double e1, double e2);

};

//
//
//
double EndpointTools::Chi2Test(TH1F const* h1, TH1F const* h2) {

	int nbinsx = h1->GetNbinsX();
	double threshold = 1;
	
	bool _debug = false;	
	if (_debug) std::cout<<"\t\tnumber of bins: "<<nbinsx
		<<"\n\t\tthreshold: "<<threshold
		<<std::endl;


	double sumchi2 = 0;
	int ndf = 0;
	double N = 0;
	double M = 0;

	for (int ibin =1; ibin <= nbinsx; ++ibin) {

		double v1 = h1->GetBinContent(ibin);
		double v2 = h2->GetBinContent(ibin);
		if (v1 < threshold && v2 < threshold) continue;
		++ndf;
		N += v1;//h1->GetBinContent(ibin);
		M += v2;//h2->GetBinContent(ibin);
	}

	for (int ibin =1; ibin <= nbinsx; ++ibin) {

		double v1 = h1->GetBinContent(ibin);
		double v2 = h2->GetBinContent(ibin);
		if (v1 < threshold && v2 < threshold) continue;
		
		double e1 = h1->GetBinError(ibin);
		double e2 = h2->GetBinError(ibin);
		double uncsq = e1*e1+e2*e2;

		if (uncsq ==0) continue;
		double locchi = (M*v1 - N*v2);	
		sumchi2 += locchi*locchi/(uncsq);

	}
	
	sumchi2 /= (N*M);
	if (_debug) std::cout<<"chi2 = "<<sumchi2<<"\t ndf = "<<ndf<<std::endl;
	return sumchi2;

/*
	double nEvts1 = 0;
	double nEvts2 = 0;

	for (int ibin =1; ibin <= nbinsx; ++ibin) {



		double v1 = h1->GetBinContent(ibin);
		double v2 = h2->GetBinContent(ibin);
		nEvts1 += v1;//h1->GetBinContent(ibin);
		nEvts2 += v2;//h2->GetBinContent(ibin);
		++ndf;

		double e1 = h1->GetBinError(ibin);
		double e2 = h2->GetBinError(ibin);

		double uncSq = e1*e1 + e2*e2 + 0.5*e1*e2;
				uncSq = 0.5*(v1+v2);
//				uncSq = e1*e1;// + e2*e2;
//				uncSq *= 0.5*0.5;// + e2*e2;

		if (uncSq ==0) continue;

		double localchi = (v1-v2);
//		double localchi = (nEvts1-nEvts2);
		double binchi2 = localchi*localchi/(uncSq);	
	
		if (_debug) std::cout<<"\t"
			<<ibin
			<<"\t"<<h1->GetBinCenter(ibin)*1e3
			<<"\t"<<v1
			<<"\t"<<v2
			<<"\t"<<localchi
			<<"\t"<<uncSq
			<<"\t"<<binchi2

//			<<"\t"<<e1
//			<<"\t"<<e2
			<<std::endl;

		if (v1 < threshold && v2 < threshold) continue;
		sumchi2 += binchi2;

	}
	
	if (_debug) std::cout<<"chi2 = "<<sumchi2<<"\t ndf = "<<ndf<<std::endl;

	return sumchi2;
//	return 5.;
*/
}
//double Chi2Statistic(double v1, double v2, double e1, double e2);

//
// for fucking around
//
double EndpointTools::Chi2TestPlay(TH1F const* h1, TH1F const* h2) {

	int nbinsx = h1->GetNbinsX();
	double threshold = 10;
	
	bool _debug = true;	
	if (_debug) std::cout<<"\t\tnumber of bins: "<<nbinsx
		<<"\n\t\tthreshold: "<<threshold
		<<std::endl;


	double sumchi2 = 0;
	int ndf = 0;

	double nEvts1 = 0;
	double nEvts2 = 0;

	for (int ibin =1; ibin <= nbinsx; ++ibin) {



		double v1 = h1->GetBinContent(ibin);
		double v2 = h2->GetBinContent(ibin);
		nEvts1 += v1;//h1->GetBinContent(ibin);
		nEvts2 += v2;//h2->GetBinContent(ibin);
		++ndf;

		double e1 = h1->GetBinError(ibin);
		double e2 = h2->GetBinError(ibin);

		double uncSq = e1*e1 + e2*e2 + 0.5*e1*e2;
				uncSq = 0.5*(v1+v2);
//				uncSq = e1*e1;// + e2*e2;
//				uncSq *= 0.5*0.5;// + e2*e2;

		if (uncSq ==0) continue;

		double localchi = (v1-v2);
//		double localchi = (nEvts1-nEvts2);
		double binchi2 = localchi*localchi/(uncSq);	
	
		if (_debug) std::cout<<"\t"
			<<ibin
			<<"\t"<<h1->GetBinCenter(ibin)*1e3
			<<"\t"<<v1
			<<"\t"<<v2
			<<"\t"<<localchi
			<<"\t"<<uncSq
			<<"\t"<<binchi2

//			<<"\t"<<e1
//			<<"\t"<<e2
			<<std::endl;

		if (v1 < threshold && v2 < threshold) continue;
		sumchi2 += binchi2;
/*
		double v1 = h1->GetBinContent(ibin);
		double v2 = h2->GetBinContent(ibin);
		if (v1 < threshold || v2 < threshold) continue;
		++ndf;

		double e1 = h1->GetBinError(ibin);
		double e2 = h2->GetBinError(ibin);


		double dv = v1-v2;
		double esq = e1*e1+e2*e2;	
		
		sumchi2 += dv*dv/sqrt(esq);
*/

	}
	
	if (_debug) std::cout<<"chi2 = "<<sumchi2<<"\t ndf = "<<ndf<<std::endl;

	return sumchi2;
//	return 5.;

}
//
// gets the exact same answer as ROOT
//
double EndpointTools::Chi2Test1(TH1F const* h1, TH1F const* h2) {

	int nbinsx = h1->GetNbinsX();
	double threshold = 1;
	
	bool _debug = true;	
	if (_debug) std::cout<<"\t\tnumber of bins: "<<nbinsx
		<<"\n\t\tthreshold: "<<threshold
		<<std::endl;


	double sumchi2 = 0;
	int ndf = 0;
	double N = 0;
	double M = 0;

	for (int ibin =1; ibin <= nbinsx; ++ibin) {

		double v1 = h1->GetBinContent(ibin);
		double v2 = h2->GetBinContent(ibin);
		if (v1 < threshold && v2 < threshold) continue;
		++ndf;
		N += v1;//h1->GetBinContent(ibin);
		M += v2;//h2->GetBinContent(ibin);
	}

	for (int ibin =1; ibin <= nbinsx; ++ibin) {

		double v1 = h1->GetBinContent(ibin);
		double v2 = h2->GetBinContent(ibin);
		if (v1 < threshold && v2 < threshold) continue;
//		if (v1 < threshold || v2 < threshold) continue;
		
		double locchi = (M*v1 - N*v2);	
		sumchi2 += locchi*locchi/(v1+v2);

//		if (v1 < threshold || v2 < threshold) continue;
//		++ndf;
//		N += v1;//h1->GetBinContent(ibin);
//		M += v2;//h2->GetBinContent(ibin);
	}
	
	sumchi2 /= (N*M);
	if (_debug) std::cout<<"chi2 = "<<sumchi2<<"\t ndf = "<<ndf<<std::endl;
	return sumchi2;

/*
	double nEvts1 = 0;
	double nEvts2 = 0;

	for (int ibin =1; ibin <= nbinsx; ++ibin) {



		double v1 = h1->GetBinContent(ibin);
		double v2 = h2->GetBinContent(ibin);
		nEvts1 += v1;//h1->GetBinContent(ibin);
		nEvts2 += v2;//h2->GetBinContent(ibin);
		++ndf;

		double e1 = h1->GetBinError(ibin);
		double e2 = h2->GetBinError(ibin);

		double uncSq = e1*e1 + e2*e2 + 0.5*e1*e2;
				uncSq = 0.5*(v1+v2);
//				uncSq = e1*e1;// + e2*e2;
//				uncSq *= 0.5*0.5;// + e2*e2;

		if (uncSq ==0) continue;

		double localchi = (v1-v2);
//		double localchi = (nEvts1-nEvts2);
		double binchi2 = localchi*localchi/(uncSq);	
	
		if (_debug) std::cout<<"\t"
			<<ibin
			<<"\t"<<h1->GetBinCenter(ibin)*1e3
			<<"\t"<<v1
			<<"\t"<<v2
			<<"\t"<<localchi
			<<"\t"<<uncSq
			<<"\t"<<binchi2

//			<<"\t"<<e1
//			<<"\t"<<e2
			<<std::endl;

		if (v1 < threshold && v2 < threshold) continue;
		sumchi2 += binchi2;

	}
	
	if (_debug) std::cout<<"chi2 = "<<sumchi2<<"\t ndf = "<<ndf<<std::endl;

	return sumchi2;
//	return 5.;
*/
}

#endif
