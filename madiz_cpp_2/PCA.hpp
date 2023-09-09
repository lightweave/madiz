#ifndef PCA_hpp__
#define PCA_hpp__

#include <vector>
#include <opencv2/opencv.hpp>
#include "dtypes.h"
using cv::Mat;
using namespace std;

tuple<int,int,vector<float>,vector<unsigned int>> count_cloudsPCA(Mimg& img);

#endif