/*
Program to add dates to the CSV file at the beginning of each line.

Written in C because it was easier to do than in Python, and much faster.
*/

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#define LINE_SIZE 500

int main() {    
    FILE *file_ptr;
    file_ptr = fopen("/home/jose/Programming/aiml/Data/houston-AQI-weather/data_new.csv", "r");

    char line[LINE_SIZE]; char line_buffer[LINE_SIZE];

    int line_num = 0;
    while (fgets(line, LINE_SIZE, file_ptr)) {
        int month = (line_num % 12) + 1;
        int year = 1997 + (line_num / 12);

        if (line[0] != '\n') {
            sprintf(line_buffer, "%02d-%d", month, year); strcat(line_buffer, line);
            printf("%s", line_buffer);
        } else {
            printf("%s", line);
            ++line_num;
        }
    }

    return 0;
}
