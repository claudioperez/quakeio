#include <PeerMotion.h>
#include <Vector.h>

#include <math.h>
#include <stdio.h>
#include <string.h>
#include <iostream>
#include <fstream>
using std::ifstream;

#include <iomanip>
using std::ios;

#include "http.h"



#include <elementAPI.h>
#define OPS_Export 

OPS_Export void *
OPS_PeerMotion(void)
{
  // Pointer to a uniaxial material that will be returned
  void *theSeries = 0;
  
  int numRemainingArgs = OPS_GetNumRemainingInputArgs();
  
  if (numRemainingArgs < 4) {
    std::cerr << "WARNING: invalid num args PeerMotion <tag?> $eqMotion $station $type $factor\n";
    return 0;
  }

  int tag = 0;     // default tag = 0
  double factor = 0.0; 
  int numData = 0;

  char *eqMotion = 0;
  char *station = 0;
  char *type = 0;

  // get tag if provided
  if (numRemainingArgs == 5 || numRemainingArgs == 7 || numRemainingArgs == 9) {
    numData = 1;
    if (OPS_GetIntInput(&numData, &tag) != 0) {
      std::cerr << "WARNING invalid series tag in Constant tag?" << "\n";
      return 0;
    }
    numRemainingArgs -= 1;
  }
  
  if ((OPS_GetStringCopy(&eqMotion) != 0) || eqMotion == 0) {
    std::cerr << "WARNING invalid eqMotion for PeerMotion with tag: " << tag << "\n";
    return 0;
  }    

    if ((OPS_GetStringCopy(&station) != 0) || station == 0) {
    std::cerr << "WARNING invalid station for PeerMotion with tag: " << tag << "\n";
    return 0;
  }    

    if ((OPS_GetStringCopy(&type) != 0) || type == 0) {
    std::cerr << "WARNING invalid type  for PeerMotion with tag: " << tag << "\n";
    return 0;
  }    


  if (OPS_GetDouble(&numData, &factor) != 0) {
    std::cerr << "WARNING invalid facor in PeerMotion Series with tag?" << tag << "\n";
    return 0;
  }
  
  theSeries = new PeerMotion(tag, eqMotion, station, type, factor);

  if (theSeries == 0) {
    std::cerr << "WARNING ran out of memory creating PeerMotion with tag: " << tag << "\n";
    return 0;
  }

  delete [] eqMotion;
  delete [] station;
  delete [] type;

  return theSeries;
}




PeerMotion::~PeerMotion()
{
  if (thePath != 0)
    delete thePath;
}


