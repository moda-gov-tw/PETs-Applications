
#include "binfhecontext.h"
#include "str_cmp.h"

using namespace lbcrypto;
LWECiphertext byte_comp(LWECiphertext b1[5], LWECiphertext b2[5], ConstLWEPublicKey sk, BinFHEContext cc){
	auto check = cc.Encrypt(sk, 1);
	for(int i = 0 ;i < 5; i++){
		auto temp = cc.EvalBinGate(XNOR, b1[i], b2[i]);
		check = cc.EvalBinGate(AND, check, temp);	
	}
	return check;
}
LWECiphertext str_comp(LWECiphertext s1[8][5], LWECiphertext s2[8][5], ConstLWEPublicKey sk, BinFHEContext cc){
	auto check = cc.Encrypt(sk, 1);
	for(int i = 0 ;i < 8; i++){
		auto temp = byte_comp(s1[i], s2[i], sk, cc);
		check = cc.EvalBinGate(AND, check, temp);	
	}
	return check;
}



