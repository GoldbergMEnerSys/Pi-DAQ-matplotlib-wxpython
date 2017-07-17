#include <iostream>
#include <errno.h>
#include <wiringPiI2C.h>
#include <string>
#include <cstdlib>

using namespace std;

int main(int argc, char *argv[])
{
   //cout << argv << endl;
   //cout << argv[1] << endl;
   int numValue  = atoi(argv[1]);
   string word;

   //memcpy(word, argv[0])

   //cout << num << endl;

   //numValue = Integer.parseInt(word);
   cout <<"hi " << numValue << endl;

   /*for (int i=0; i < argv[0].len(); i++) {
   	char* value = argv[i];
        cout << value << endl;
   	numValue += (*value%48)*(10^(i-1));
        cout<<numValue << endl;
   }*/

   cout << numValue << endl;

   int fd, result, set;

   fd = wiringPiI2CSetup(0x28);

   cout << "Init result: "<< fd << endl;

   set = wiringPiI2CWriteReg8(fd, 0xaf, 0x3);
  


   if(set == -1)
   {

      fd = wiringPiI2CSetup(0x2f);
      set = wiringPiI2CWriteReg8(fd, 0xaf, 0x3);
      if(set == -1)
      {

	fd = wiringPiI2CSetup(0x2e);
      	set = wiringPiI2CWriteReg8(fd, 0xaf, 0x03);
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
