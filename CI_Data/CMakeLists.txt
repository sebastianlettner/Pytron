cmake_minimum_required(VERSION 3.8)
project(CI)

set(CMAKE_C_STANDARD 99)
set(CMAKE_VERBOSE_MAKEFILE on)

set (CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra")
set(SOURCE_FILES main.c HW1/helloworld.h HW1/multiby2.h HW1/bubbleSort.h HW1/InsertionSort.h HW1/MergeSort.h)
add_executable(CI ${SOURCE_FILES})

