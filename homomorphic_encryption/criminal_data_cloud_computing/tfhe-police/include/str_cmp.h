#ifndef _STR_CMP_
#define _STR_CMP_

#include "binfhecontext.h"
using namespace lbcrypto;
LWECiphertext byte_comp(lbcrypto::LWECiphertext b1[8], lbcrypto::LWECiphertext b2[8], lbcrypto::ConstLWEPublicKey sk, lbcrypto::BinFHEContext cc);

LWECiphertext str_comp(lbcrypto::LWECiphertext s1[8][5], lbcrypto::LWECiphertext s2[8][5], lbcrypto::ConstLWEPublicKey sk, lbcrypto::BinFHEContext cc);


#endif
