#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>
#include <sys/types.h>


int main(int argc, char **argv)
	{
	int commpipe[2];
	pid_t pid;

	if(pipe(commpipe)){
		printf("Could not create pipe.\n");
		return(1);
		}
	
	
	
	
	return 0;
	}
