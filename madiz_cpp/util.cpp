#include <iostream>
#include <stdio.h>
#include <vector>
#include <omp.h>
#include "lodepng.h"
#include <libgen.h>
#include <unistd.h>
#include <linux/limits.h>
#include <filesystem>
#include <bits/stdc++.h>
namespace fs = std::filesystem;
using namespace std;
#define uchar unsigned char

struct Mat
{
    unsigned rows,cols;
    vector<vector<uchar>> at;
};

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
    return img.at[i][j];
}

uchar pixel(Mat &img,point &p) //Get mean of pixel brightness values in all chanels
{
    return img.at[p.y][p.x];
}

void spixel(Mat &img,point &p,uchar value)
{
    img.at[p.y][p.x]=value;
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
            img.at[i][j]=(uchar)min(255,(int)(pixel(img,i,j)*factor));
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

Mat zero_Mat(unsigned height, unsigned width)
{
    Mat img;
    img.cols=width;
    img.rows=height;
    img.at=vector<vector<uchar>>(height,vector<uchar>(width,0));
    return img;
}

string get_cur_path(string rpth)
{
    fs::path p = rpth;
    stringstream ss(fs::absolute(p));
    string fl;
    vector<string> pth;
    while (getline(ss, fl, '/')) {
        pth.push_back(fl);
    }pth.push_back(fl);
    for (int i=0;i<pth.size()-1;i++)
    {
        if (pth[i+1]=="..")
        {
            if (i==0)
            {
                throw std::invalid_argument("not valid path");
            }
            pth.erase(pth.begin() + i+1);
            pth.erase(pth.begin() + i);
        }

    }
    fl="";
    for (int i=1;i<pth.size()-1;i++)
    {
        fl+="/"+pth[i];
    }
    return fl;
}

Mat load_gray_image(string pth)
{
    Mat img;
    vector<uchar> pixels;
    cout<<get_cur_path(pth)<<'\n';
    unsigned width, height;
    lodepng::decode(pixels, width, height,get_cur_path(pth));
    cout<<height<<' '<<width<<'\n';
    img=zero_Mat(height,width);
    //#pragma omp parallel for
    for (int y = 0; y < height; y++) {
        //#pragma omp parallel for
        for (int x = 0; x < width; x++) {
            img.at[y][x]=(pixels[(y * width + x)  * 3] + pixels[(y * width + x)  * 3 + 1] + pixels[(y * width + x)  * 3 + 2])/3;
        }
    }
    return img;
}

Mat copy_im(Mat img)
{
    Mat nimg;
    nimg.cols=img.cols;
    nimg.rows=img.rows;
    nimg.at=img.at;
    return nimg;
}