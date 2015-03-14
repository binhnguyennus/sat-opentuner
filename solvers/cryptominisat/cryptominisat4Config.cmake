# Config file for the Build-tree CryptoMiniSat Package
# It defines the following variables
#  CRYPTOMINISAT4_INCLUDE_DIRS - include directories for cryptominisat4
#  CRYPTOMINISAT4_LIBRARIES    - libraries to link against
#  CRYPTOMINISAT4_EXECUTABLE   - the cryptominisat executable

# Compute paths
get_filename_component(CRYPTOMINISAT4_CMAKE_DIR "${CMAKE_CURRENT_LIST_FILE}" PATH)
set(CRYPTOMINISAT4_INCLUDE_DIRS "/home1/02055/marijn/code/automate/807a4fc3c822294bdd4c30e57d98a6a3/binary/include")

# Our library dependencies (contains definitions for IMPORTED targets)
include("${CRYPTOMINISAT4_CMAKE_DIR}/cryptominisat4Targets.cmake")

# These are IMPORTED targets created by cryptominisat4Targets.cmake
set(CRYPTOMINISAT4_LIBRARIES libcryptominisat4)
set(CRYPTOMINISAT4_EXECUTABLE cryptominisat4)
