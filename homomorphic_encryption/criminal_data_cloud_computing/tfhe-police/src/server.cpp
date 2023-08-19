#include <iostream>
#include <getopt.h>
#include "function.h"

using namespace lbcrypto;

void help();

int main(int argc , char* argv[])
{
	int c = 0;
	option opt[] = 
	{
		{"help" , 0 , NULL , 'h'} , 
		{"counter" , 0 , NULL , 'c'} ,
		{"qeury" , 0 , NULL , 'q'} , 
		{"add" , 0 , NULL , 'a'}
	};
	while((c = getopt_long(argc , argv , "hcqa" , opt , NULL)) != -1)
	{
		switch(c)
		{
			case 'h':
				help();
				break;
			case 'c':
                counter();
                break;
            case 'q':
                query();
                break;
			case 'a':
				add();
				break;
			case '?':
				std::cout << "unknown argument.\n";
				break;
			default:
				std::cout << "unknown error.\n";
		}
	}
	return 0;
}

void help()
{
	std::cout << "Usage: ./server [options] ...\n";
	std::cout << "Options:\n";
	std::cout << "\t-h, --help\t\tdisplay this help and exit.\n";
	std::cout << "\t-c, --count\n";
	std::cout << "\t-q, --query\n";
	std::cout << "\t-a, --add\n";
	return;
}