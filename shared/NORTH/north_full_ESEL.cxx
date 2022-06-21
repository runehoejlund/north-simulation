#include <bout/physicsmodel.hxx>
#include <smoothing.hxx>
#include <invert_laplace.hxx>
#include <derivs.hxx>
#include <initialprofiles.hxx>
#include "BoutFastOutput/fast_output.hxx"
#include "./utils/include/cylindricalBCs.hxx"
#include <bout/constants.hxx> // Gives PI and TWOPI

class NORTH : public PhysicsModel {
  public:
    NORTH();
    
  private:
    Field3D n, vort, T;  // Evolving density, vorticity and electron temperature
    Field3D phi;      // Electrostatic potential
    Field3D source_n, source_T, sink_T, wall_shadow; // Density source, Temperature source

    // Model parameters
    BoutReal kappa;      // Effective gravity
    BoutReal Dvort, Dn, DT;  // Diffusion 
    BoutReal tau_source, tau_sink_vort, tau_wall_n, tau_wall_T, tau_wall_vort; // Characteristic times
    
    CylindricalBCs cylBCs; // Class containing methods which sets the ghost points at singularity (rho=0)

    // Method to use: BRACKET_ARAKAWA, BRACKET_STD or BRACKET_SIMPLE
    BRACKET_METHOD bm; // Bracket method for advection terms
    
    class Laplacian* phiSolver; // Laplacian solver for vort -> phi
    
    int fields(), interchange(), diffusive(), source(), sink(), curvature();
    Field3D C(const Field3D &f);
    
    // Create object from FastOutput class
    FastOutput fast_output;

  protected:
    int init(bool UNUSED(restart));
    int rhs(BoutReal UNUSED(t));
};

NORTH::NORTH(){}

int NORTH::init(bool UNUSED(restart)) {
  auto& options = Options::root()["north"];
  kappa = options["kappa"].withDefault(1.0e-3);

  Dvort = options["Dvort"].withDefault(1.0e-2);
  Dn = options["Dn"].withDefault(1.0e-2);
  DT = options["DT"].withDefault(1.0e-2);

  tau_source 	= options["tau_source"].withDefault(1.0);
  tau_sink_vort 	= options["tau_sink_vort"].withDefault(1.0);
  tau_wall_n = options["tau_wall_n"].withDefault(1.0);
  tau_wall_T = options["tau_wall_T"].withDefault(1.0);
  tau_wall_vort = options["tau_wall_vort"].withDefault(1.0);


	initial_profile("source_n",  source_n);
  initial_profile("source_T",  source_T);
  initial_profile("sink_T",  sink_T);
  initial_profile("wall_shadow",  wall_shadow);
	
  SOLVE_FOR(T, vort, n);
  SAVE_REPEAT(phi);
  SAVE_ONCE(source_n, source_T, sink_T, wall_shadow);

  phiSolver = Laplacian::create();
  phi = 0.; // Starting phi
  
  // Choose method to use for Poisson bracket advection terms
  switch(options["bracket"].withDefault(0)) {
  case 0: {
    bm = BRACKET_STD; 
    output << "\tBrackets: default differencing\n";
    break;
  }
  case 1: {
    bm = BRACKET_SIMPLE; 
    output << "\tBrackets: simplified operator\n";
    break;
  }
  case 2: {
    bm = BRACKET_ARAKAWA; 
    output << "\tBrackets: Arakawa scheme\n";
    break;
  }
  case 3: {
    bm = BRACKET_CTU; 
    output << "\tBrackets: Corner Transport Upwind method\n";
    break;
  }
  default:
    output << "ERROR: Invalid choice of bracket method. Must be 0 - 3\n";
    return 1;
  }


  // Write fast output
  if (fast_output.enabled) {
    // Add monitor if necessary
    if (fast_output.enable_monitor) {
      solver->addMonitor(&fast_output);
    }

    // Add points from the input file
    int i = 0;
    Options* fast_output_options = Options::getRoot()->getSection("fast_output");
    while (true) {
      BoutReal xprobe;
      int ix, iy, iz;

      // Add more points if explicitly set in input file
      fast_output_options->get("xprobe"+std::to_string(i), xprobe, -1.);
      if (xprobe<0.) {
        output.write("\tAdded %i fast_output points\n", i);
        break;
      }
      ix = int(xprobe*mesh->GlobalNx);
      iy = 0;
      iz = 0;

      // Add fields to be monitored
      fast_output.add("n"+std::to_string(i), n, ix, iy, iz);
      fast_output.add("T"+std::to_string(i), T, ix, iy, iz);
      fast_output.add("phi"+std::to_string(i), phi, ix, iy, iz);
      i++;
    }
  }

  return 0;
}
  
int NORTH::rhs(BoutReal t) {
  // Treat singularity at rho = 0
  cylBCs.innerRhoCylinder(n);
  cylBCs.innerRhoCylinder(T);
  cylBCs.innerRhoCylinder(vort);
  cylBCs.innerRhoCylinder(phi);

	fields();
  interchange();     
  diffusive();     
  source();
	sink();
  curvature();
  if (fast_output.enabled){
      fast_output.monitor_method(t); // Store fast output in BOUT.fast.<processor_no.>
  }
  return 0;
}
  
int NORTH::fields() {
	ddt(n) = 0;
  ddt(T) = 0;
  ddt(vort) = 0;
  return 0;
}
  
int NORTH::interchange() {
  // Solve for potential
  phi = phiSolver->solve(vort, phi);
  
  // Communicate variables
  mesh->communicate(n, vort, phi, T);

  // Convective transport
  ddt(n) += -bracket(phi, n, bm) ;
  ddt(T) += -bracket(phi, T, bm) ;
  ddt(vort) += -bracket(phi, vort, bm) ;
  return 0;
}

int NORTH::diffusive() {
  // Communicate variables
  mesh->communicate(n, vort, T);

  // Diffusive transport
  ddt(n) += Dn*Delp2(n);
  ddt(T) += DT*Delp2(T);
  ddt(vort) += Dvort*Delp2(vort);
  return 0;
} 

int NORTH::source() {
  // Source term
  ddt(n) += source_n/tau_source;
  ddt(T) += source_T/tau_source;
  
  return 0;
}

int NORTH::sink() {	
  // Sink terms
  mesh->communicate(n, vort, T);
  ddt(n) += -n*wall_shadow/tau_wall_n;
  ddt(T) += -T*wall_shadow/tau_wall_T;
  ddt(vort) += -vort/tau_sink_vort-vort*wall_shadow/tau_wall_vort;
  
  return 0;
}

int NORTH::curvature() {	
  // curvature terms
  mesh->communicate(n, vort, T, phi);
  ddt(n) += (C(n*T)-n*C(phi));
  ddt(T) += -2/3*T*C(phi) + 7/3*T*C(T) + 2/3*pow(T,2)/n*C(n);
  ddt(vort) += C(n*T);
  return 0;
}

Field3D NORTH::C(const Field3D &f) {
  Vector3D zhat; // vertical unit vector (z-hat in toroidal coordinates)
  zhat.covariant = false;
  zhat.x = 1.0;
  zhat.y = 0.0;
  zhat.z = PI/2.0;

  return kappa*V_dot_Grad(zhat, f);
  
 return 0*f;
}

// Define a main() function
BOUTMAIN(NORTH);
