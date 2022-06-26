#ifndef __TOROIDALBCS_CXX__
#define __TOROIDALBCS_CXX__

#include "../include/toroidalBCs.hxx"
#include <string>

/*!
 * \brief Constructor
 *
 * Constructor which sets the private member data
 *
 * \warning firstUpperYGhost and firstLowerGhost
 *          should only be used for the processors using the respective
 *          boundaries
 */
ToroidalBCs::ToroidalBCs() {
  // yend = index value of last inner point on this processor
  firstUpperYGhost = mesh->yend + 1;
  // ystart = index value of first inner point on this processor
  firstLowerYGhost = mesh->ystart - 1;
}

// Member functions
/*!
 * Sets the inner x ghost points of a Field3D in toroidal coordinates.
 *
 * \param[in] f The original field
 * \param[out] f The field after setting the inner boundary
 *
 * ## Idea:
 * We assume continuity for diametrically opposite points on the boundary
 * at r = 0.
 * The innermost ghost points in x (x_index = 0), closest to the boundary)
 * will be set to the value of the innermost internal point (meaning all
 * points excluding the ghost points) which lies \f$\theta + \pi\f$ away
 * (modulus $2 \pi$). The next ghost point (x_index = 1) will be set to the
 * value of the second innermost internal point which lies \f$\theta + \pi\f$
 * away, and so on.
 *
 * This means that the index of the point diametrically opposite to the
 * current ghost point will be on the form
 *
 * ~~~{.cpp}
 * corresponding_xIndex = 2 * mesh->xstart - (current_ghost_x_index + 1)
 * corresponding_zIndex = (current_ghost_zIndex + mesh->LocalNz/2) % (mesh->LocalNz)
 * ~~~
 *
 * where `x` is the radius, \f$\r\f$, and z is azimuthal angle, \f$\theta\f$.
 *
 * \sa applyCenterBCLoop
 *
 * \note We are also setting the inner x-y corner points
 */
void ToroidalBCs::applyCenterBC(Field3D &f) {
  if (mesh->firstX()) {
    // Set the boundary for the inner y points
    applyCenterBCLoop(f, mesh->ystart, mesh->yend);
    // Do the same for the ghost points in y
    if (mesh->firstY()) {
      applyCenterBCLoop(f, 0, firstLowerYGhost);
    }
    if (mesh->lastY()) {
      // Note that LocalNy starts counting from 1
      applyCenterBCLoop(f, firstUpperYGhost, mesh->LocalNy - 1);
    }
  }
}

// Auxiliary
/*!
 * The actual loops which sets the ghost points for inner \f$\r\f$
 *
 * \param[in] f The field to loop over
 * \param[in] yStart The start (inclusive) of the y index we are looping over
 * \param[in] yEnd The end (inclusive) of the y index we are looping over
 *
 * \param[out] f The field which has the inner boundaries set
 *
 * \sa applyCenterBC
 */
void ToroidalBCs::applyCenterBCLoop(Field3D &f, const int &yStart,
                                  const int &yEnd) {
  // Loop through all X and Y and all Z-points on the processor
  for (int xInd = 0; xInd < mesh->xstart; xInd++) {
    for (int yInd = yStart; yInd <= yEnd; yInd++) {
      for (int zInd = 0; zInd < mesh->LocalNz; zInd++) {
        // Set the value on the ghost point
        f(xInd, yInd, zInd) =
            f(2 * mesh->xstart - (xInd + 1), yInd, (zInd + (mesh->LocalNz / 2))%(mesh->LocalNz));
      }
    }
  }
}

#endif

