#include <stdio.h>
#include <string.h>
#include <usb.h>
#include <time.h>
#include <fcntl.h>



void get_usb_device(void);
void do_speed(void);
void do_stop(void);
void do_endstopoff(void);
void do_endstopon(void);
void usb_send(char *message);
void usb_get(char *message);
void do_adc(void);
void do_hp(void);
void do_ha(void);
void do_isotherm(void);
void do_adc_to_file(FILE *fhandle,int time);
void do_open(void);
void do_close(void);
float return_calibrated_pressure(int pvalue);
void set_globalhighpressure(void);
void set_globallowpressure(void);
void set_globalzero(void);
void do_pressure(void);
int get_raw_pressure(float fpressure);

usb_dev_handle *usbhandle;
char filepath[64] ="temp.txt";
int globalhighpressure = 27677;
int globallowpressure = 20784;
int globalzero= 26916;
float timeaveragecurrentpressure[5];

int main(int argc, char **argv)
	{

 	//usb_dev_handle *usbhandle = 0;

	unsigned char incmd[64];

	
	
	printf("Program has started.\n");
	
	get_usb_device();  // start up and connect to the controller

		
	while(strcmp(incmd,"exit") != 0){
		printf("Command:");
		scanf("%s",incmd);


		if (strcmp(incmd,"speed")==0){
			do_speed();
		}
		if (strcmp(incmd,"stop")==0){
			do_stop();
		}
		if (strcmp(incmd,"endstopoff")==0){
			do_endstopoff();
		}
		if (strcmp(incmd,"endstopon")==0){
			do_endstopon();
		}
		if (strcmp(incmd,"adc")==0){
			do_adc();
		}
		if (strcmp(incmd,"hp")==0){
			do_hp();
		}
		if (strcmp(incmd,"ha")==0){
			do_ha();
		}
		if (strcmp(incmd,"record")==0){
			do_isotherm();
		}
		if (strcmp(incmd,"open")==0){
			printf("Opening Barrier.\n");
			do_open();
		}
		if (strcmp(incmd,"close")==0){
			printf("Closing Barrier.\n");
			do_close();
		}
		if (strcmp(incmd,"psethigh")==0){
			set_globalhighpressure();
		}
		if (strcmp(incmd,"psetlow")==0){
			set_globallowpressure();
		}
		if (strcmp(incmd,"psetzero")==0){
			set_globalzero();
		}
		if (strcmp(incmd,"pressure")==0){
			do_pressure();
		}

	}	

	printf("Closing the handle\n");
	usb_close(usbhandle);

	printf(" Exiting now.\n");

	return 0;
	}

void get_usb_device(void)
	{
	struct usb_bus *busses;
	struct usb_bus *bus;
	struct usb_device *dev;
	struct usb_config_descriptor *config;
	struct usb_interface_descriptor *interface;
	//usbhandle= -1;
	int errorcode;

	usb_init();
	usb_set_debug(3);
	usb_find_busses();
	usb_find_devices();
	busses = usb_get_busses();
	printf("Libusb init.\n");

	for(bus = busses; bus; bus = bus->next){
		for(dev = bus->devices; dev; dev = dev->next){
			//printf("%x\n",dev->descriptor.idVendor);
			//printf("%x\n",dev->descriptor.idProduct);
			//printf("num interfaces %d.\n", dev->config[0].bNumInterfaces);
			//printf("Configuration value %d.\n", dev->config[0].bConfigurationValue);
			//if ((dev->descriptor.idVendor == 0x3eb)&&(dev->descriptor.idProduct == 0xFF2))
			if ((dev->descriptor.idVendor == 0xFF2)&&(dev->descriptor.idProduct == 0xFF2))
				{
					usbhandle = usb_open(dev);
						if(usbhandle <= 0){
						printf("Could not open the device.\n");
						}else{
						printf("Opend the device.\n");
						}
						errorcode = usb_set_configuration(usbhandle,1);	
						printf("%i Setting config.\n",errorcode);

						errorcode = usb_claim_interface(usbhandle,0);	
						printf("%i claiming interface.\n",errorcode);

						errorcode = usb_set_altinterface(usbhandle,0);	
						printf("%i set alt interface.\n",errorcode);
					
				}
			}
		}
	}

