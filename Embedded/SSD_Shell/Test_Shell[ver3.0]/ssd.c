#include <stdio.h>
#include <stdlib.h>
#include <string.h>
int main(int argc, char* argv[]) {
	FILE* ssd = fopen("nand.txt","r+");
	int idx = atoi(argv[2]);
	fseek(ssd, 16 * idx, SEEK_SET);
	if (strcmp(argv[1], "W") == 0) {
		char buffer[21];
		sprintf(buffer,"[%02d] %s", idx,argv[3]);
		fputs(buffer,ssd);
	}
	else {
		FILE* result = fopen("result.txt", "w");
		char arr[20];
		fgets(arr,20,ssd);
		fputs(arr,result);
		fclose(result);
	}
	fclose(ssd);

	return 0;
}
