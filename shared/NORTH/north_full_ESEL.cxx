#include <bout/physicsmodel.hxx>
#include <smoothing.hxx>
#include <invert_laplace.hxx>
#include <derivs.hxx>
#include <initialprofiles.hxx>
#include "BoutFastOutput/fast_output.hxx"
#include "./dependencies/utils/include/toroidalBCs.hxx"
#include <bout/constants.hxx> // Gives PI and TWOPI

class NORTH : public PhysicsModel {
  public:
    NORTH();
    
  private:
    Field3D n, vort, T;  // Evolving density, vorticity and electron temperature
    Field3D phi, B;      // Electrostatic potential and B-field
    Field3D source_T, wall_shadow, bracket_prefactor, cos_z_over_x, sin_z_field; // Density source, Temperature source
    Field3D S_n, S_T, S_w; // Volume source/sink terms
	  Field3D n_bck, T_bck;

    // Model parameters
    BoutReal kappa;           // Effective gravity
    BoutReal n_n;             // Neutral density
    BoutReal E_ion;           // Ionization energy   
    
    BoutReal rho_s;           // Ion larmor radius
    BoutReal oci;             // Ion cyclotron frequency
    BoutReal n0;              // Reference density

	  bool recombination, ionization;

    BoutReal Dvort, Dn, nu_ea, k_ei, rho_Le, DT;   // Diffusion 
    BoutReal tau_source, tau_wall_n, tau_wall_T; // Characteristic times
    
    ToroidalBCs toroidalBCs; // Class containing methods which sets the ghost points at singularity (r=0)

    // Method to use: BRACKET_ARAKAWA, BRACKET_STD or BRACKET_SIMPLE
    BRACKET_METHOD bm; // Bracket method for advection terms
    
    class Laplacian* phiSolver; // Laplacian solver for vort -> phi
    
    int fields(), interchange(), diffusive(), source(), sink(), curvature();
    Field3D C(const Field3D &f);
    Field3D k_ionization(const Field3D &f);
    Field3D k_recombination(const Field3D &f);
    
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

  n_n = options["n_n"].withDefault(1.0e3);
  E_ion = options["E_ion"].withDefault(2.0);
  rho_s = options["rho_s"].withDefault(1.0e3);
  oci = options["oci"].withDefault(2.0);
  n0 = options["n0"].withDefault(1.0e16);

  Dvort = options["Dvort"].withDefault(1.0e-2);
  Dn = options["Dn"].withDefault(1.0e-2); // Deprecated
  k_ei = options["k_ei"].withDefault(1.05e-6);
  nu_ea = options["nu_ea"].withDefault(0.1103);
  rho_Le = options["rho_Le"].withDefault(85.6);
  DT = options["DT"].withDefault(1.0e-2);

  std::cout << "\n************* This run is with ***************\n";
  std::cout << "\n New Diffusion Coefficients. Only neutral-electron collisions. My BCs. \n";
  std::cout << nu_ea * pow(rho_Le, 2);

  tau_source 	= options["tau_source"].withDefault(1.0);
  tau_wall_n = options["tau_wall_n"].withDefault(1.0);
  tau_wall_T = options["tau_wall_T"].withDefault(1.0);
  
  recombination = options["recombination"].withDefault(true);
  ionization = options["ionization"].withDefault(true);
  
  n_bck = options["n_bck"].withDefault(1.0e-2);
  T_bck = options["T_bck"].withDefault(1.0e-2);
  
  initial_profile("B", B);
  initial_profile("source_T",  source_T);
  initial_profile("wall_shadow",  wall_shadow);
  
  initial_profile("bracket_prefactor",  bracket_prefactor);
  initial_profile("cos_z_over_x",  cos_z_over_x);
  initial_profile("sin_z_field",  sin_z_field);

  SOLVE_FOR(T, vort, n);
  SAVE_REPEAT(phi);
  SAVE_ONCE(B, source_T, wall_shadow, bracket_prefactor, cos_z_over_x, sin_z_field);

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
    BoutReal xprobe;
    Options* fast_output_options = Options::getRoot()->getSection("fast_output");
    while (true) {
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
  // Treat singularity at r = 0
  toroidalBCs.applyCenterBC(n);
  toroidalBCs.applyCenterBC(T);
  toroidalBCs.applyCenterBC(vort);
  toroidalBCs.applyCenterBC(phi);

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
  ddt(n) += -bracket_prefactor * bracket(phi, n, bm) ;
  ddt(T) += -bracket_prefactor * bracket(phi, T, bm) ;
  ddt(vort) += -bracket_prefactor * bracket(phi, vort, bm) ;
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

int NORTH::diffusive() {
  // Communicate variables
  mesh->communicate(n, vort, T);

  // Diffusive transport
  // ddt(n) += k_ei * pow(rho_Le, 2) * Div(n * Grad_perp(n)); // Diffusion from ion-electron collisions
  // ddt(n) += k_ei * pow(rho_Le, 2) * n * Delp2(n); // Diffusion from ion-electron collisions
  ddt(n) += nu_ea * pow(rho_Le, 2) * Delp2(n); // Diffusion from electron-atom collisions
  // ddt(n) += Dn*Delp2(n); // Deprecated
  ddt(T) += DT*Delp2(T);
  ddt(vort) += Dvort*Delp2(vort);
  return 0;
} 

int NORTH::source() {
  // Volumen source term
  S_n = 0;
  S_T = 0;
  
  if (ionization){
	S_n += n_n*n*k_ionization(T);
	S_T -= (E_ion+T)*n_n*k_ionization(T);
  }

  if(recombination){
	S_n -= n*n*k_recombination(T);
  }
  
  S_w = - n_n * k_ionization(T) * ((n/B) * vort + Grad_perp(phi) * Grad(n/B));
  
  ddt(n) += S_n;
  ddt(T) += S_T;
  ddt(vort) += S_w;
  
  ddt(T) += source_T/(tau_source*n); // Heating source
  
  return 0;
}

int NORTH::sink() {	
  // Sink terms
  mesh->communicate(n, vort, T);
  
  ddt(n) -= (n-n_bck)*wall_shadow/tau_wall_n;
  ddt(T) -= (T-T_bck)*wall_shadow/tau_wall_T;
  
  return 0;
}

Field3D NORTH::C(const Field3D &f) {
  return 2.0*kappa*(sin_z_field*DDX(f) + cos_z_over_x*DDZ(f));
}

Field3D NORTH::k_ionization(const Field3D &f) {
  //return 2.0e-13*pow(f/E_ion, 0.5)/(6.0 + f/E_ion)*exp(-E_ion/f)/(pow(rho_s,2)*c_s);
  return 2.0e-13*pow(f/E_ion, 0.5)/(6.0 + f/E_ion)*exp(-E_ion/f)*n0/(oci);
  //return 0*f;
}

Field3D NORTH::k_recombination(const Field3D &f) {
  return 7.0e-20*pow(E_ion/f, 0.5)*n0/(oci);
}

/*
Field3D NORTH::max_n(const Field3D &f) {
  if (f>0.05){
    return f;
  }
  else{
    return f;
  }
}*/

// Define a main() function
BOUTMAIN(NORTH);
