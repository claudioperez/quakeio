/* ****************************************************************** **
**    OpenSees - Open System for Earthquake Engineering Simulation    **
**          Pacific Earthquake Engineering Research Center            **
** ****************************************************************** */
//
#ifndef PeerNGAMotion_h
#define PeerNGAMotion_h
#include <iostream>
#ifndef OPS_Stream
#  define OPS_Stream std::ostream
#endif

// Written: fmk 
// Created: 10/06
//
// Description: This file contains the class definition for PeerNGAMotion.
// PeerNGAMotion is a TimeSeries class which obtains the reference points from
// the Peer Strong Motion Database, interpolates the load factor using 
// these specified control points and the time. The dT for the control
// points is obtained from the Peer Database.

// object. The control points are obtained from the peer strong motion database
//

class Vector;

class PeerNGAMotion // : public TimeSeries
{
  public:
    // constructors  
  PeerNGAMotion(int tag,
		const char *earthquake,
		const char *station,
		const char *type,
		double cfactor = 1.0);

  PeerNGAMotion(int tag,
		const char *earthquakeStation,
		const char *station,
		double cfactor = 1.0);

  PeerNGAMotion();    
    
  // destructor    
  ~PeerNGAMotion();

  // method to get factor
  double getFactor(double pseudoTime);
  double getDuration ();
  double getPeakFactor ();
  double getTimeIncr (double pseudoTime);
  double getDt();
  int getNPts();
  
  void Print(OPS_Stream &s, int flag =0);    
  
 protected:
  PeerNGAMotion(int tag,
		Vector *thePath,
		double dT, 
		double cFactor);
  
 private:
  Vector *thePath;      // vector containing the data points
  double dT;
  int currentTimeLoc;   // current location in time
  double cFactor;       // additional factor on the returned load factor
  int dbTag1, dbTag2;   // additional database tags needed for vector objects
  int lastSendCommitTag;
  int otherDbTag;       // a database tag needed for the vector object   
  
  void *lastChannel;
};

#endif
