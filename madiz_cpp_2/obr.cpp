#include <iostream>
#include <opencv2/opencv.hpp>
#include <stdio.h>
#include <vector>
#include <omp.h>
#include <math.h>
#include "util.hpp"
#include "dtypes.h"
#include "serv.hpp"
using cv::Mat;
using cv::Size;
using namespace std;


bool is_overexposed(Mimg &img)
{
    int treshold=100;
    return mean(img)>treshold;
}

vector<point> get_groupBFS(Mat &img,point &start, float &factor,Mat &vizited)
{
    vector<point> group,posetit;
    posetit.push_back(start);
    group.push_back(start);
    point tk;
    while (!posetit.empty())
    {
        tk=posetit[posetit.size()-1];
        posetit.pop_back();
        for (int dy=-1;dy<2;dy++)
            for (int dx=-1;dx<2;dx++)
            {
                point sl=tk+point(dy,dx);
                if (sl.x>=0 && sl.y>=0 && sl.x<img.cols && sl.y<img.rows)
                    if (pixel(img,sl)>factor && pixel(vizited,sl)==0)
                    {
                        spixel(vizited,sl,1);
                        group.push_back(sl);
                        posetit.push_back(sl);
                    }
            }
    }
    return group;
}

int count_groups(Mimg &img,float &factor)
{

    Mat vizited = Mat::zeros(img.img.rows,img.img.cols,CV_8U);
    vector<vector<point>> groups;
    point start;
    for (int i = 0; i < img.img.rows; i++) {
        for (int j = 0; j < img.img.cols; j++) {
            if (pixel(img.img,i,j)>factor && pixel(vizited,i,j)==0){
                    start=point(i,j);
                    spixel(vizited,start,1);
                    groups.push_back(get_groupBFS(img.img,start,factor,vizited));
            }
        }
    }

    return groups.size();
}