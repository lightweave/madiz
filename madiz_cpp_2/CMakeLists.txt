cmake_minimum_required(VERSION 2.8)
project( MADIZ )
set(CMAKE_CXX_STANDARD 17)

FIND_PACKAGE( OpenMP)
      if(OPENMP_FOUND)
         message("OPENMP FOUND")
         set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} ${OpenMP_C_FLAGS}")
         set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} ${OpenMP_CXX_FLAGS}")
         set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} ${OpenMP_EXE_LINKER_FLAGS}")
      endif()
     include_directories(SYSTEM ${OpenMP_INCLUDE_PATH})
find_package( OpenCV REQUIRED )
   if(!OPENCV_FOUND)
         message(ERROR "OPENCV NOT FOUND")
    endif()


add_compile_options(-O2 -Ofast -fopenmp )
add_compile_options(-Wl,--as-needed -lfoo)

include_directories( ${OpenCV_INCLUDE_DIRS} )
add_executable( MADIZ MADIZ.cpp serv.cpp util.cpp obr.cpp PCA.cpp)
target_link_libraries( MADIZ  opencv_core opencv_imgproc opencv_imgcodecs)# ${OpenCV_LIBS}

