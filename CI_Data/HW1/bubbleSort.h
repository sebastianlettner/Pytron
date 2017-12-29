//
// Created by Sebastian Lettner on 19.10.17.
//

#ifndef CI_BUBBLESORT_H
#define CI_BUBBLESORT_H

#include <stdio.h>
#include <string.h>
#include "InsertionSort.h"


void swap(char* s,int a, int b);

void bubbleSort() {

    char s[100];
    int length_input,i1,i2,l;

    //Read in a a string containing "A-Z" (max. 100 characters)
    scanf("%s", s);

    //Length of input
    length_input = strlen(s);

    if (length_input == 1) {
        printf("%s\n",s);
        return;
    }
    //Compute bubble sort algo
    for(i1 = length_input; i1>1; i1--) {
        for(i2 = 0; i2 < length_input -1; i2++) {
            if (s[i2] > s[i2+1]) {
                char* temp = s;
                swap(s, i2, i2 + 1);
                }

        }//End inner for-loop
        printf("%s\n", s);
        if (is_sorted(s)) {
            return;
        }
    }//End outter for-loop
}

void swap(char* s,int a, int b) {

    int length = strlen(s);
    //Catch index exeption
    if (a >= length || b >= length) {
        printf("Inidixes exeeds array dimension");
        return;
    }
    char temp;
    temp = s[a];
    s[a] = s[b];
    s[b] = temp;

    return;

}
#endif //CI_BUBBLESORT_H
