#ifndef util_hpp__
#define util_hpp__

#include <vector>
#include "dtypes.h"
#include <opencv2/opencv.hpp>
using cv::Mat;
using namespace std;

uchar pixel(Mat &img,int &i,int &j);

uchar pixel(Mat &img,point &p);

void spixel(Mat &img,point &p,uchar value);

float mean(Mimg &img, float doff=0.0);

void EnchanceBrightness(Mat &img,float factor);

vector<uchar> filter_pixels(Mat &img, float factor);

#endif