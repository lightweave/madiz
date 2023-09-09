#ifndef obr_hpp__
#define obr_hpp__

#include "dtypes.h"
#include <vector>
#include <opencv2/opencv.hpp>
using cv::Mat;
using namespace std;

bool is_overexposed(Mimg &img);

//vector<point> get_groupBFS(Mat &img,point &start, float &factor,Mat &vizited);

int count_groups(Mimg &img,float &factor);

#endif