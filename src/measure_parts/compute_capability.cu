/*
 * Program to show the COMPUTE CAPABILITY of the current device
 *
 * Version: Jul 2021
*/
#include <stdio.h>
//#define CURRENT_DEVICE 1
#define EXIT_SUCCESSFULLY 0
#define EXIT_ERROR -1


int main(int argc, char** argv) 
{
    cudaError_t resultMajor, resultMinor;
    int device, computeCapabilityMayor, computeCapabilityMinor;
    
    //cudaSetDevice(CURRENT_DEVICE);
    cudaGetDevice(&device);
    resultMajor = cudaDeviceGetAttribute(&computeCapabilityMayor, cudaDevAttrComputeCapabilityMajor, device);
    resultMinor = cudaDeviceGetAttribute(&computeCapabilityMinor, cudaDevAttrComputeCapabilityMinor, device);
    if (resultMajor != cudaSuccess || resultMinor != cudaSuccess)
        return EXIT_ERROR;
    printf("%d.%d\n",computeCapabilityMayor,computeCapabilityMinor);
    return EXIT_SUCCESSFULLY;
}