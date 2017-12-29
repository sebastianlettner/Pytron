//
// Created by Sebastian Lettner on 19.10.17.
//

#ifndef CI_MERGESORT_H
#define CI_MERGESORT_H

#include <stdio.h>
#include <string.h>
#include "bubbleSort.h"


void merge(char* s, int begin, int mid, int end);


void merge_sort(char* s) {

    int n = strlen(s);
    divide_and_conquer(s,0,n-1);

}

void divide_and_conquer(char* s,int begin, int end) {

    int mid;
    if ((end-begin) >1) {
    mid = (begin+end)/2; // e.g. length:7 -> (0+7)/2 = 3
    // Divide and Conquer
    divide_and_conquer(s,begin,mid);
    divide_and_conquer(s,mid+1,end);
    // Combine
    merge(s,begin,mid,end);
    }

}

void merge(char* s, int begin, int mid, int end) {


}


#endif //CI_MERGESORT_H
