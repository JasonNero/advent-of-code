cmake_minimum_required(VERSION 3.28)

# Use clang++ and libc++ (must be set before project())
set(CMAKE_CXX_COMPILER clang++-21)

project(cpp20_tour CXX)

# Generate compile_commands.json for clangd
set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

# Set C++20 standard
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -stdlib=libc++ -O2 -Wall")

# Set output directory for executables
set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR})

# C++20 module configuration
set(STD_MODULE_SOURCE /usr/lib/llvm-21/share/libc++/v1/std.cppm)
set(STD_PCM ${CMAKE_BINARY_DIR}/std.pcm)

# Precompile the std module
add_custom_command(
    OUTPUT ${STD_PCM}
    COMMAND ${CMAKE_CXX_COMPILER} -std=c++20 -stdlib=libc++ -O2 -Wall
            -Wno-reserved-module-identifier --precompile
            -o ${STD_PCM} -c ${STD_MODULE_SOURCE}
    DEPENDS ${STD_MODULE_SOURCE}
    COMMENT "Precompiling std module"
)

add_custom_target(std_module ALL DEPENDS ${STD_PCM})

# Find all single .cpp files directly in src/
file(GLOB SINGLE_FILE_SOURCES "src/*.cpp")

# Create executables for single-file programs
foreach(source_file ${SINGLE_FILE_SOURCES})
    get_filename_component(target_name ${source_file} NAME_WE)
    add_executable(${target_name} ${source_file})
    target_compile_options(${target_name} PRIVATE -fmodule-file=std=${STD_PCM})
    add_dependencies(${target_name} std_module)
endforeach()

# Find all subdirectories in src/
file(GLOB SUBDIRS RELATIVE ${CMAKE_SOURCE_DIR}/src ${CMAKE_SOURCE_DIR}/src/*)

# Create executables for multi-file programs in subdirectories
foreach(subdir ${SUBDIRS})
    if(IS_DIRECTORY ${CMAKE_SOURCE_DIR}/src/${subdir})
        file(GLOB subdir_sources "src/${subdir}/*.cpp")
        if(subdir_sources)
            add_executable(${subdir} ${subdir_sources})
            target_include_directories(${subdir} PRIVATE ${CMAKE_SOURCE_DIR}/src/${subdir})
            target_compile_options(${subdir} PRIVATE -fmodule-file=std=${STD_PCM})
            add_dependencies(${subdir} std_module)
        endif()
    endif()
endforeach()
