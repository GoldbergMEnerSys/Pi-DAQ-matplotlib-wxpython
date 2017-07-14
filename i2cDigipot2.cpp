#include <iostream>
#include <errno.h>
#include <wiringPiI2C.h>

using namespace std;

int main()
{
   int fd, result, set;

   fd = wiringPiI2CSetup(0x28);

   cout << "Init result: "<< fd << endl;

   set = wiringPiI2CWriteReg8(fd, 10101111, 00000011);
  


   if(set == -1)
   {

      fd = wiringPiI2CSetup(0x2f);
      set = wiringPiI2CWriteReg8(fd, 10101111, 00000011);
      if(set == -1)
      {

	fd = wiringPiI2CSetup(0x2e);
      	set = wiringPiI2CWriteReg8(fd, 10101111, 00000011);
      	if(set == -1)
      	{
      		cout << "Error.  Errno is: " << errno << endl;
	}
	else {
		cout <<"sucess: "<<set<<endl;
   	}

      }
      else {
	cout <<"sucess: "<<set<<endl;
      }
   }
   else {
	cout <<"sucess: "<<set<<endl;
   }


   result = wiringPiI2CRead(fd);

   if(result == -1)
   {
      cout << "Error.  Errno is: " << errno << endl;
   }
   else {
	cout <<"data: "<<result<<endl;
   }
   
}
