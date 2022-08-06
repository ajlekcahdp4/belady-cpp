cmake_minimum_required(VERSION 3.23)

project (belady)

set (BELADY_INCLUDE_DIR ${CMAKE_CURRENT_SOURCE_DIR}/include)
set (CMAKE_CXX_COMPILER clang++)

find_program(BASH_PROGRAM bash)

add_subdirectory(test)