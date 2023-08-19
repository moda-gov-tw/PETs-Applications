#ifndef _DATA_H_
#define _DATA_H_

#include "binfhecontext-ser.h"
#include <vector>

struct data_
{
	char name[9];
	int caseNum;
	int location;
	int time;
};

struct dataCipher_
{
	lbcrypto::LWECiphertext nameCipher[8][5];
	lbcrypto::LWECiphertext caseCipher[3];
	lbcrypto::LWECiphertext locationCipher[8];
	lbcrypto::LWECiphertext timeCipher[13];
};


class DataBase
{
	private:
		std::vector <dataCipher_> __dataCipher;
		std::string __dirName;
	public:
		DataBase(const char* dirName);
		int fetch();
		std::vector <dataCipher_> get();
		//int encrypt(lbcrypto::LWEPrivateKey sk , lbcrypto::BinFHEContext cc , const char* fileName);
		//int query(lbcrypto::LWEPrivateKey sk , lbcrypto::BinFHEContext cc , const char* dirName);
};

#endif