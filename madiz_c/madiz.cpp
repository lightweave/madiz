using namespace std;

#include <iostream>
#include "lodepng.h"
#include <vector>
#include <cstdlib>
#include <fstream>
#include <chrono>
#include <ctime>
#include <string>
#include <bits/stdc++.h>

int main(int argc, char *argv[]) {
   
    ofstream outfile;
    time_t now = time(0);
    tm *ltm = localtime(&now);
 
    string hrs = to_string(ltm -> tm_hour);
    string minn = to_string(ltm -> tm_min);
    string secc = to_string(ltm -> tm_sec);
    string name_file = hrs + '-' + minn + '-' + secc;
    
    outfile.open(name_file + ".txt");
    while (1) {
        time_t now = time(0);
        tm *ltm = localtime(&now);
    
        hrs = to_string(ltm -> tm_hour);
        minn = to_string(ltm -> tm_min);
        secc = to_string(ltm -> tm_sec);
        name_file = hrs + '-' + minn + '-' + secc;
        vector<unsigned char> pixels;
        string command = "raspistill -t 10 -ISO 800 -br 50 -ex night -ag 1 -ss 3000000 -st --encoding png -o /home/pi/Desktop/monitor1/c++/" + name_file + ".png";
        int ret = std::system(command.c_str());

        unsigned width, height;
        lodepng::decode(pixels, width, height, "/home/pi/Desktop/monitor1/c++/" + name_file + ".png");

        long sbr_pix = accumulate(pixels.begin(), pixels.end(), 0) / 24245760 + 11;
        int spxR = 0;
        int spxG = 0;
        int spxB = 0;
        vector <vector <int>> pixb;
        vector <vector <int>> pixb_p;
        int threshold = 80;
        for (int y = 0; y < height; y++) {
            for (int x = 0; x < width; x++) {
                size_t byte_index = (y * width + x)  * 3;
                spxR = pixels[byte_index];
                spxG = pixels[byte_index + 1];
                spxB = pixels[byte_index + 2];
                int brightness = (spxR + spxG + spxB) / 3;
                if (brightness > threshold) {
                    pixb.push_back({x, y});
                }
    	        if (brightness > sbr_pix) {
    		    pixb_p.push_back({x, y});
                }
            }
        }
    
        outfile << name_file << " " << threshold << " " << pixb.size() << " "  << sbr_pix << endl;
        cout << pixb.size() << " " << pixb.size()  << " "  << sbr_pix << "\n";
    }
    return 0;
}
