#ifndef __CosmicEndpointFitter_h_
#define __CosmicEndpointFitter_h_

#include <iostream>
#include <vector>

#include "TFile.h"
#include "TH1F.h"
#include "TF1.h"
#include "TH2F.h"
#include "TH3F.h"
#include "TBranch.h"
#include "TLeaf.h"
#include "TTree.h"
#include "TNtuple.h"
#include "TCanvas.h"
#include "TStyle.h"
#include "TRoot.h"
#include "TMath.h"
#include "TRandom3.h"


bool _testMode 	= false;
int const _nBinsBias  = 400;                   // stepping precision

//
// Track info
//
typedef struct {
	int valid;
    int charge;
    float pt;
    float eta;
    float phi;

	float chisquare;
	int ndf;

	float dxy;
	float dz;
	float vx;
	float vy;
	float vz;

	float ptErr;
	float etaErr;
	float phiErr;
	float dxyErr;
	
	float trackProbability;

} _TrackInfo;


//
// muon information
//
typedef struct {
    int charge;
	int isTrackerMuon;
	int isGlobalMuon;
	int isStandAloneMuon;

	int numTrackerHits;
	int numLostTrackerHits;
	int numLostTrackerHitsInner;
	int numLostTrackerHitsOuter;
	int numSegmentMatches;
	int numPixelHits;
	int numMuonHits;
	int numValidHitsDT;
	int numValidHitsCSC;
	int numValidHitsRPC;
    float pt;
    float eta;
    float phi;
    float sumPt;
    float sumEtECAL;
    float sumEtHCAL;

	float drTrig9;
	float drTrig11;
	float drTrig15;
	float normalizedChi2;

	int firstLayer;
	int firstDetId;
	int firstSubdetId;

} _MuonInfo;
#endif
