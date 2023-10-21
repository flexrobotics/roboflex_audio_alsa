cmake_minimum_required(VERSION 3.25)

project(roboflex_audio_alsa VERSION 0.1.1 DESCRIPTION "roboflex audio sensor using ALSA")

# specify the C++ standard
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED True)


# -------------------- 
# Resolve dependencies

# Advanced Linux Sound Architecture (ALSA)
find_package(ALSA REQUIRED)                                    

# Locate the installed roboflex_core and its dependencies (a few)
# find_package(roboflex_core REQUIRED)

include(FetchContent)

# download and build pybind11
FetchContent_Declare(roboflex_core
    GIT_REPOSITORY https://github.com/flexrobotics/roboflex.git
    GIT_TAG        main
)
FetchContent_MakeAvailable(roboflex_core)


# -------------------- 
# Define the library

add_library(roboflex_audio_alsa STATIC
    src/audio_alsa.cpp
    include/roboflex_audio_alsa/audio_alsa.h
)

# Set some properties on our library
set_property(TARGET roboflex_audio_alsa PROPERTY 
    POSITION_INDEPENDENT_CODE ON
)

# Include directories when we compile our library
target_include_directories(roboflex_audio_alsa PUBLIC 
    $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include> 
    $<INSTALL_INTERFACE:include>
    ${ALSA_INCLUDE_DIRS}
    #${roboflex_core_INCLUDE_DIRS}
)

# Link against the necessary libraries
target_link_libraries(roboflex_audio_alsa PUBLIC 
    ${ALSA_LIBRARIES}
    roboflex_core

    # Unfortunately, we need to link against all these libraries
    # because they are used by roboflex_core. Urgh, someone help.
    flatbuffers_util 
    xtensor 
    xsimd 
    xtl
    Eigen3::Eigen
)


# -------------------- 
# install

# If you need to install the roboflex_audio_alsa library
install(TARGETS roboflex_audio_alsa 
    LIBRARY DESTINATION lib
    ARCHIVE DESTINATION lib
    RUNTIME DESTINATION bin
    INCLUDES DESTINATION include
)

install(DIRECTORY include/roboflex_audio_alsa
    DESTINATION include
)


# --------------------
# build python bindings

add_subdirectory(python)
