cmake_minimum_required(VERSION 3.14)
project(json_test C)

set(CMAKE_C_STANDARD 90)

add_library(cjson STATIC cJSON.c)
install(TARGETS cjson DESTINATION lib)
install(FILES cJSON.h DESTINATION include)

add_library(list STATIC list.c)
install(TARGETS list DESTINATION lib)
install(FILES list.h DESTINATION include)

add_executable(json_test main.c location_system.c)
target_link_libraries(json_test cjson)
target_link_libraries(json_test m)
install(TARGETS json_test DESTINATION bin)