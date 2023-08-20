#ifndef util_hpp__
#define util_hpp__

#include <vector>
#include <opencv2/opencv.hpp>
using cv::Mat;
using namespace std;


class point
{
    public:
    int x,y;
    point(int &ys,int &xs)
    {
        x=xs;
        y=ys;
    }
    point()
    {
        x=0;y=0;
    }
    point operator+(point const &obj)
    {
        point res;
        res.x=x+obj.x;
        res.y=y+obj.y;
        return res;
    }
};

uchar pixel(Mat &img,int &i,int &j);

uchar pixel(Mat &img,point &p);

void spixel(Mat &img,point &p,uchar value);

float mean(Mat &img);

void EnchanceBrightness(Mat &img,float factor);

vector<uchar> filter_pixels(Mat &img, float factor);

#endif