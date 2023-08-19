#include "encode.h"
#include <stdio.h>

int decodeName(const char* name , int* ret)
{
	for(int i = 0 ; i < 8 ; i++)
	{
		int temp = 1;
		// printf("%d\n" , (name[i] | ' ') - 'a' + 1);
		for(int j = 0 ; j < 5 ; j++)
		{
			ret[i * 5 + 4 - j] = ((name[i] | ' ') & temp) / temp;
			temp <<= 1;
		}
	}
	return 0;
}

int encodeName(int* dec , char* name)
{
	for(int i = 0 ; i < 8 ; i++)
	{
		char temp = dec[i * 5];
		for(int j = 1 ; j < 5 ; j++)
		{
			temp <<= 1;
			temp += dec[i * 5 + j];
			// printf("%d\n" , temp);
		}
		if(temp)
		{
			name[i] = temp | 96;
		}
		else
		{
			name[i] = temp;
		}
	}
	name[0] = name[0] ^ 32;
	return 0;
}

int decodeCase(int n , int* ret)
{
	int temp = 1;
	for(int i = 0 ; i < 3 ; i++)
	{
		ret[2 - i] = (n & temp) / temp;
		temp <<= 1;
	}
	return 0;
}

int encodeCase(int* dec)
{
	int temp = dec[0];
	for(int i = 1 ; i < 3 ; i++)
	{
		temp <<= 1;
		temp += dec[i];
	}
	return temp;
}

int decodeLocation(int n , int* ret)
{
	int temp = 1;
	for(int i = 0 ; i < 8 ; i++)
	{
		ret[7 - i] = (n & temp) / temp;
		temp <<= 1;
	}
	return 0;
}

int encodeLocation(int* dec)
{
	int temp = dec[0];
	for(int i = 1 ; i < 8 ; i++)
	{
		temp <<= 1;
		temp += dec[i];
	}
	return temp;
}

int decodeTime(int n , int* ret)
{
	int year = 2023 - n / 10000;
	int month = (n / 100) % 100;
	int day = n % 100;
	// printf("%d , %d , %d\n" , year , month , day);
	int temp = 1;
	//year
	for(int i = 0 ; i < 4 ; i++)
	{
		ret[3 - i] = (year & temp) / temp;
		temp <<= 1;
	}
	//month
	temp = 1;
	for(int i = 0 ; i < 4 ; i++)
	{
		ret[7 - i] = (month & temp) / temp;
		temp <<= 1;
	}
	//day
	temp = 1;
	for(int i = 0 ; i < 5 ; i++)
	{
		ret[12 - i] = (day & temp) / temp;
		temp <<= 1;
	}
	return 0;
}

int encodeTime(int* dec)
{
	//year
	int year = dec[0];
	for(int i = 1 ; i < 4 ; i++)
	{
		year <<= 1;
		year += dec[i];
	}
	year = 2023 - year;
	//month
	int month = dec[4];
	for(int i = 5 ; i < 8 ; i++)
	{
		month <<= 1;
		month += dec[i];
	}
	//day
	int day = dec[8];
	for(int i = 9 ; i < 13 ; i++)
	{
		day <<= 1;
		day += dec[i];
	}
	int ret = year * 10000 + month * 100 + day;
	return ret;
}
