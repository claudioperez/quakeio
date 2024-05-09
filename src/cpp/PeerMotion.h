/* ****************************************************************** **
**    OpenSees - Open System for Earthquake Engineering Simulation    **
**          Pacific Earthquake Engineering Research Center            **
**                                                                    **
** ****************************************************************** */
//
#ifndef PeerMotion_h
#define PeerMotion_h


#include <iostream>
#ifndef OPS_Stream
#  define OPS_Stream std::ostream
#endif
//
// Description: This file contains the class definition for PeerMotion.
// PeerMotion is a TimeSeries class which obtains the reference points from
// the Peer Strong Motion Database, interpolates the load factor using 
// these specified control points and the time. The dT for the control
// points is obtained from the Peer Database.

// object. The control points are obtained from the peer strong motion database
//
// Written: fmk 
// Created: 10/06
//

class Vector;

class PeerMotion
{
  public:
   // constructors  
   PeerMotion(int tag,
	     const char *earthquake,
	     const char *station,
	     const char *responseType,
	     double cfactor = 1.0);

  PeerMotion();    
    
  // destructor    
  ~PeerMotion();

  
  // method to get factor
    double getFactor(double pseudoTime);
    double getDuration ();
    double getPeakFactor ();
    double getTimeIncr (double pseudoTime);
    double getDt();
    int getNPts();
 
    void Print(OPS_Stream &s, int flag =0);    
    
 protected:
   PeerMotion(int tag,
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

