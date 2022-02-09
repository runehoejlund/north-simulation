
#include <bout/physicsmodel.hxx>
#include <smoothing.hxx>
#include <invert_laplace.hxx>
#include <derivs.hxx>
#include <initialprofiles.hxx>
#include "BoutFastOutput/fast_output.hxx"
#include <iostream>
#include <fstream>
#include <list>
#include <string>

class NORTH : public PhysicsModel {
public:
  NORTH();
	
private:
  Field3D n, vort;  // Evolving density and vorticity
  Field3D phi;      // Electrostatic potential
  Field3D source_n; // Density source
  
  std::fstream fs;
  // FastOutput fast_output;

  // Model parameters
  BoutReal kappa;      // Effective gravity
  BoutReal Dvort, Dn;  // Diffusion 
  BoutReal tau_source, tau_sink;
  BoutReal x_pos;
  std::list<int> probe_list;
  std::string datadir, probe_file;
  
  // Poisson brackets: b0 x Grad(f) dot Grad(g) / B = [f, g]
  // Method to use: BRACKET_ARAKAWA, BRACKET_STD or BRACKET_SIMPLE
  BRACKET_METHOD bm; // Bracket method for advection terms
  
  class Laplacian* phiSolver; // Laplacian solver for vort -> phi
  
  int fields(), convective(), diffusive(), source(), sink(), store_probe_data(BoutReal t);
  
  FastOutput fast_output;


protected:
  int init(bool UNUSED(restart));
  int rhs(BoutReal UNUSED(t));
};

NORTH::NORTH(){}

int NORTH::init(bool UNUSED(restart)){
	
    auto& options = Options::root()["north"];
    kappa = options["kappa"].withDefault(1e-3);
    Dvort = options["Dvort"].withDefault(1e-2);
    Dn = options["Dn"].withDefault(1e-2);
    tau_source 	= options["tau_source"].withDefault(1);
    tau_sink 	= options["tau_sink"].withDefault(1);

/*
	// Probes
	std::string datadir = Options::root()["datadir"];
    auto& probes = Options::root()["probes"];
	
	int i = 0;
	while (true) {
		x_pos = probes["x"+std::to_string(i)].withDefault(-1.);
		if (x_pos < 0.){	
		  output.write("\tInculdes %i probes \n", i);
		  break;
		}
		probe_list.push_back(x_pos);
		i++;
	}
	
	probe_file = "./" + datadir + "/probes.out";
	fs.open(probe_file, std::ios::in | std::ios::out | std::ios::app);
	fs << "t";
	for (auto const &i: probe_list) {
		fs  << "\t" << "n[" << i << "]";
	}
	for (auto const &i: probe_list) {
		fs  << "\t" << "phi[" << i << "]";
	}
	fs << "\n";
	fs.close();
*/	
	initial_profile("source_n",  source_n);
	
    SOLVE_FOR(n, vort);
    SAVE_REPEAT(phi);
    SAVE_ONCE(source_n);
	
	/*
	if (fast_output.enabled) {
	  // Add monitor if necessary
		if (fast_output.enable_monitor) {
		  solver->addMonitor(&fast_output);
		}

	  // Add points from the input file
	  int i = 0;
	  BoutReal xpos, ypos, zpos;
	  int ix, iy, iz;
	  Options* fast_output_options = Options::getRoot()->getSection("fast_output");
	  while (true) {
		// Add more points if explicitly set in input file
		fast_output_options->get("xpos"+std::to_string(i), xpos, -1.);
		fast_output_options->get("ypos"+std::to_string(i), ypos, -1.);
		fast_output_options->get("zpos"+std::to_string(i), zpos, -1.);
		if (xpos<0. || ypos<0. || zpos<0.) {
		  output.write("\tAdded %i fast_output points\n", i);
		  break;
		}
		ix = int(xpos*mesh->GlobalNx);
		iy = int(ypos*mesh->GlobalNy);
		iz = int(zpos*mesh->GlobalNz);
		
		// Add fields to be monitored	
		fast_output.add("n"+std::to_string(i), n, ix, iy, iz);
		fast_output.add("phi"+std::to_string(i), phi, ix, iy, iz);
		fast_output.add("vort"+std::to_string(i), vort, ix, iy, iz);
		i++;
	  }
	}
	*/
	
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
    
if (fast_output.enabled) {

  // Add monitor if necessary
    if (fast_output.enable_monitor) {
      solver->addMonitor(&fast_output);
    }

  // Add points from the input file
  int i = 0;
  BoutReal xpos, ypos, zpos;
  int ix, iy, iz;
  Options* fast_output_options = Options::getRoot()->getSection("fast_output");
  while (true) {
    // Add more points if explicitly set in input file
    fast_output_options->get("xpos"+std::to_string(i), xpos, -1.);
    fast_output_options->get("ypos"+std::to_string(i), ypos, -1.);
    fast_output_options->get("zpos"+std::to_string(i), zpos, -1.);
    if (xpos<0. || ypos<0. || zpos<0.) {
      output.write("\tAdded %i fast_output points\n", i);
      break;
    }
    ix = int(xpos*mesh->GlobalNx);
    iy = int(ypos*mesh->GlobalNy);
    iz = int(zpos*mesh->GlobalNz);

    // Add fields to be monitored
    fast_output.add("n"+std::to_string(i), n, ix, iy, iz);
    fast_output.add("phi"+std::to_string(i), phi, ix, iy, iz);
    i++;
  }
}

    return 0;
  }
  
