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

float mean(Mat &img) //mean of brightness
{
    int sum_pix_val=0;
    #pragma omp parallel for reduction(+ : sum_pix_val)
    for (int i = 0; i < img.rows; i++) {
        #pragma omp parallel for reduction(+ : sum_pix_val)
        for (int j = 0; j < img.cols; j++) {
            sum_pix_val+=pixel(img,i,j);
        }
    }
    float mean_intensity = sum_pix_val / (img.cols*img.rows + .0);
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