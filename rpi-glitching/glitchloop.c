#include <stdio.h>
 
//gcc glitchloop.c -o glitchloop
//./glitchloop
 
int main(void){
	volatile int i, j, k,l;
 
	char status[] = "<>";
 
	while(1){
 
	k = 0;
	for (i=0; i < 10000; i++){
		for (j=0; j < 10000; j++){
			k++;
		}
	}
 
	printf("%d %d %d %c\n", i, j, k, status[l++ % 2]);
 
	}
 
 
}