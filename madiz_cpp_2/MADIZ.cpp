#include "obr.hpp"
#include "util.hpp"
#include "serv.hpp"
#include "PCA.hpp"
#include "dtypes.h"
#include <omp.h>
#include <iostream>
#include <vector>
#include <opencv2/opencv.hpp>
#include <string>
#define str to_string
using cv::Mat;
using cv::COLOR_RGB2GRAY;
using cv::imread;
using namespace std;


void scan(Mimg &img,vector<string>&s,vector<int> &csts,int i)
{
    float averange=mean(img)+csts[i];
    vector<unsigned int> sum_groups_bright;
    vector<float> groups_bright;
    int particle=0,treck=0;
    int cnt_groups=count_groups(img,averange);
    tie(treck, particle, groups_bright,sum_groups_bright)=count_cloudsPCA(img);
    s[i]=";"+str(averange)+";"+str(treck)+';'+str(particle)+";"+str(cnt_groups);
}


int main(int argc, char** argv)
{
    ios::sync_with_stdio(false);
    cin.tie(NULL);
    cout.tie(NULL);
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
    Mimg img(image);
    //cout<<image.rows<<' '<<image.cols<<'\n';
    vector<int> csts = vector<int> {17};
    vector<bool> fxs = vector<bool> {false};
    string sn=str(is_overexposed(img)); //row for save to csv file
    vector<string> s = vector<string>(csts.size());
    #pragma omp parallel for
    for (int i=0;i<csts.size();i++)
    {
        scan(img,s,csts,i);
    }

    cout<<sn;
    for (int i=0;i<csts.size();i++)
    {
        cout<<s[i];
    }
    cout<<'\n';
    
    get_time(t,"main");
    process_mem_usage();

    return 0;
}