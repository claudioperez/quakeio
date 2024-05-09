#include "PeerNGAMotion.h"
#include "elementAPI.h"

void *
OPS_PeerNGAMotion(int argc, const char* argv[])
{
  // Pointer to a uniaxial material that will be returned
  
  int numRemainingArgs = argc;
  
  if (numRemainingArgs < 2) {
    std::cerr << "WARNING: invalid num args PeerNGAMotion <tag?> $eqMotion $factor\n";
    return 0;
  }

  int tag = 0;     // default tag = 0
  double factor = 0.0; 
  int numData   = 0;
  const char *type = "-ACCEL";

  // get tag if provided
  if (numRemainingArgs == 3 || numRemainingArgs == 5 || numRemainingArgs == 7) {
    numData = 1;
    if (OPS_GetIntInput(&numData, &tag) != 0) {
      std::cerr << "WARNING invalid series tag in Constant tag?" << "\n";
      return 0;
    }
    numRemainingArgs -= 1;
  }

  const char *eqMotion = OPS_GetString();

  numData = 1;
  if (OPS_GetDouble(&numData, &factor) != 0) {
    std::cerr << "WARNING invalid shift in peerNGAMotion with tag?" << tag << "\n";
    return 0;
  }
  
  return new PeerNGAMotion(tag, eqMotion, type, factor);
}
