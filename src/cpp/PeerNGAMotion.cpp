/* ****************************************************************** **
**    OpenSees - Open System for Earthquake Engineering Simulation    **
**          Pacific Earthquake Engineering Research Center            **
**                                                                    **
** ****************************************************************** */
//
// Written: fmk 
// Created: 10/06
//
// Purpose: This file contains the class definition for PeerNGAMotion.
// PeerNGAMotion is a concrete class. A PeerNGAMotion object provides
// a linear time series. the factor is given by the pseudoTime and 
// a constant factor provided in the constructor. 
//


#include <PeerNGAMotion.h>
#include <Vector.h>
#include <math.h>

#include <string.h>
#include <stdio.h>
#include <time.h>
#include <iostream>
#include <fstream>
using std::ifstream;

#include <iomanip>
using std::ios;

//#include <Socket.h>

#ifdef _WIN32
int __cdecl
#else
int
#endif
httpGet(char const *URL, char const *page, unsigned int port, char **dataPtr);





PeerNGAMotion::PeerNGAMotion()	
  : thePath(0), dT(0.0), 
   cFactor(0.0), dbTag1(0), dbTag2(0), lastSendCommitTag(-1)
{
  // does nothing
}

		   
PeerNGAMotion::PeerNGAMotion(int tag,
			     const char *earthquake,
			     const char *station,
			     const char *type,
			     double theFactor)
  : thePath(0), dT(0.0), 
   cFactor(theFactor), dbTag1(0), dbTag2(0), lastSendCommitTag(-1), lastChannel(0)
{
  char peerPage[124];
  char *nextData, *eqData;
  int nPts,i;
  char tmp1[100];
  
  if ((strcmp(type,"ACCEL") == 0) || (strcmp(type,"-accel") == 0) || (strcmp(type,"-ACCEL") == 0)
      || (strcmp(type,"accel") == 0) || (strcmp(type,"ATH") == 0) || (strcmp(type,"-ATH") == 0)) {
    sprintf(peerPage, "/nga_files/ath/%s/%s.AT2",earthquake,station);
  } else if ((strcmp(type,"DISP") == 0) || (strcmp(type,"-disp") == 0) || (strcmp(type,"-DISP") == 0)
      || (strcmp(type,"adisp") == 0) || (strcmp(type,"DTH") == 0) || (strcmp(type,"-DTH") == 0)) {
    std::cerr << "PeerNGAMotion::PeerNGAMotion() - not a valid type:" << type << " (-ACCEL requiured)\n";
  } else {
    std::cerr << "PeerNGAMotion::PeerNGAMotion() - not a valid type:" << type << " (-ACCEL requiured)\n";
    return;
  }

  if (httpGet("peer.berkeley.edu",peerPage,80,&eqData) != 0) {
    if (httpGet("peer.berkeley.edu",peerPage,80,&eqData) != 0) {
      std::cerr << "PeerNGAMotion::PeerNGAMotion() - could not connect to PEER Database, ";
      return; 
    }
  }

  nextData = strstr(eqData,"Page Not Found");
  if (nextData != 0) {
    std::cerr << "PeerNGAMotion::PeerNGAMotion() - could not get Data for record from Database, ";
    std::cerr << "page: " << peerPage << " missing \n";
    free(eqData);
    return;
  }
  
  nextData = strstr(eqData,"NPTS");
  if (nextData == NULL) {
    std::cerr << "PeerNGAMotion::PeerNGAMotion() - could not find nPts in record, send email opensees-support@berkeley.edu";
    free(eqData);
    return;
  }

  nextData+=5; // NPTS=
  nPts = atoi(nextData);
  
  nextData = strstr(eqData, "DT");
  if (nextData == NULL) {
    nextData = strstr(eqData, "dt");
    if (nextData == NULL) {
      std::cerr << "PeerNGAMotion::PeerNGAMotion() - could not find dt in record, send email opensees-support@berkeley.edu";
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
  
  // create copies of the vectors
}



PeerNGAMotion::PeerNGAMotion(int tag,
			     const char *earthquakeStation,
			     const char *type,
			     double theFactor)
  :
   thePath(0), dT(0.0), 
   cFactor(theFactor), dbTag1(0), dbTag2(0), lastSendCommitTag(-1), lastChannel(0)
{
  char  peerPage[124];
  char *nextData, *eqData;
  int nPts,i;


  if ((strcmp(type,"ACCEL") == 0) || (strcmp(type,"-accel") == 0) || (strcmp(type,"-ACCEL") == 0)
      || (strcmp(type,"accel") == 0) || (strcmp(type,"ATH") == 0) || (strcmp(type,"-ATH") == 0)) {
    sprintf(peerPage, "/nga_files/ath/%s.AT2",earthquakeStation);
  } else if ((strcmp(type,"DISP") == 0) || (strcmp(type,"-disp") == 0) || (strcmp(type,"-DISP") == 0)
      || (strcmp(type,"adisp") == 0) || (strcmp(type,"DTH") == 0) || (strcmp(type,"-DTH") == 0)) {
    std::cerr << "PeerNGAMotion::PeerNGAMotion() - not a valid type:" << type << " (-ACCEL requiured)\n";
  } else {
    std::cerr << "PeerNGAMotion::PeerNGAMotion() - not a valid type:" << type << " (-ACCEL requiured)\n";
    return;
  }
  
  if (httpGet("peer.berkeley.edu",peerPage,80,&eqData) != 0) {
    std::cerr << "PeerNGAMotion::PeerNGAMotion() - could not connect to PEER Database, ";
    return; 
  }

  nextData = strstr(eqData,"Page Not Found");
  if (nextData != 0) {
    std::cerr << "PeerNGAMotion::PeerNGAMotion() - could not get Data for record from Database, ";
    std::cerr << "page: " << peerPage << " missing \n";
    free(eqData);
    return;
  }

  nextData = strstr(eqData,"\n"); nextData++;
  nextData = strstr(nextData,"\n"); nextData++;
  nextData = strstr(nextData,"\n"); nextData++;

  nPts = atoi(nextData);
  nextData = strstr(nextData," ");
  dT = strtod(nextData, &nextData);

  nextData = strstr(nextData,"\n"); nextData++;

  thePath = new Vector(nPts);
  //  data = (double *)malloc(nPts*sizeof(double));
  
  for (i=0; i<nPts; i++) {
    double value = strtod(nextData, &nextData);
    (*thePath)(i) = value;
  }

  if (thePath->Size() == 0) {
    delete thePath;
    thePath = 0;
    std::cerr << "PeerNGAMotion - nodata for record from url: " << peerPage << "\n";
  }
    
  free(eqData);
  
  // create copies of the vectors
}

PeerNGAMotion::PeerNGAMotion(int tag,
			     Vector *theDataPoints,
			     double theTimeStep, 
			     double theFactor)
  :
   thePath(0), dT(theTimeStep), 
   cFactor(theFactor), dbTag1(0), dbTag2(0), lastSendCommitTag(-1), lastChannel(0)
{
  if (theDataPoints != 0)
    thePath = new Vector(*theDataPoints);
}


PeerNGAMotion::~PeerNGAMotion()
{
  if (thePath != nullptr)
    delete thePath;
}

double
PeerNGAMotion::getTimeIncr (double pseudoTime)
{
  // NEED TO FILL IN, FOR NOW return 1.0
  return 1.0;
}

double
PeerNGAMotion::getFactor(double pseudoTime)
{
  // check for a quick return
  if (pseudoTime < 0.0 || thePath == 0 || time == 0)
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
PeerNGAMotion::getDuration()
{
  if (thePath == 0)
  {
    std::cerr << "WARNING -- PeerNGAMotion::getDuration() on empty Vector" << "\n";
    return 0.0;
  }
  return (thePath->Size() * dT);
}

double
PeerNGAMotion::getPeakFactor()
{
  if (thePath == 0)
  {
    std::cerr << "WARNING -- PeerNGAMotion::getPeakFactor() on empty Vector" << "\n";
    return 0.0;
  }

  double peak = fabs((*thePath)[0]);
  int num = thePath->Size();
  double temp;
  
  for (int i = 1; i < num; i++)
  {
    temp = fabs((*thePath)[i]);
    if (temp > peak)
      peak = temp;
  }
  
  return (peak*cFactor);
}


double 
PeerNGAMotion::getDt()
{
  return dT;
}
int
PeerNGAMotion::getNPts()
{
  if (thePath == 0)
    return 0;
  else
    return thePath->Size();
}


