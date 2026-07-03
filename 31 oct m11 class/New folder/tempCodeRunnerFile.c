#include<stdio.h>
int main(){
     int a[5]={2,3,4,5,6};
     for(int i =0;i<5;i++)
         printf("%d is stored at  %u\n",*(a+i),a+i);
         return 0;
}