#include <opencv2/opencv.hpp>
#include <opencv2/cudaarithm.hpp>
#include <opencv2/cudafilters.hpp>
#include <opencv2/cudaimgproc.hpp>
#include <opencv2/cudawarping.hpp>
#include <iostream>
#include <vector>
#include <string>
#include <filesystem>

using namespace std;
using namespace cv;
using namespace cv::cuda;
namespace fs = std::filesystem;

constexpr double AREA_RATIO = 0.65;
constexpr double MIN_CONTOUR_FRACTION = 0.001;

int main() {
    cout << "CUDA is enabled" << endl;
    cout << "Path to image: ";
    string image;
    cin >> image;

    fs::path imgPath(image);
    imgPath = fs::absolute(imgPath);

    if (!fs::exists(imgPath)) {
        cerr << "File does not exist" << endl;
        return -1;
    }

    Mat frame = imread(imgPath.string());
    if (frame.empty()) {
        cerr << "Failed to load image: " << imgPath << endl;
        return -1;
    }

    GpuMat d_frame, d_hsv, d_redMask, d_blueMask;
    d_frame.upload(frame);

    Ptr<cuda::Filter> gaussianFilter = cuda::createGaussianFilter(d_frame.type(), d_frame.type(), Size(7, 7), 0);
    gaussianFilter->apply(d_frame, d_frame);

    cuda::cvtColor(d_frame, d_hsv, COLOR_BGR2HSV);

    Scalar lowerRed1(0, 70, 70), upperRed1(10, 255, 255);
    Scalar lowerRed2(160, 70, 70), upperRed2(179, 255, 255);
    GpuMat d_redMask1, d_redMask2;
    cuda::inRange(d_hsv, lowerRed1, upperRed1, d_redMask1);
    cuda::inRange(d_hsv, lowerRed2, upperRed2, d_redMask2);
    cuda::add(d_redMask1, d_redMask2, d_redMask);

    Ptr<cuda::Filter> morphFilter = cuda::createMorphologyFilter(MORPH_OPEN, d_redMask.type(), getStructuringElement(MORPH_ELLIPSE, Size(7, 7)));
    morphFilter->apply(d_redMask, d_redMask);
    morphFilter->apply(d_redMask, d_redMask);

    Scalar lowerBlue(100, 70, 70), upperBlue(130, 255, 255);
    cuda::inRange(d_hsv, lowerBlue, upperBlue, d_blueMask);
    morphFilter->apply(d_blueMask, d_blueMask);
    morphFilter->apply(d_blueMask, d_blueMask);

    Mat redMask, blueMask;
    d_redMask.download(redMask);
    d_blueMask.download(blueMask);

    Mat debugOverlay = frame.clone();
    vector<vector<Point>> contours;
    findContours(redMask, contours, RETR_EXTERNAL, CHAIN_APPROX_NONE);
    for (const auto &contour : contours) {
        double area = contourArea(contour);
        Point2f center;
        float radius;
        minEnclosingCircle(contour, center, radius);
        circle(debugOverlay, center, (int)radius, Scalar(0, 255, 255), 2);
        if (area >= AREA_RATIO * radius * radius * 3.1415f) {
            circle(debugOverlay, center, (int)radius, Scalar(0, 255, 0), 2);
        }
    }

    findContours(blueMask, contours, RETR_EXTERNAL, CHAIN_APPROX_NONE);
    for (const auto &contour : contours) {
        double area = contourArea(contour);
        Point2f center;
        float radius;
        minEnclosingCircle(contour, center, radius);
        circle(debugOverlay, center, (int)radius, Scalar(255, 255, 0), 2);
        if (area >= AREA_RATIO * radius * radius * 3.1415f) {
            circle(debugOverlay, center, (int)radius, Scalar(255, 0, 0), 2);
        }
    }

    namedWindow("BalloonDetection", WINDOW_NORMAL);
    imshow("BalloonDetection", debugOverlay);

    cout << "Press a button to exit" << endl;
    waitKey(0);

    return 0;
}