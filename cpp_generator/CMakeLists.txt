cmake_minimum_required(VERSION 2.8 FATAL_ERROR)
project( RandomTreeGenerator )

set(CMAKE_CXX_FLAGS "-std=c++11 -Wall -Wextra -Werror"
        CACHE STRING "Flags used by the compiler during all build types." FORCE)

add_executable(RandomTreeGenerator TupleGenerator.cpp)