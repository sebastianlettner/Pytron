//
// Created by Sebastian Lettner on 19.10.17.
//

#ifndef CI_INSERTIONSORT_H
#define CI_INSERTIONSORT_H

#include "stdio.h"
#include "stdbool.h"

bool is_sorted(char* s);


void insertionSort() {

    char s[100];
    int length_input,i1,i2;

    //Read in a a string containing "A-Z" (max. 100 characters)
    scanf("%s", s);

    //Length of input
    length_input = strlen(s);

    if (length_input == 1) {
        printf("%s\n",s);
        return;
    }
    for (i1 = 1; i1 < length_input; i1++) {
        char sort_val = s[i1];
        i2 = i1;
        while (i2 > 0 && s[i2 - 1] > sort_val) {
            s[i2] = s[i2 - 1];
            i2--;
        }
        s[i2] = sort_val;
        printf("%s\n", s);
        if (is_sorted(s)) {
            return;
        }

    }



}

bool is_sorted(char* s) {

    int i,n;
    bool sorted_flag = true;
    n = strlen(s);
    if (n == 1) {
        return true;
    }

    for (i = 0; i<n-1; i++) {
        if (s[i] > s[i+1]) {
            sorted_flag = false;
        }
    }
    return sorted_flag;

}

#endif //CI_INSERTIONSORT_H
