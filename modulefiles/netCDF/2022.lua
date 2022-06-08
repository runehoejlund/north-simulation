help([[
For detailed instructions, go to:
    https://www.unidata.ucar.edu/software/netcdf/
]])
whatis("NetCDF-C Version: 4.8.1. NetCDF-C++ Version: 4.3.1")
whatis("Keywords: netcdf, c, c++, bout")
whatis("Description: NetCDF (network Common Data Form) is a set of software libraries"..
 "and machine-independent data formats that support the creation, access, and sharing of array-oriented"..
 "scientific data."..
 "The latest versions of NetCDF have separated out the C++ API from the main C library."..
 "This is both the C and the C++ API.")
whatis("Homepage: https://www.unidata.ucar.edu/software/netcdf/")
whatis("URL: https://www.unidata.ucar.edu/software/netcdf/")
conflict("netCDF")

prepend_path("CMAKE_PREFIX_PATH","~/local/modules/software/netCDF")
prepend_path("CPATH","~/local/modules/software/netCDF/include")
prepend_path("LD_LIBRARY_PATH","~/local/modules/software/netCDF/lib")
prepend_path("LIBRARY_PATH","~/local/modules/software/netCDF/lib")
prepend_path("MANPATH","~/local/modules/software/netCDF/share/man")
prepend_path("PATH","~/local/modules/software/netCDF/bin")
prepend_path("PKG_CONFIG_PATH","~/local/modules/software/netCDF/lib/pkgconfig")
prepend_path("XDG_DATA_DIRS","~/local/modules/software/netCDF/share")