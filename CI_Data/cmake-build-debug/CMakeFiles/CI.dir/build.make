# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.8

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Remove some rules from gmake that .SUFFIXES does not remove.
SUFFIXES =

.SUFFIXES: .hpux_make_needs_suffix_list


# Produce verbose output by default.
VERBOSE = 1

# Suppress display of executed commands.
$(VERBOSE).SILENT:


# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /Applications/CLion.app/Contents/bin/cmake/bin/cmake

# The command to remove a file.
RM = /Applications/CLion.app/Contents/bin/cmake/bin/cmake -E remove -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = "/Users/sebastianlettner/Google Drive/5.Semester WS 17-18 /CI_Data"

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = "/Users/sebastianlettner/Google Drive/5.Semester WS 17-18 /CI_Data/cmake-build-debug"

# Include any dependencies generated for this target.
include CMakeFiles/CI.dir/depend.make

# Include the progress variables for this target.
include CMakeFiles/CI.dir/progress.make

# Include the compile flags for this target's objects.
include CMakeFiles/CI.dir/flags.make

CMakeFiles/CI.dir/main.c.o: CMakeFiles/CI.dir/flags.make
CMakeFiles/CI.dir/main.c.o: ../main.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir="/Users/sebastianlettner/Google Drive/5.Semester WS 17-18 /CI_Data/cmake-build-debug/CMakeFiles" --progress-num=$(CMAKE_PROGRESS_1) "Building C object CMakeFiles/CI.dir/main.c.o"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/CI.dir/main.c.o   -c "/Users/sebastianlettner/Google Drive/5.Semester WS 17-18 /CI_Data/main.c"

CMakeFiles/CI.dir/main.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/CI.dir/main.c.i"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E "/Users/sebastianlettner/Google Drive/5.Semester WS 17-18 /CI_Data/main.c" > CMakeFiles/CI.dir/main.c.i

CMakeFiles/CI.dir/main.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/CI.dir/main.c.s"
	/Applications/Xcode.app/Contents/Developer/Toolchains/XcodeDefault.xctoolchain/usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S "/Users/sebastianlettner/Google Drive/5.Semester WS 17-18 /CI_Data/main.c" -o CMakeFiles/CI.dir/main.c.s

CMakeFiles/CI.dir/main.c.o.requires:

.PHONY : CMakeFiles/CI.dir/main.c.o.requires

CMakeFiles/CI.dir/main.c.o.provides: CMakeFiles/CI.dir/main.c.o.requires
	$(MAKE) -f CMakeFiles/CI.dir/build.make CMakeFiles/CI.dir/main.c.o.provides.build
.PHONY : CMakeFiles/CI.dir/main.c.o.provides

CMakeFiles/CI.dir/main.c.o.provides.build: CMakeFiles/CI.dir/main.c.o


# Object files for target CI
CI_OBJECTS = \
"CMakeFiles/CI.dir/main.c.o"

# External object files for target CI
CI_EXTERNAL_OBJECTS =

CI: CMakeFiles/CI.dir/main.c.o
CI: CMakeFiles/CI.dir/build.make
CI: CMakeFiles/CI.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir="/Users/sebastianlettner/Google Drive/5.Semester WS 17-18 /CI_Data/cmake-build-debug/CMakeFiles" --progress-num=$(CMAKE_PROGRESS_2) "Linking C executable CI"
	$(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/CI.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
CMakeFiles/CI.dir/build: CI

.PHONY : CMakeFiles/CI.dir/build

CMakeFiles/CI.dir/requires: CMakeFiles/CI.dir/main.c.o.requires

.PHONY : CMakeFiles/CI.dir/requires

CMakeFiles/CI.dir/clean:
	$(CMAKE_COMMAND) -P CMakeFiles/CI.dir/cmake_clean.cmake
.PHONY : CMakeFiles/CI.dir/clean

CMakeFiles/CI.dir/depend:
	cd "/Users/sebastianlettner/Google Drive/5.Semester WS 17-18 /CI_Data/cmake-build-debug" && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" "/Users/sebastianlettner/Google Drive/5.Semester WS 17-18 /CI_Data" "/Users/sebastianlettner/Google Drive/5.Semester WS 17-18 /CI_Data" "/Users/sebastianlettner/Google Drive/5.Semester WS 17-18 /CI_Data/cmake-build-debug" "/Users/sebastianlettner/Google Drive/5.Semester WS 17-18 /CI_Data/cmake-build-debug" "/Users/sebastianlettner/Google Drive/5.Semester WS 17-18 /CI_Data/cmake-build-debug/CMakeFiles/CI.dir/DependInfo.cmake" --color=$(COLOR)
.PHONY : CMakeFiles/CI.dir/depend