PeerMotion::PeerMotion(int tag,
		       const char *earthquake,
		       const char *station,
		       const char *type,
		       double theFactor)
  ://TimeSeries(tag, TSERIES_TAG_PeerMotion),
   thePath(0), dT(0.0), 
   cFactor(theFactor), dbTag1(0), dbTag2(0), lastSendCommitTag(-1), lastChannel(0)
{
  char peerPage[124];
  char *nextData, *eqData;
  int nPts,i;
  char tmp1[100];

  if (earthquake != 0 && station != 0 && type != 0) {
    
    if ((strcmp(type,"ACCEL") == 0) || (strcmp(type,"-accel") == 0) || (strcmp(type,"-ACCEL") == 0)
	|| (strcmp(type,"accel") == 0) || (strcmp(type,"ATH") == 0) || (strcmp(type,"-ATH") == 0)) {
      sprintf(peerPage, "/smcat/data/ath/%s/%s.AT2",earthquake,station);
    } else if ((strcmp(type,"DISP") == 0) || (strcmp(type,"-disp") == 0) || (strcmp(type,"-DISP") == 0)
	       || (strcmp(type,"adisp") == 0) || (strcmp(type,"DTH") == 0) || (strcmp(type,"-DTH") == 0)) {
      sprintf(peerPage, "/smcat/data/dth/%s/%s.DT2",earthquake,station);
    } else {
      std::cerr << "PeerMotion::PeerMotion() - not a valid type:" << type << " (-DISP or -ACCEL requiured)\n";
      return;
    }

    if (httpGet("peer.berkeley.edu", peerPage, 80, &eqData) != 0) {
      std::cerr << "PeerMotion::PeerMotion() - could not connect to PEER Database, ";
      return; 
    }

    if (eqData == 0) {
      std::cerr << "PeerMotion::PeerMotion() - NO data returned ";
      return; 
    }

    nextData = strstr(eqData, "Page Not Found");
    if (nextData != 0) {
      std::cerr << "PeerMotion::PeerMotion() - could not get Data for record from Database, ";
      std::cerr << "page: " << peerPage << " missing \n";
      free(eqData);
      return;
    }

    nextData = strstr(eqData,"NPTS");
    if (nextData == NULL) {
      std::cerr << "PeerMotion::PeerMotion() - could not find nPts in record, send email opensees-support@berkeley.edu";
      free(eqData);
      return;
    }

    nextData+=5; // NPTS=
    nPts = atoi(nextData);

    nextData = strstr(eqData, "DT");
    if (nextData == NULL) {
      nextData = strstr(eqData, "dt");
      if (nextData == NULL) {
	std::cerr << "PeerMotion::PeerMotion() - could not find dt in record, send email opensees-support@berkeley.edu";
	free(eqData);
	return;
      }
    }

    nextData+=4; //DT= dT UNIT
    dT = strtod(nextData, &nextData);
    
    sscanf(nextData, "%s", tmp1);
    nextData += strlen(tmp1)+1;
    
    sscanf(nextData, "%s", tmp1);

    thePath = new Vector(nPts);
    //  data = (double *)malloc(nPts*sizeof(double));

    for (i=0; i<nPts; i++) {
      double value = strtod(nextData, &nextData);
      (*thePath)(i) = value;
    }
    
    free(eqData);
  }
}


PeerMotion::PeerMotion(int tag,
		       Vector *theDataPoints,
		       double theTimeStep, 
		       double theFactor)
  ://TimeSeries(tag, TSERIES_TAG_PeerMotion),
   thePath(0), dT(theTimeStep), 
   cFactor(theFactor), dbTag1(0), dbTag2(0), lastSendCommitTag(-1), lastChannel(0)
{
  if (theDataPoints != 0)
    thePath = new Vector(*theDataPoints);
}


double
PeerMotion::getTimeIncr (double pseudoTime)
{
  // NEED TO FILL IN, FOR NOW return 1.0
  return 1.0;
}

double
PeerMotion::getFactor(double pseudoTime)
{
  // check for a quick return
  if (pseudoTime < 0.0 || thePath == 0)
    return 0.0;

  // determine indexes into the data array whose boundary holds the time
  double incr = pseudoTime/dT; 
  int incr1 = floor(incr);
  int incr2 = incr1+1;

  if (incr2 >= thePath->Size())
    return 0.0;

  double value1 = (*thePath)[incr1];
  double value2 = (*thePath)[incr2];
  return cFactor*(value1 + (value2-value1)*(pseudoTime/dT - incr1));
}

double
PeerMotion::getDuration()
{
  if (thePath == 0)
  {
    std::cerr << "WARNING -- PeerMotion::getDuration() on empty Vector" << "\n";
	return 0.0;
  }
  return (thePath->Size() * dT);
}

double
PeerMotion::getPeakFactor()
{
  if (thePath == 0) {
    std::cerr << "WARNING -- PeerMotion::getPeakFactor() on empty Vector" << "\n";
    return 0.0;
  }

  double peak = fabs((*thePath)[0]);
  int num = thePath->Size();
  double temp;
  
  for (int i = 1; i < num; i++) {
    temp = fabs((*thePath)[i]);
    if (temp > peak)
      peak = temp;
  }
  
  return (peak*cFactor);
}


double 
PeerMotion::getDt()
{
  return dT;
}
int
PeerMotion::getNPts()
{
  if (thePath == 0)
    return 0;
  else
    return thePath->Size();
}


void
PeerMotion::Print(OPS_Stream &s, int flag)
{
    s << "Path Time Series: constant factor: " << cFactor;
    s << " dT: " << dT << "\n";
    if (flag == 1 && thePath != 0) {
      s << " specified path: " << *thePath;

    }
}
