#ifndef _ENCODE_H_
#define _ENCODE_H_

int decodeName(const char* name , int* ret);

int encodeName(int* dec , char* name);

int decodeCase(int n , int* ret);

int encodeCase(int* dec);

int decodeLocation(int n , int* ret);

int encodeLocation(int* dec);

int decodeTime(int n , int* ret);

int encodeTime(int* dec);

#endif