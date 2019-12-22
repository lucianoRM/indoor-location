cmake_minimum_required(VERSION 3.14)
project(list C)

set(CMAKE_C_STANDARD 99)

add_library(list_lib STATIC list.c)
install(TARGETS list_lib DESTINATION lib)
install(FILES list.h DESTINATION include)

add_executable(list main.c)
target_link_libraries(list list_lib)