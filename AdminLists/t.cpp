/******************************************************************************

                              Online C++ Compiler.
               Code, Compile, Run and Debug C++ program online.
Write your code in this editor and press "Run" button to compile and execute it.

*******************************************************************************/

#include <iostream>

using namespace std;

int main()
{
    int arr1[4] = {10,91,99,200};
    int arr2[3] = {81,182,149};
    
    int p = 101;
    int count = 0;
    
    for(int i=0;i<sizeof(arr1);i++){
        for(int j=0;j<sizeof(arr2);j++){
            
            int xorout = (arr1[i] ^ arr2[j]);
            if(p > xorout){
                if(((arr1[i]*xorout)-1)%p == 0){
                    count++;
                }
            }
        }
    }
    
    cout<< count;
    return count;
}
