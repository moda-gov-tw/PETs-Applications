#ifndef _FUNCTION_H_
#define _FUNCTION_H_

#include "binfhecontext-ser.h"

struct nameCipher {
	lbcrypto::LWECiphertext nc[8][5];
};

/* server */
int fetchName(nameCipher* myCipher);
int counter();
void *eval(void *);/* thread of counter */
int query();

/* client */
int keygen();
int encrypt(const char* dirName);
int decrypt(const char* dirName);
int encryptName (char *name);
void decryptCount();
int add();

#endif
