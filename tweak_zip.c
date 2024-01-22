

#include <stdlib.h>
#include <stdio.h>

#define ZIP_SIZE 490

int main(int argc, char *argv[]) {
    printf("OMG\n");
    FILE *fp = fopen("good.zip", "rb");
    char *buffer = malloc(ZIP_SIZE);
    fread(buffer, ZIP_SIZE, 1, fp);

    /* The offsets are at octal 0000424, 0000547, and  0000661 with values 0, 50 an a0.. */
    /* decimal bytes: 276, 359, 433 */
    /* divide by 4 to get ints: 69, 89.75, 110.75 */

    // The offets aren't even mutliples of 4,but the numbers are ints.

    // attempt 1
    /*
    int *bp=(int *) (buffer+359);
    *bp=-100;
    int *cp=(int *) (buffer+433);
    *cp=-200;
     //file #2:  bad zipfile offset (lseek):  4294934528
     //file #3:  bad zipfile offset (lseek):  16769024
    */

    // attempt 2
    int *bp=(int *) (buffer+356);
    *bp=-100;

    int *cp=(int *) (buffer+430);
    *cp=-200;



    FILE *wfp = fopen("gooder.zip", "wb");
    fwrite(buffer, ZIP_SIZE, 1, wfp);
}
