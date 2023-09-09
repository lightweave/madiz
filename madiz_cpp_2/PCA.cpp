#include <iostream>
#include <opencv2/opencv.hpp>
#include <stdio.h>
#include <vector>
#include <omp.h>
#include <math.h>
#include "util.hpp"
#include "dtypes.h"

float* Cov_matrix(vector<point>& mass_points)
{
    float M_0=0,M_1=0;
    #pragma omp parallel for reduction(+ : M_0) reduction(+ : M_1)
    for (int i=0;i<mass_points.size();i++)
    {
        M_0+=mass_points[i].x;
        M_1+=mass_points[i].y;
    }
    M_0/=mass_points.size()+.0;
    M_1/=mass_points.size()+.0;

    float cov_00=0,cov_11=0,cov_01=0;
    #pragma omp parallel for reduction(+ : cov_00) reduction(+ : cov_11) reduction(+ : cov_01)
    for (int i=0;i<mass_points.size();i++)
    {
        cov_00+=(mass_points[i].x-M_0)*(mass_points[i].x-M_0);
        cov_11+=(mass_points[i].y-M_1)*(mass_points[i].y-M_1);
        cov_01+=(mass_points[i].x-M_0)*(mass_points[i].y-M_1);
    }
    cov_00/=mass_points.size()-1.0;
    cov_01/=mass_points.size()-1.0;
    cov_11/=mass_points.size()-1.0;
    return new float[3]{cov_00,cov_01,cov_11};
}

float* EigenValues(float* matrix)
{
    float D_sqrt = sqrt((matrix[0]-matrix[2])*(matrix[0]-matrix[2]) + 4*matrix[1]*matrix[1]);
    float lamb_1 = (matrix[0] + matrix[2] + D_sqrt) / 2.0;
    float lamb_2 = (matrix[0] + matrix[2] - D_sqrt) / 2.0;

    return new float[2]{lamb_1,lamb_2};
}

float PCA_analyse(vector<point>& mass_points)
{
    float* cov_matrix = Cov_matrix(mass_points);
    float *v_lamb = EigenValues(cov_matrix);
    float ans=(v_lamb[0]<v_lamb[1] ? v_lamb[0]/v_lamb[1] : v_lamb[1]/v_lamb[0]);
    delete cov_matrix;
    delete v_lamb;
    return ans;
}

vector<point> PCA_BFS(Mat &img,point &start, filt &filter,Mat &vizited,unsigned int &sm_br)
{
    vector<point> group,posetit;
    posetit.push_back(start);
    if (filter(pixel(img,start))==1)
    {
        sm_br+=pixel(img,start);
        group.push_back(start);
    }
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
                    if (filter(pixel(img,sl))>0 && pixel(vizited,sl)==0)
                    {
                        spixel(vizited,sl,1);
                        if (filter(pixel(img,sl))==1)
                        {
                            sm_br+=pixel(img,start);
                            group.push_back(sl);
                        }
                        posetit.push_back(sl);
                    }
            }
    }
    return group;
}

tuple<int,int,vector<float>,vector<unsigned int>> count_cloudsPCA(Mimg& img)
{
    static const int c1=117,c2=20;
    int particle=0,treck=0;
    vector<unsigned int> sum_groups_bright;
    vector<float> groups_bright;
    filt filter;
    filter.max=mean(img)+c1;
    filter.min=mean(img)+c2;
    
    Mat vizited = Mat::zeros(img.img.rows,img.img.cols,CV_8U);
    vector<vector<point>> groups;
    point start;
    unsigned int sm_br;
    for (int i = 0; i < img.img.rows; i++) {
        for (int j = 0; j < img.img.cols; j++) {
            if (filter(pixel(img.img,i,j))>0 && pixel(vizited,i,j)==0){
                sm_br=0;
                start=point(i,j);
                spixel(vizited,start,filter(pixel(img.img,start)));
                groups.push_back(PCA_BFS(img.img,start,filter,vizited,sm_br));
                sum_groups_bright.push_back(sm_br);
            }
        }
    }
    groups_bright.resize(groups.size());
    #pragma omp parallel for
    for (int i=0;i<groups.size();i++)
    {
        //cout<<PCA_analyse(groups[i])<<' '<<groups[i].size()<<'\n'; 
        groups_bright[i]=sum_groups_bright[i]/(groups[i].size()+.0);
        if (groups[i].size()>3)
            if (PCA_analyse(groups[i])>0.3)
                particle++;
            else
                treck++;
        else
            particle++;
    }
    return tuple<int,int,vector<float>,vector<unsigned int>>(treck, particle, groups_bright, sum_groups_bright);
}

