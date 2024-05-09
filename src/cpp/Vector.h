/* ****************************************************************** **
**    OpenSees - Open System for Earthquake Engineering Simulation    **
**          Pacific Earthquake Engineering Research Center            **
**                                                                    **
** ****************************************************************** */
//
// Written: fmk 
// Created: 11/96
//
// Description: This file contains the class definition for Vector.
// Vector is a concrete class implementing the vector abstraction.

#ifndef Vector_h
#define Vector_h 


class Vector
{
  public:
    // constructors and destructor
    Vector();
    Vector(int);
    Vector(const Vector &);    
#if !defined(NO_CXX11_MOVE)
    Vector(Vector &&);    
#endif

    Vector(double *data, int size);
    ~Vector();

    // utility methods
    int setData(double *newData, int size);
    double Norm(void) const;
    double pNorm(int p) const;
    inline int Size(void) const;
    int resize(int newSize);
    inline void Zero(void);
    int Normalize(void);
    
    int addVector(const Vector &other, double factOther);
    int addVector(double factThis, const Vector &other, double factOther);

    // overloaded operators
    inline double operator()(int x) const;
    inline double &operator()(int x);
    double operator[](int x) const;  // these two operator do bounds checks
    double &operator[](int x);
    Vector &operator=(const Vector  &V);
#if !defined(NO_CXX11_MOVE)   
    Vector &operator=(Vector  &&V);
#endif
    Vector &operator+=(double fact);
    Vector &operator-=(double fact);
    Vector &operator*=(double fact);
    Vector &operator/=(double fact); 

    Vector operator+(double fact) const;
    Vector operator-(double fact) const;
    Vector operator*(double fact) const;
    Vector operator/(double fact) const;
    
    Vector &operator+=(const Vector &V);
    Vector &operator-=(const Vector &V);
    
    Vector operator+(const Vector &V) const;
    Vector operator-(const Vector &V) const;
    double operator^(const Vector &V) const;

    int operator==(const Vector &V) const;
    int operator==(double) const;
    int operator!=(const Vector &V) const;
    int operator!=(double) const;


    // methods added by Remo
    int  Assemble(const Vector &V, int init_row, double fact = 1.0);
    int  Extract (const Vector &V, int init_row, double fact = 1.0); 
  
    // friend istream &operator>>(istream &s, Vector &V);    
    friend Vector operator*(double a, const Vector &V);
    
  private:
    int sz;
    double *theData;
    int fromFree;
//  static double VECTOR_NOT_VALID_ENTRY;
};


/********* INLINED VECTOR FUNCTIONS ***********/
inline int 
Vector::Size(void) const 
{
  return sz;
}


inline void
Vector::Zero(void){
  for (int i=0; i<sz; i++) theData[i] = 0.0;
}


inline double 
Vector::operator()(int x) const
{
#ifdef _G3DEBUG
  // check if it is inside range [0,sz-1]
  if (x < 0 || x >= sz) {
      opserr << "Vector::(loc) - loc " << x << " outside range [0, " << sz-1 << endln;
      return VECTOR_NOT_VALID_ENTRY;
  }
#endif

  return theData[x];
}


inline double &
Vector::operator()(int x)
{
#ifdef _G3DEBUG
  // check if it is inside range [0,sz-1]
  if (x < 0 || x >= sz) {
      opserr << "Vector::(loc) - loc " << x << " outside range [0, " << sz-1 << endln;
      return VECTOR_NOT_VALID_ENTRY;
  }
#endif
  
  return theData[x];
}


#endif

