#ifndef __VERIFICATION_H__
#define __VERIFIcATION_H__
#endif // !__VERIFICATION_H__

#include <stdio.h>
#include <string.h>
#include <stdlib.h>

extern char input[][101];
extern char* address_value;
extern int idx;
int invaild();
void init();
int inNum(char* nums);
int inAddress(char add);
int isExist(char *fName);
