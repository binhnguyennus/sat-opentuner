# Generated by CMake 2.8.7

IF("${CMAKE_MAJOR_VERSION}.${CMAKE_MINOR_VERSION}" LESS 2.5)
   MESSAGE(FATAL_ERROR "CMake >= 2.6.0 required")
ENDIF("${CMAKE_MAJOR_VERSION}.${CMAKE_MINOR_VERSION}" LESS 2.5)
CMAKE_POLICY(PUSH)
CMAKE_POLICY(VERSION 2.6)
#----------------------------------------------------------------
# Generated CMake target import file.
#----------------------------------------------------------------

# Commands may need to know the format version.
SET(CMAKE_IMPORT_FILE_VERSION 1)

# Create imported target libcryptominisat4
ADD_LIBRARY(libcryptominisat4 STATIC IMPORTED)

# Create imported target cryptominisat
ADD_EXECUTABLE(cryptominisat IMPORTED)

# Import target "libcryptominisat4" for configuration "Release"
SET_PROPERTY(TARGET libcryptominisat4 APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
SET_TARGET_PROPERTIES(libcryptominisat4 PROPERTIES
  IMPORTED_LINK_INTERFACE_LANGUAGES_RELEASE "CXX"
  IMPORTED_LINK_INTERFACE_LIBRARIES_RELEASE "m4ri"
  IMPORTED_LOCATION_RELEASE "/home1/02055/marijn/code/automate/807a4fc3c822294bdd4c30e57d98a6a3/binary/lib/libcryptominisat4.a"
  )

# Import target "cryptominisat" for configuration "Release"
SET_PROPERTY(TARGET cryptominisat APPEND PROPERTY IMPORTED_CONFIGURATIONS RELEASE)
SET_TARGET_PROPERTIES(cryptominisat PROPERTIES
  IMPORTED_LOCATION_RELEASE "/home1/02055/marijn/code/automate/807a4fc3c822294bdd4c30e57d98a6a3/binary/cryptominisat"
  )

# Commands beyond this point should not need to know the version.
SET(CMAKE_IMPORT_FILE_VERSION)
CMAKE_POLICY(POP)
