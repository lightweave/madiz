#ifndef obr_hpp__
#define obr_hpp__

#include <vector>
#include <opencv2/opencv.hpp>
#include "util.hpp"
using cv::Mat;
using namespace std;

bool is_overexposed(Mat &img);

tuple<float, vector<uchar>,vector<uchar>> count_pixels(Mat &img, int &cst, bool fixed=false);

vector<point> get_groupBFS(Mat &img,point &start, float &factor,Mat &vizited);

int count_groups(Mat &img,float &factor);

#endif