cmake_minimum_required (VERSION 3.8)
if (POLICY CMP0141)
  cmake_policy(SET CMP0141 NEW)
  set(CMAKE_MSVC_DEBUG_INFORMATION_FORMAT "$<IF:$<AND:$<C_COMPILER_ID:MSVC>,$<CXX_COMPILER_ID:MSVC>>,$<$<CONFIG:Debug,RelWithDebInfo>:EditAndContinue>,$<$<CONFIG:Debug,RelWithDebInfo>:ProgramDatabase>>")
endif()
project ("jk")
message(STATUS "test message =${CONAN_BIN_DIRS_ZLIB}")
set(CMAKE_CXX_STANDARD 11)
#set(CMAKE_EXE_LINKER_FLAGS "-static")

#include_directories("../queen")



#file(COPY ../girl/girl.py DESTINATION ${CMAKE_CURRENT_BINARY_DIR})
#file(COPY ../queen/x64/Release/queen.dll DESTINATION ${CMAKE_CURRENT_BINARY_DIR})
#file(COPY ../queen/x64/Release/queen.lib DESTINATION ${CMAKE_CURRENT_BINARY_DIR})
#find_package(PythonLibs REQUIRED)
#include_directories(${PYTHON_INCLUDE_DIRS})


#include_directories(./include/)
#include_directories(./ThostTraderApi/)
#link_directories(./ThostTraderApi/)



add_executable (jk "jk.cpp" "jk.h")
#link_libraries(../lib/c/include)

target_link_libraries(jk ${PYTHON_LIBRARIES}) 
#link_libraries(thostmduserapi_se.dll)
#link_libraries(thosttraderapi_se.dll)

target_link_libraries (jk -static gcc stdc++ winpthread -dynamic)

if (CMAKE_VERSION VERSION_GREATER 3.12)
  set_property(TARGET jk PROPERTY CXX_STANDARD 20)
endif()