void do_speed(void){
	unsigned char invalue[64];
	unsigned char message[64];
	int speed;
	
	printf("enter speed from 0 to 1023: ");
	scanf("%s",invalue);
	
	speed = atoi(invalue);
	
	message[0]='1';
	message[2]=speed;
	message[1]=(speed>>8);
	printf(" speed is %i.\n",speed); 

	usb_send(message);
	
	usb_get(message);
}

void usb_send(char *message){
	int bytessent;
	bytessent = usb_bulk_write(usbhandle, 0x02, message, 64, 1000);
	//printf("%i bytes sent.\n",bytessent);

}

void usb_get(char *message){
	int bytessent = 0;
	bytessent = usb_bulk_read(usbhandle, 0x81, message, 64, 1000);
	//printf("message recieved is %s.\n",message);
	//printf("message recieved is %i.\n",bytessent);
}

void do_stop(void){
	usb_send("0");

}

void do_endstopoff(void){
	usb_send("a");

}

void do_endstopon(void){
	usb_send("b");

}

void do_adc(void){
	int bytessent;
	int barriervalue;
	int psensorvalue;
	unsigned char message[64];
	message[0]='3';

	usb_send(message);

	usb_get(message);


	barriervalue = message[3];
	barriervalue = (barriervalue<<8)|message[4];
	psensorvalue = message[1];
	psensorvalue = (psensorvalue<<8)|message[2];
	printf("The barrier value was %i ",barriervalue);
	printf("and the pressure sensor value was %i.\n",psensorvalue);
}

void do_hp(void){
	unsigned char message[64];
	unsigned char invalue[64];
	message[0]='4';
	int rawpressure;
	float calpressure;
	
	printf("enter hold pressure: ");
	scanf("%s",invalue);
	
	calpressure = atof(invalue);
	
	rawpressure = get_raw_pressure(calpressure);

	message[2]=rawpressure;
	message[1]=(rawpressure>>8);
	printf("Hold pressure is set to %F.\n",calpressure); 

	usb_send(message);
	
	usb_get(message);
}

void do_ha(void){
	unsigned char message[64];
	unsigned char invalue[64];
	message[0]='5';
	int speed;
	
	printf("enter hold area: ");
	scanf("%s",invalue);
	
	speed = atoi(invalue);
	
	message[2]=speed;
	message[1]=(speed>>8);
	printf("Hold area is set to %i.\n",speed); 

	usb_send(message);
	
	usb_get(message);
}

void do_isotherm(void){

	char* stri;
	int compipe[2];
	unsigned char incmd[64] = "go";

	timeaveragecurrentpressure[0] = 0;
	timeaveragecurrentpressure[1] = 0;
	timeaveragecurrentpressure[2] = 0;
	timeaveragecurrentpressure[3] = 0;
	timeaveragecurrentpressure[4] = 0;

	pipe(compipe);

	if(fork() == 0){
		close(compipe[0]);
		while(strcmp(incmd,"end") != 0){
			printf("Recording has started. Type end to end.\n");
			scanf("%s",incmd);
			write(compipe[1],incmd,(strlen(incmd)+1));
		}
		exit(0);
	
	}else{
		FILE *fhandle;
		time_t currenttime= time(NULL);
		time_t lastmessure= time(NULL);
		time_t starttimer = time(NULL);
		close(compipe[1]);
		int flags = fcntl(compipe[0],F_GETFL,0);
		fcntl(compipe[0],F_SETFL,flags|O_NONBLOCK);
		
		fhandle=fopen(filepath, "a");
		fprintf(fhandle,"# ");
		//fprintf(fhandle,ctime(&starttimer));
		fprintf(fhandle,"# Time bvalue pvalue Pressure timeavgpress\n");
		fclose(fhandle);

		

		
	
		while(strcmp(incmd,"end")!=0){
			read(compipe[0],incmd,sizeof(incmd));
			time(&currenttime);
			if((int)difftime(currenttime,lastmessure)>= 1){		
					fhandle=fopen(filepath, "a");
					
					do_adc_to_file(fhandle,(int)difftime(currenttime,starttimer));
					lastmessure=currenttime;
					fclose(fhandle);
				}
				if (strcmp(incmd,"open")==0){
					printf("Opening Barrier.\n");
					do_open();
				}
				if (strcmp(incmd,"close")==0){
					printf("Closing Barrier.\n");
					do_close();
				}
				if (strcmp(incmd,"stop")==0){
					do_stop();
				}
			}
	


		
		
		
	
	}

}

