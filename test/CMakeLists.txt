set (BELADY_RESOURCES
    src/main.cc
)

add_executable(belady ${BELADY_RESOURCES})
target_include_directories(belady PUBLIC ${BELADY_INCLUDE_DIR})


install(TARGETS belady DESTINATION ${CMAKE_CURRENT_SOURCE_DIR}/bin)

enable_testing()
if (BASH_PROGRAM)
    add_test(NAME TestBelady.TestEndToEnd COMMAND ${BASH_PROGRAM} ${CMAKE_CURRENT_SOURCE_DIR}/test.sh "$<TARGET_FILE:belady>" ${CMAKE_CURRENT_SOURCE_DIR})
endif()