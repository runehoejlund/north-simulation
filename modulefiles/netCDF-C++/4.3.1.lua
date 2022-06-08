help([[
For detailed instructions, go to:
    https://docs.unidata.ucar.edu/netcdf-cxx/current/
]])
whatis("Version: 4.3.1")
whatis("Keywords: netcdf, c++, bout")
whatis("URL: https://www.unidata.ucar.edu/software/netcdf/")
whatis("Description: NetCDF (Network Common Data Form) is a set of software libraries and machine-independent data formats that support the creation, access, and sharing of array-oriented scientific data. The latest versions of NetCDF have separated out the C++ API from the main C library. This is the C++ API.")

prepend_path("LD_LIBRARY_PATH","~/local/lib")
prepend_path("LIBRARY_PATH","~/local/lib")
prepend_path("PATH","~/local/bin")