#include <iostream>
#include <errno.h>
#include <wiringPiI2C.h>
#include <string>
#include <cstdlib>

using namespace std;

int main(int argc, char *argv[])
{

   int numValue  = atoi(argv[1]);
   //std::stringstream stream;

   //cout << numValue << endl;
   //stream << "0x" << std::hex << numValue << endl;
   string valToSet;
   //valToSet << "0x" << hex << numValue << endl;

   int fd, result, set;

   fd = wiringPiI2CSetup(0x29);


   //for(int i=0;i<100;i++){
   set = wiringPiI2CWriteReg8(fd, 0x00, 0xFF);
   set = wiringPiI2CWriteReg8(fd, 0x00, 0xFF);
   set = wiringPiI2CWriteReg8(fd, 0x01, 0xFF);
   set = wiringPiI2CWriteReg8(fd, 0x02, 0xFF);
   set = wiringPiI2CWriteReg8(fd, 0x03, 0xFF);
   //}

   if(set == -1)
   {
      cout << "Error.  Errno is: " << errno << endl;

      /*fd = wiringPiI2CSetup(0x2f);
      set = wiringPiI2CWriteReg8(fd, 0xaf, numValue);
      if(set == -1)
      {

	fd = wiringPiI2CSetup(0x2e);
      	set = wiringPiI2CWriteReg8(fd, 0xaf, numValue);
      	if(set == -1)
      	{
	}
	

      }*/
   }

   //set = wiringPiI2CWriteReg8(fd, 0xFF, numValue);
   //set = wiringPiI2CWrite(fd, numValue);

   //if(set == -1)
   //{
      //cout << "Error.  Errno is: " << errno << endl;

      /*fd = wiringPiI2CSetup(0x2f);
      set = wiringPiI2CWriteReg8(fd, 0xaf, numValue);
      if(set == -1)
      {

	fd = wiringPiI2CSetup(0x2e);
      	set = wiringPiI2CWriteReg8(fd, 0xaf, numValue);
      	if(set == -1)
      	{
	}
	

      }*/
   //}


   /*result = wiringPiI2CRead(fd);

   if(result == -1)
   {
      cout << "Error.  Errno is: " << errno << endl;
   }
   else {
	cout <<result<<endl;
   }*/
   
}

   //string word;
   //cout << argv << endl;
   //cout << argv[1] << endl;
   //memcpy(word, argv[0])

   //cout << num << endl;

   //numValue = Integer.parseInt(word);
   //cout <<"hi " << numValue << endl;

   /*for (int i=0; i < argv[0].len(); i++) {
   	char* value = argv[i];
        cout << value << endl;
   	numValue += (*value%48)*(10^(i-1));
        cout<<numValue << endl;
   }*/
      //cout << "Init result: "<< fd << endl;

   /*else {
		cout <<"sucess: "<<set<<endl;
   	}*/
