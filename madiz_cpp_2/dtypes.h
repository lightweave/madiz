#ifndef dtypes_hpp__
#define dtypes_hpp__

#include <iostream>
#include <opencv2/opencv.hpp>
#include <stdio.h>
#include <vector>
#include <omp.h>
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

class Mimg
{
    public:
    unsigned long sm;
    Mat img;
    Mimg(Mat &in_img, bool pre_mean=true)
    {
        img=in_img.clone();
        sm=0;
        if (pre_mean)
            sm=sum_img(img);
    }
    /*Mimg clone()
    {
        Mimg nimg=Mimg(img,false);
        sm=sm;
        return nimg;
    }*/
    unsigned long sum_img(Mat &img)
    {
        unsigned long sum_pix_val=0;
        #pragma omp parallel for reduction(+ : sum_pix_val)
        for (int i = 0; i < img.rows; i++) {
            #pragma omp parallel for reduction(+ : sum_pix_val)
            for (int j = 0; j < img.cols; j++) {
                sum_pix_val+=img.at<uchar>(i,j);
            }
        }
        return sum_pix_val;
    }
};


struct filt
{
    float max,min;
    uchar operator()(uchar a) const {
        if (a<min) return 0;
        if (a<max) return 2;
        return 1;
    }
};

#endif