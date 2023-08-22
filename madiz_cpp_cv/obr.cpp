#include <iostream>
#include <opencv2/opencv.hpp>
#include <stdio.h>
#include <vector>
#include <omp.h>
#include "util.hpp"
#include "serv.hpp"
using cv::Mat;
using cv::Size;
using namespace std;


bool is_overexposed(Mat &img)
{
    int treshold=100;
    float mean_intensity=mean(img);
    return mean_intensity>treshold;
}


tuple<float, vector<uchar>,vector<uchar>> count_pixels(Mat &img, int &cst, bool fixed=false)
{
    float averange;
    if (fixed)
        averange = 80;
    else
        averange = mean(img)+cst;

    vector<uchar> pixel_brightness=filter_pixels(img,averange);

    EnchanceBrightness(img,255);

    resize(img,img,Size(img.cols/99,img.rows/99));

    EnchanceBrightness(img,80);
    vector<uchar> group_brightness=filter_pixels(img,mean(img)+cst);

    return tuple<float,vector<uchar>,vector<uchar>>(averange, pixel_brightness, group_brightness);
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
/*
point* sld(Mat &img,point start,int dy, int dx, float &factor,Mat &vizited,vector<point> &group)
{
    point sl=start+point(dy,dx);
    if (sl.x>=0 && sl.y>=0 && sl.x<img.cols && sl.y<img.rows)
        if (pixel(img,sl)>factor && pixel(vizited,sl)==0)
        {
            spixel(vizited,sl,1);
            group.push_back(sl);
            point *p=new point;
            *p=sl;
            return p;
        }
    return nullptr;
}

void get_groupDFSa(Mat &img,point* start, float &factor,Mat &vizited,vector<point> &group)
{

    if (start==nullptr) return;
    group.push_back(*start);
//    #pragma omp parallel for
    for (int dy=-1;dy<2;dy++)
//        #pragma omp parallel for
        for (int dx=-1;dx<2;dx++)
        {
            get_groupDFSa(img,sld(img,*start,dy,dx,factor,vizited,group),factor,vizited,group);
        }
}

vector<point> get_groupDFS(Mat &img,point start, float &factor,Mat &vizited)
{
    vector<point> group;
    get_groupDFSa(img,&start,factor,vizited,group);
    return group;
}*/

int count_groups(Mat &img,float &factor)
{

    Mat vizited = Mat::zeros(img.rows,img.cols,CV_8U);
    vector<vector<point>> groups;
    point start;
    for (int i = 0; i < img.rows; i++) {
        for (int j = 0; j < img.cols; j++) {
            if (pixel(img,i,j)>factor && pixel(vizited,i,j)==0){
                    start=point(i,j);
                    spixel(vizited,start,1);
                    groups.push_back(get_groupBFS(img,start,factor,vizited));
            }
        }
    }

    return groups.size();
}