void do_adc_to_file(FILE *fhandle,int time){
	int bytessent;
	int barriervalue;
	int psensorvalue;
	float calpressure,avgpressure;
	unsigned char message[64];
	message[0]='3';

	usb_send(message);

	usb_get(message);


	barriervalue = message[3];
	barriervalue = (barriervalue<<8)|message[4];
	psensorvalue = message[1];
	psensorvalue = (psensorvalue<<8)|message[2];

	calpressure = return_calibrated_pressure(psensorvalue);
	timeaveragecurrentpressure[0] = timeaveragecurrentpressure[1];
	timeaveragecurrentpressure[1] = timeaveragecurrentpressure[2];
	timeaveragecurrentpressure[2] = timeaveragecurrentpressure[3];
	timeaveragecurrentpressure[3] = timeaveragecurrentpressure[4];
	timeaveragecurrentpressure[4] = calpressure;

	avgpressure = (timeaveragecurrentpressure[0]+timeaveragecurrentpressure[1]+timeaveragecurrentpressure[2]+timeaveragecurrentpressure[3]+timeaveragecurrentpressure[4])/5;


	fprintf(fhandle,"%i %i %i %f %f\n",time,barriervalue,psensorvalue,calpressure,avgpressure);
	printf("%i %i %i %f %f\n",time,barriervalue,psensorvalue,calpressure,avgpressure);
}


void do_open(void){
	unsigned char message[64] ="6";
	usb_send(message);
}

void do_close(void){
	unsigned char message[64]="7";
	usb_send(message);
}


float return_calibrated_pressure(int pvalue){
	float calibratedpressure;
	calibratedpressure = -72/(float)(globalhighpressure - globallowpressure)*(float)(pvalue - globalzero);
	return(calibratedpressure);

}

void set_globalhighpressure(void){
	int bytessent;
	int barriervalue;
	int psensorvalue;
	unsigned char message[64];
	message[0]='3';

	usb_send(message);

	usb_get(message);


	psensorvalue = message[1];
	psensorvalue = (psensorvalue<<8)|message[2];
	globalhighpressure = psensorvalue;
	printf("High pressure set to %i\n",psensorvalue);

}

void set_globallowpressure(void){

	int bytessent;
	int barriervalue;
	int psensorvalue;
	unsigned char message[64];
	message[0]='3';

	usb_send(message);

	usb_get(message);


	psensorvalue = message[1];
	psensorvalue = (psensorvalue<<8)|message[2];
	globallowpressure = psensorvalue;
	printf("Low pressure set to %i\n",psensorvalue);
}

void set_globalzero(void){

	int bytessent;
	int barriervalue;
	int psensorvalue;
	unsigned char message[64];
	message[0]='3';

	usb_send(message);

	usb_get(message);


	psensorvalue = message[1];
	psensorvalue = (psensorvalue<<8)|message[2];
	globalzero = psensorvalue;
	printf("zero pressure set to %i\n",psensorvalue);
}

void do_pressure(void){
	int bytessent;
	int barriervalue;
	int psensorvalue;
	unsigned char message[64];
	message[0]='3';

	usb_send(message);

	usb_get(message);


	psensorvalue = message[1];
	psensorvalue = (psensorvalue<<8)|message[2];
	printf("Pressure is at %f dyne\n",return_calibrated_pressure(psensorvalue));
}

int get_raw_pressure(float fpressure){
	int rawpressure;
	rawpressure =(fpressure*(globalhighpressure - globallowpressure)/-72)+globalzero;
	printf("Calibrate pressure %f, raw value %i . \n",fpressure, rawpressure);
	return(rawpressure);

}
