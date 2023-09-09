#include <iostream>
#include <opencv2/opencv.hpp>
#include <stdio.h>
#include <vector>
#include <omp.h>
#include "dtypes.h"
using cv::Mat;
using namespace std;

uchar pixel(Mat &img,int &i,int &j) //Get mean of pixel brightness values in all chanels
{
    return img.at<uchar>(i,j);
}

uchar pixel(Mat &img,point &p) //Get mean of pixel brightness values in all chanels
{
    return img.at<uchar>(p.y,p.x);
}

void spixel(Mat &img,point &p,uchar value)
{
    img.at<uchar>(p.y,p.x)=value;
}

float mean(Mimg &img, float doff=0.0) //mean of brightness
{
    float mean_intensity = img.sm / (img.img.cols*img.img.rows - doff);
    return mean_intensity;
}

void EnchanceBrightness(Mat &img,float factor)
{
    #pragma omp parallel for// num_threads(10)
    for (int i = 0; i < img.rows; i++) {
        #pragma omp parallel for //num_threads(10)
        for (int j = 0; j < img.cols; j++) {
            img.at<uchar>(i,j)=(uchar)min(255,(int)(pixel(img,i,j)*factor));
        }
    }
}

vector<uchar> filter_pixels(Mat &img, float factor)
{
    vector<uchar> res;
    uchar k;
    for (int i = 0; i < img.rows; i++) {
        for (int j = 0; j < img.cols; j++) {
            k=pixel(img,i,j);
            if (k>=factor)
                res.push_back(k);
        }
    }
    return res;
}