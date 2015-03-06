#ifndef __EndpointValFit_h_
#define __EndpointValFit_h_
#include "TF1.h"
#include "TH1F.h"

class EndpointValFit {

  private:
 	TF1* _fit;
	double _vmin;
	double _verrParab;

	double errParab(double val);

  public: 
	EndpointValFit();
	
	void fitEndpointPol(TH1F* _hist,bool const dozoom = true);	

	double getEndpoint() { return _vmin;}
	double getErrParab() { return _verrParab;}
	void printEndpoint();
		

};
//
//
//
EndpointValFit::EndpointValFit():_vmin(0),_verrParab(0) {
	_fit = new TF1("evpfit","pol8");
}
//
//
//
void EndpointValFit::fitEndpointPol(TH1F* _hist,bool const dozoom) {
		
	double x1 = _hist->GetXaxis()->GetXmin();
	double x2 = _hist->GetXaxis()->GetXmax();
	_fit->SetRange(x1,x2);

//	_fit->Clear();
//	_fit->SetRange(x1,x2);
//	_hist->Fit("evpfit","bQ");
//	_hist->Fit("evpfit","bQ");
//	_hist->Fit("evpfit","rbQ");
//	_hist->GetFunction("evpfit")->Delete();
//	_hist->RecursiveRemove(_fit);
//	_hist->Fit("evpfit","rbQ");
	_hist->Fit("pol8","bQ");
	_vmin = _fit->GetMinimumX(x1,x2);
	_verrParab = errParab(_vmin);

//	this->printEndpoint();
	if (false) {
		_fit->SetRange(std::max(_vmin - 0.01*_vmin,x1), std::min(x2,_vmin+0.01*_vmin));
		_hist->Fit("evpfit","rbQ");
		_vmin = _fit->GetMinimumX();//x1,x2);
		_verrParab = errParab(_vmin);
//		this->printEndpoint();
	}
	if (dozoom) {
		_fit->SetRange(std::max(_vmin - 10*_verrParab,x1), std::min(x2,_vmin+10*_verrParab));
		_hist->Fit("evpfit","rbQ");
		_vmin = _fit->GetMinimumX();//x1,x2);
		_verrParab = errParab(_vmin);
//		this->printEndpoint();
	}

	_fit = _hist->GetFunction("pol8");
	_fit->SetName("evpfit");

}	
//
//
//
double EndpointValFit::errParab(double val) {
	return sqrt(2./_fit->Derivative2(val));
}
//
//
//
void EndpointValFit::printEndpoint(){
	std::cout<<_vmin<<"\t"<<_verrParab<<" c/TeV"<<std::endl;
}

#endif
