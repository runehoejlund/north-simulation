#ifndef __TOROIDALBCS_H__
#define __TOROIDALBCS_H__

#include <bout.hxx>           // Includes all necessary classes and types
#include <string>

/*!
 * \class ToroidalBCs
 *
 * \brief Class which has member functions to set ghost points in toroidal geometry
 *
 * Class for proper treatment of singularity
 * in toroidal coordinates at center: r = 0.
 * The code is almost one-to-one taken from the
 * OwnBCs-class from the CELMA-project:
 * https://celma-project.github.io/
 * by Michael Løiten, DTU Physics, 2017.
 * 
 * However, we (Asbjørn CLod Pedersen and
 * Rune Højlund, DTU Physics, 2022)
 * have made a small change such that
 * we use the modulus operator to
 * match the Z-indexes. Also our class is
 * simpler, since we don't need all the
 * functionality from the original implementation.
 **************************************************************************
 * Original credit to Michael Løiten, DTU Physics, 2017
 *
 * Adaptation by Asbjørn Clod Pedersen, Rune Højlund,
 * Technical University of Denmark, 2022
 *
 * \date 2022.19.06
 */
class ToroidalBCs {
private:
  // Data members
  int piIndex;          //!< Index corresponding to \f$\pi\f$
  int firstUpperYGhost; //!< Given that the processor has a boundary
  int firstLowerYGhost; //!< Given that the processor has a boundary

  // Member functions
  //! A function which loops over the inner boundary
  void applyCenterBCLoop(Field3D &the_field, const int &y_start,
                            const int &y_end);
  BoutReal x; //!< The value of x at the current index
  BoutReal z; //!< The value of z at the current index
public:
  // Constructors
  ToroidalBCs();

  // Destructors
  // Not needed as we have no dynamic memory allocation yet

  // Member functions
  //! Specify ghost at inner \f$\r\f$
  void applyCenterBC(Field3D &the_field);
};

// Function bodies of the non-inlined functions are located in the .cxx file
#include "../src/toroidalBCs.cxx"

#endif

