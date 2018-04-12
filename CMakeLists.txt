##~---------------------------------------------------------------------------##
##                     _______  _______  _______  _     _                     ##
##                    |   _   ||       ||       || | _ | |                    ##
##                    |  |_|  ||       ||   _   || || || |                    ##
##                    |       ||       ||  | |  ||       |                    ##
##                    |       ||      _||  |_|  ||       |                    ##
##                    |   _   ||     |_ |       ||   _   |                    ##
##                    |__| |__||_______||_______||__| |__|                    ##
##                             www.amazingcow.com                             ##
##  File      : CMakeLists.txt                                                ##
##  Project   : COWTODO                                                       ##
##  Date      : April 11, 2018                                                ##
##  License   : GPLv3                                                         ##
##  Author    : n2omatt <n2omatt@amazingcow.com>                              ##
##  Copyright : AmazingCow - 2018                                             ##
##                                                                            ##
##  Description :                                                             ##
##                                                                            ##
##---------------------------------------------------------------------------~##

cmake_minimum_required(VERSION 3.5)

##----------------------------------------------------------------------------##
## Project                                                                    ##
##----------------------------------------------------------------------------##
set(PROJECT cowtodo)
project(${PROJECT})


##----------------------------------------------------------------------------##
## Sources                                                                    ##
##----------------------------------------------------------------------------##
set(SOURCES 
    src/main.cpp
    src/ExcludeDirsRC.cpp
    src/Logger.cpp
)


##----------------------------------------------------------------------------##
## Libraries                                                                  ##
##----------------------------------------------------------------------------##
##------------------------------------------------------------------------------
## Defines
add_definitions(-DCOREDIR_UNDEF_WINDOWS_DECLARATIONS=1)


##------------------------------------------------------------------------------
## Libs.
add_subdirectory(libs/acow_algo         )
add_subdirectory(libs/acow_c_goodies    )
add_subdirectory(libs/acow_cpp_goodies  )
add_subdirectory(libs/acow_posix_goodies)
add_subdirectory(libs/CMD               )
add_subdirectory(libs/CoreAssert        )
add_subdirectory(libs/CoreDir           )
add_subdirectory(libs/CoreFile          )
add_subdirectory(libs/CoreFS            )
add_subdirectory(libs/CoreLog           )
add_subdirectory(libs/CoreString        )
add_subdirectory(libs/libtermcolor      )


##----------------------------------------------------------------------------##
## Executable                                                                 ##
##----------------------------------------------------------------------------##
##------------------------------------------------------------------------------
## Executable.
add_executable(${PROJECT} ${SOURCES})

##------------------------------------------------------------------------------
## Dependencies
target_link_libraries(${PROJECT} LINK_PUBLIC acow_algo         )
target_link_libraries(${PROJECT} LINK_PUBLIC acow_c_goodies    )
target_link_libraries(${PROJECT} LINK_PUBLIC acow_cpp_goodies  )
target_link_libraries(${PROJECT} LINK_PUBLIC acow_posix_goodies)
target_link_libraries(${PROJECT} LINK_PUBLIC CMD               )
target_link_libraries(${PROJECT} LINK_PUBLIC CoreAssert        )
target_link_libraries(${PROJECT} LINK_PUBLIC CoreDir           )
target_link_libraries(${PROJECT} LINK_PUBLIC CoreFile          )
target_link_libraries(${PROJECT} LINK_PUBLIC CoreFS            )
target_link_libraries(${PROJECT} LINK_PUBLIC CoreLog           )
target_link_libraries(${PROJECT} LINK_PUBLIC CoreString        )
target_link_libraries(${PROJECT} LINK_PUBLIC libtermcolor      )


##----------------------------------------------------------------------------##
## Install                                                                    ##
##----------------------------------------------------------------------------##
install(TARGETS ${PROJECT} RUNTIME DESTINATION ${CMAKE_INSTALL_PREFIX})