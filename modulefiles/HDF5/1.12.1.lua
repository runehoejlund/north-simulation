help([[
Description
===========
HDF5 is a data model, library, and file format for storing and managing data.
 It supports an unlimited variety of datatypes, and is designed for flexible
 and efficient I/O and for high volume and complex data.


More information
================
 - Homepage: https://portal.hdfgroup.org/display/support
]])
whatis("Description: HDF5 is a data model, library, and file format for storing and managing data."..
 " It supports an unlimited variety of datatypes, and is designed for flexible"..
 "and efficient I/O and for high volume and complex data.")
whatis("Homepage: https://portal.hdfgroup.org/display/support")
whatis("URL: https://portal.hdfgroup.org/display/support")
conflict("HDF5")
prepend_path("CMAKE_PREFIX_PATH","~/local/modules/software/HDF5/1.12.1")
prepend_path("CPATH","~/local/modules/software/HDF5/1.12.1/include")
prepend_path("LD_LIBRARY_PATH","~/local/modules/software/HDF5/1.12.1/lib")
prepend_path("LIBRARY_PATH","~/local/modules/software/HDF5/1.12.1/lib")
prepend_path("PATH","~/local/modules/software/HDF5/1.12.1/bin")
prepend_path("PKG_CONFIG_PATH","~/local/modules/software/HDF5/1.12.1/lib/pkgconfig")
prepend_path("XDG_DATA_DIRS","~/local/modules/software/HDF5/1.12.1/share")
-- setenv("EBROOTHDF5","~/local/modules/software/HDF5/1.12.1")
-- setenv("EBVERSIONHDF5","1.10.7")
-- setenv("EBDEVELHDF5","~/local/modules/software/HDF5/1.12.1/easybuild/HDF5-1.10.7-iimpi-2020b-easybuild-devel")
setenv("HDF5_DIR","~/local/modules/software/HDF5/1.12.1")