

#include <stdlib.h>
#include <stdio.h>
#define ZIP_SIZE 490
int main(int argc, char *argv[]) {
    printf("OMG\n");
    FILE *fp = fopen("good.zip", "rb");
    char *buffer = malloc(ZIP_SIZE);
    fread(buffer, ZIP_SIZE, 1, fp);

    /* The offsets are at 0000424, 0000547, and  0000661 with values 0, 50 an a0.. */
/* 276, 359, 433, now what is -8 in 2-bytes 2's compliment? 65528?? */

    short *short_buffer = (short *) buffer;
    printf("%hi, %hi, %hi\n", short_buffer[138], short_buffer[179], short_buffer[217]);

    //for (int i=0; i<ZIP_SIZE; i++) { 
    //    printf("%d:   %c   %hi\n", i, buffer[i], short_buffer[i]); 
    //}

    int i=179;
    printf("%d:   %c   %hi\n", i, buffer[i], short_buffer[i]); 
    i=217;
    printf("%d:   %c   %hi\n", i, buffer[i], short_buffer[i]); 
    short_buffer[179]=-8;
    short_buffer[217]=-8;
    i=179;
    printf("%d:   %c   %hi\n", i, buffer[i], short_buffer[i]); 
    i=217;
    printf("%d:   %c   %hi\n", i, buffer[i], short_buffer[i]); 

    FILE *wfp = fopen("gooder.zip", "wb");
    //write(buffer, ZIP_SIZE, 1, wfp);
    fwrite((char *) short_buffer, ZIP_SIZE, 1, wfp);
}