int NORTH::rhs(BoutReal t) {    
	fields();
    convective();     
    diffusive();     
    source();
	sink();

     if (fast_output.enabled){
        fast_output.monitor_method(t); // Store fast output in BOUT.fast.<processor_no.>
    }
	//store_probe_data(t);
    return 0;
}
  
int NORTH::fields() {
	
	ddt(n) = 0;
    ddt(vort) = 0;
  
    return 0;
  }
  
  int NORTH::convective() {
    // Non-stiff, convective part of the problem
    
    // Solve for potential
    phi = phiSolver->solve(vort, phi);
    
    // Communicate variables
    mesh->communicate(n, vort, phi);
	
	// Convective transport
    ddt(n) += -bracket(phi, n, bm) + kappa*(DDZ(n)-n*DDZ(phi));
    ddt(vort) += -bracket(phi, vort, bm) + kappa/n*DDZ(n);
  
    return 0;
  }
  
  int NORTH::diffusive() {
    
	// Communicate variables
    mesh->communicate(n, vort);
	
    // Diffusive transport
    ddt(n) += Dn*Delp2(n);
    ddt(vort) += Dvort*Delp2(vort);
    
	return 0;
  } 
  
  int NORTH::source() {
	
    // Source term
    ddt(n) += source_n/tau_source;
    
	return 0;
  }
	
  int NORTH::sink() {
	/*
	n_tot = 0;
	for (int i = mesh->xstart; i < mesh->xend; ++i) {
		for (int j = mesh->ystart; j < mesh->yend; ++j) {
			for (int k = 0; k < mesh->LocalNz; ++k) {
				n_tot += n(i,j,k);
			}
		}
	}
	n_tot /= n_tot_0;
	tau_sink = 1/n_tot;
    */
	
	// Sink terms
    ddt(n) += -n/tau_sink;
	ddt(vort) += -vort/tau_sink;
    
	return 0;
  }
  
  int NORTH::store_probe_data(BoutReal t) {
	  
	BoutReal j = 0;
	BoutReal k = mesh->LocalNz/2;

	fs.open(probe_file, std::ios::in | std::ios::out | std::ios::app);
	
	fs << t;
	for (auto const &i: probe_list) {
		fs  << "\t" << n(i, j, k);
	}
	for (auto const &i: probe_list) {
		fs  << "\t" << phi(i, j, k);
	}
	fs << "\n";
	fs.close();

	return 0;
  }
  
// Define a main() function
BOUTMAIN(NORTH);
