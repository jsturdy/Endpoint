#ifndef __Format_h_
#define __Format_h_

typedef struct {
	float k;
	float eta;
	float phi;
	float ptErr;

	std::string static contents() { return "k/F:eta:phi:ptErr";}

} _OutType;

typedef struct {

	int seed;
	float trueVal;
	float measVal;
	float measErr;

} _PullInfo;


#endif

