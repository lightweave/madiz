#include "obr.hpp"
#include "serv.hpp"
#include <omp.h>
#include <iostream>
#include <vector>
#include <opencv2/opencv.hpp>
#include <stdio.h>
#include <string>
#define str to_string
using cv::Mat;
using cv::COLOR_RGB2GRAY;
using cv::imread;
using namespace std;


void scan(Mat &image,vector<string>&s,vector<int> &csts, vector<bool> &fxs,int i)
{
    Mat imgs;
    float averange;
    vector<uchar> pixel_brightness, group_brightness;
    imgs=image.clone();
    tie(averange, pixel_brightness, group_brightness)=count_pixels(imgs,csts[i],fxs[i]);
    int cgroups=count_groups(image,averange);
    s[i]=";"+str(averange)+";"+str(pixel_brightness.size())+';'+str(group_brightness.size())+";"+str(cgroups);
}


int main(int argc, char** argv)
{
	Mat image;
	image = imread(argv[1], 1);
    //namedWindow("Display Image", WINDOW_AUTOSIZE);
	//imshow("Display Image", image);
    //waitKey(0);
	if (!image.data) {
		cout<<"No image data \n";
		return -1;
	}
    
    auto t=start_time();

    cvtColor(image,image,COLOR_RGB2GRAY);
    //cout<<image.rows<<' '<<image.cols<<'\n';
    vector<int> csts = vector<int> { 7, 9, 11, 15, 17,(int)mean(image)/32,80};
    vector<bool> fxs = vector<bool> {false,false,false,false,false,false,true};
    string sn=str(is_overexposed(image)); //row for save to csv file
    vector<string> s = vector<string>(7);
    #pragma omp parallel for //num_threads(7)
    for (int i=0;i<7;i++)
    {
        scan(image,s,csts,fxs,i);
    }

    get_time(t,"main");
    
    cout<<sn;
    for (int i=0;i<7;i++)
    {
        cout<<s[i];
    }
    cout<<'\n';
    process_mem_usage();
    return 0;
}