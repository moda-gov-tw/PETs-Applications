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
		{"keygen" , 0 , NULL , 'k'} , 
		{"name" , 1 , NULL , 'n'} , 
		{"decrypt" , 1 , NULL , 'd'} ,
        {"decryptCount" , 0 , NULL , 'c'} ,
        {"encrypt" , 1 , NULL , 'e'} , 
		{"add" , 0 , NULL , 'a'}
	};
	while((c = getopt_long(argc , argv , "hn:d:kce:a" , opt , NULL)) != -1)
	{
		switch(c)
		{
			case 'h':
				help();
				break;
			case 'k':
				keygen();
				break;
			case 'n':
				encryptName(optarg);
				break;
			case 'd':
				decrypt(optarg);
				break;
            case 'c':
                decryptCount();
                break;
            case 'e':
				encrypt(optarg);
				break;
			case 'a':
				encrypt("insert");
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
	std::cout << "Usage: ./cleint [options] ...\n";
	std::cout << "Options:\n";
	std::cout << "\t-h, --help\t\tdisplay this help and exit.\n";
	std::cout << "\t-k, --keygen\t\tgenerate a key and save in \"./myKey\".\n";
	std::cout << "\t-n, --name NAME\t\tgenerate a file that can query by NAME(at most 8 characters). It also generate a file for decryption named \"CC\".\n";
	std::cout << "\t-d, --decrypt FILENAME\tdecrypt the result which is named FILENAME by \"./myKey\" and show the result.\n";
	return;
}
