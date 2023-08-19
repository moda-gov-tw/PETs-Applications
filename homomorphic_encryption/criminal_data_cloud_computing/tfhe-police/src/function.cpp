#include <iostream>

#include <cstring>

#include <stdlib.h>

#include <stdio.h>

#include <future>

#include "binfhecontext-ser.h"

#include "function.h"

#include "encode.h"

#include "data.h"

#include "str_cmp.h"

/* global variables */

lbcrypto::LWECiphertext count[10];

int numThreads = 8;

pthread_mutex_t lock;

/* assigned to counter threads */
int dataIdx[8] = {0,1,2,3,4,5,6,7};

int blockSize;

/*data size */
int num;

std::vector <dataCipher_> tempdata;

lbcrypto::LWECiphertext qNameCipher[8][5];

lbcrypto::LWEPrivateKey secretKey;

lbcrypto::BinFHEContext cryptoContext;


#define DEBUG 0

void decryptCount() {

    lbcrypto::LWEPrivateKey sk;

    lbcrypto::BinFHEContext cc;

    lbcrypto::Serial::DeserializeFromFile("secretKey" , sk , lbcrypto::SerType::BINARY);

    lbcrypto::Serial::DeserializeFromFile("CC" , cc , lbcrypto::SerType::BINARY);

    lbcrypto::LWECiphertext countCipher[10];

    lbcrypto::LWEPlaintext countPlain[10];

    int sum   = 0;

    int power = 1; /* 2^0 */

    char* filename;

    system("unzip countResult");

    puts("start decrypting...");

    for (int bit = 0; bit < 10 ; bit++) {

        asprintf(&filename, "countResult/%d-count", bit);

        lbcrypto::Serial::DeserializeFromFile(filename, countCipher[bit], lbcrypto::SerType::BINARY);

        cc.Decrypt(sk, countCipher[bit], &countPlain[bit]);

        sum += (power * countPlain[bit]);

        power = power * 2;

    }

    std::cout << "the count result (decimal) is : " << sum << std::endl;


}


int counter(){

    DataBase mydb("encData");

    nameCipher mycipher;

    mydb.fetch();

    fetchName(&mycipher);

    lbcrypto::LWEPublicKey publicKey;
	lbcrypto::Serial::DeserializeFromFile("myKey" , publicKey , lbcrypto::SerType::BINARY);
	lbcrypto::Serial::DeserializeFromFile("CC" , cryptoContext , lbcrypto::SerType::BINARY);
	lbcrypto::RingGSWACCKey refreshKey;
	lbcrypto::LWESwitchingKey ksKey;
	lbcrypto::Serial::DeserializeFromFile("rfKey" , refreshKey , lbcrypto::SerType::BINARY);
	lbcrypto::Serial::DeserializeFromFile("ksKey" , ksKey , lbcrypto::SerType::BINARY);

	cryptoContext.BTKeyLoad({refreshKey , ksKey});

    tempdata = mydb.get();

    num = tempdata.size();

    for(int i = 0;i <8 ;i++){

        for(int j = 0;j < 5;j++)

            qNameCipher[i][j] = mycipher.nc[i][j];
    }

    blockSize = (num - 1) / numThreads + 1;

    /* initialize the count as 0 in ciphertext */
    for (int i = 0;i < 10; i++ ) {

        count[i] = cryptoContext.Encrypt(publicKey, 0);

    }

    system("mkdir countResult");

    puts("start multi-processing...");


    if (pthread_mutex_init(&lock, NULL) != 0) {

        printf("\n mutex init has failed\n");

        return 1;
    }

    int *tinfo = dataIdx;

    int i = 0;

    int error;

    pthread_t tid[8];

    while (i < numThreads) {

        error = pthread_create(&(tid[i]),
                               NULL,
                               &eval, (void*)&tinfo[i]);
        if (error != 0)

            printf("\nThread can't be created :[%s]",

                   strerror(error));

        i++;

    }


    for (int t = 0; t < numThreads; t++) {

        if (pthread_join(tid[t], NULL) != 0) {

            perror("pthread_join() error");

            exit(3);

        }
    }
    pthread_mutex_destroy(&lock);

    puts("serializing count to file... ");

    char* filename;

    for (int bit = 0; bit < 10; bit++) {

        asprintf(&filename, "countResult/%d-count", bit);

        lbcrypto::Serial::SerializeToFile(filename, count[bit], lbcrypto::SerType::BINARY);
    }

    system("zip -r countResult countResult");

    system("rm -rf countResult");

    return 0;
}

void *eval(void *arg) {

    int *data = (int *) arg;

	lbcrypto::LWEPublicKey publicKey;
	lbcrypto::Serial::DeserializeFromFile("myKey" , publicKey , lbcrypto::SerType::BINARY);
	lbcrypto::Serial::DeserializeFromFile("CC" , cryptoContext , lbcrypto::SerType::BINARY);
	lbcrypto::RingGSWACCKey refreshKey;
	lbcrypto::LWESwitchingKey ksKey;
	lbcrypto::Serial::DeserializeFromFile("rfKey" , refreshKey , lbcrypto::SerType::BINARY);
	lbcrypto::Serial::DeserializeFromFile("ksKey" , ksKey , lbcrypto::SerType::BINARY);

	cryptoContext.BTKeyLoad({refreshKey , ksKey});

    printf("thread %d is running\n", data[0]);

    for (int b = 0; b < blockSize; b++) {

        if (b + data[0] * blockSize >= num) {
            break;
        }

        /* cmpResult is 0 or 1 in ciphertext */
        auto cmpResult = str_comp(tempdata[b + data[0] * blockSize].nameCipher, qNameCipher, publicKey, cryptoContext);

        /* the count is shared variable so we have to synchronize the threads */

        pthread_mutex_lock(&lock);

        auto carry = cmpResult;

        for (int bit = 0; bit < 10; bit++) {

            auto res = cryptoContext.EvalBinGate(XOR, count[bit], carry);

            carry = cryptoContext.EvalBinGate(AND, count[bit], carry);

            count[bit] = res;

        }

        pthread_mutex_unlock(&lock);


    }
        
       printf("thread %d finished\n", data[0]);
    

       return NULL;
}




int encryptName(char* name)

{

	char temp[9] = {'\0'};

	strncpy(temp , name , 8);

	int* pDName = (int*)calloc(40 , sizeof(int));

	decodeName(temp , pDName);

	std::cout << "Fetching key and cryptoContext ...\n";

	lbcrypto::LWEPrivateKey SecretKey;

	lbcrypto::BinFHEContext CryptoContext;

	if(lbcrypto::Serial::DeserializeFromFile(std::string("secretKey") , SecretKey , lbcrypto::SerType::BINARY) == 0)

	{

		std::cerr << "Error getting key.\n";

		return 1;

	}

	if(lbcrypto::Serial::DeserializeFromFile(std::string("CC") , CryptoContext , lbcrypto::SerType::BINARY) == 0)

	{

		std::cerr << "Error getting CC.\n";

		return 2;

	}

	CryptoContext.BTKeyGen(SecretKey);

	std::cout << "Encrypting ...\n";

	lbcrypto::LWECiphertext DName[40];

	system("mkdir cts");

	char* fname = NULL;

	for(int i = 0 ; i < 40 ; i++)

	{

		DName[i] = CryptoContext.Encrypt(SecretKey , pDName[i]);

		asprintf(&fname , "cts/temp%d" , i);

		lbcrypto::Serial::SerializeToFile(fname , DName[i] , lbcrypto::SerType::BINARY);

	}

	system("zip -r cts cts");

	system("rm -f -R cts");

	std::cout << "Completed.\n";

	free(pDName);

	free(fname);

	return 0;

}



int fetchName(nameCipher* myCipher){

	system("unzip cts.zip");

	char* filename;

	bool check = 0;

	for(int i = 0 ; i < 8 ; i++)

	{

		for(int j = 0 ; j < 5 ; j++)

		{

			asprintf(&filename , "cts/temp%d" , i * 5 + j);

			check = lbcrypto::Serial::DeserializeFromFile(filename , myCipher->nc[i][j] , lbcrypto::SerType::BINARY);

			if(check == false)

			{

				std::cout << "Error when deserial file, name :" << filename << "\n";

			}

		}

	}

	free(filename);

	//system("rm -f -R cts");

	return 0;

}



int query(){

	DataBase mydb("encData");

	nameCipher mycipher;

	mydb.fetch();

	fetchName(&mycipher);

	char* filename;


	lbcrypto::LWEPublicKey publicKey;
	lbcrypto::Serial::DeserializeFromFile("myKey" , publicKey , lbcrypto::SerType::BINARY);
	lbcrypto::Serial::DeserializeFromFile("CC" , cryptoContext , lbcrypto::SerType::BINARY);
	lbcrypto::RingGSWACCKey refreshKey;
	lbcrypto::LWESwitchingKey ksKey;

	lbcrypto::Serial::DeserializeFromFile("rfKey" , refreshKey , lbcrypto::SerType::BINARY);
	lbcrypto::Serial::DeserializeFromFile("ksKey" , ksKey , lbcrypto::SerType::BINARY);

	cryptoContext.BTKeyLoad({refreshKey , ksKey});

	tempdata = mydb.get();

	num = tempdata.size();

	lbcrypto::LWECiphertext tempNameCipher[num][8][5];

	lbcrypto::LWECiphertext tempCaseCipher[num][3];

	lbcrypto::LWECiphertext tempLocCipher[num][8];

	lbcrypto::LWECiphertext tempTimeCipher[num][13];

	for(int i = 0;i <8 ;i++){

		for(int j = 0;j < 5;j++)

			qNameCipher[i][j] = mycipher.nc[i][j];

	}


	int thread = 8;

	std::vector <std::future <bool>> threads;

	blockSize = (num - 1) / thread + 1;
	lbcrypto::LWECiphertext cmpResult;
	puts("start querying....");	
   	system("mkdir queryData");
   	char* temp;
	asprintf(&temp , "queryData/length");

	FILE* fptr = fopen(temp , "wb");

	fprintf(fptr , "%d" , num);

	fclose(fptr);


	for(int row = 0 ; row < thread ; row++)	
	{
		threads.push_back(std::async([&](int row) {
			for(int b = 0 ; b < blockSize ; b++)
			{
				if(b + row * blockSize >= num)
				{
					break;
				}
				auto cmpResult = str_comp(tempdata[b + row * blockSize].nameCipher , qNameCipher , publicKey , cryptoContext);
				for(int byte = 0 ; byte < 8 ; byte++)	
				{

					for(int bit = 0 ; bit < 5 ; bit++)
					{
						tempNameCipher[b + row * blockSize][byte][bit] = cryptoContext.EvalBinGate(AND , cmpResult, tempdata[b + row * blockSize].nameCipher[byte][bit]);
                        asprintf(&filename , "queryData/%dN%02d" , b + row * blockSize , byte * 5 + bit);
                       	lbcrypto::Serial::SerializeToFile(filename , tempNameCipher[b + row * blockSize][byte][bit] , lbcrypto::SerType::BINARY);
					}

				}

				for(int bit = 0 ; bit < 3 ; bit++)
				{
					tempCaseCipher[b + row * blockSize][bit] = cryptoContext.EvalBinGate(AND , cmpResult, tempdata[b + row * blockSize].caseCipher[bit]);
					asprintf(&filename , "queryData/%dC%02d" , b + row * blockSize , bit);
					lbcrypto::Serial::SerializeToFile(filename , tempCaseCipher[b + row * blockSize][bit]  , lbcrypto::SerType::BINARY);
				}

				for(int bit = 0 ; bit < 8 ; bit++)
				{

					tempLocCipher[b + row * blockSize][bit] = cryptoContext.EvalBinGate(AND , cmpResult, tempdata[b + row * blockSize].locationCipher[bit]);
					asprintf(&filename , "queryData/%dL%02d" , b + row * blockSize , bit);
					lbcrypto::Serial::SerializeToFile(filename , tempLocCipher[b + row * blockSize][bit] , lbcrypto::SerType::BINARY);
				}

				for(int bit = 0 ; bit < 13 ; bit++)
				{
					tempTimeCipher[b + row * blockSize][bit] = cryptoContext.EvalBinGate(AND , cmpResult, tempdata[b + row * blockSize].timeCipher[bit]);
					asprintf(&filename , "queryData/%dT%02d" , b + row * blockSize , bit);
					lbcrypto::Serial::SerializeToFile(filename , tempTimeCipher[b + row * blockSize][bit] , lbcrypto::SerType::BINARY);
				}
			}
			return true;
		}, row));
	}



	for(int row = 0; row < thread; ++row) {

				threads[row].get();

		}


	return 0;

}



int keygen()

{

	std::cout << "Start generating the key...\n";

	auto CryptoContext = lbcrypto::BinFHEContext();

	CryptoContext.GenerateBinFHEContext(lbcrypto::MEDIUM);

	auto SecretKey = CryptoContext.KeyGen();
	CryptoContext.BTKeyGen(SecretKey , PUB_ENCRYPT);
	auto PublicKey = CryptoContext.GetPublicKey();

	std::cout << "Start saving the key...\n";

	if(lbcrypto::Serial::SerializeToFile(std::string("secretKey") , SecretKey , lbcrypto::SerType::BINARY) == 0)
	{
		std::cerr << "Error saving secret key.\n";
		return 1;
	}

	if(lbcrypto::Serial::SerializeToFile(std::string("CC") , CryptoContext , lbcrypto::SerType::BINARY) == 0)
	{
		std::cerr << "Error saving CC.\n";
		return 2;
	}

	if(lbcrypto::Serial::SerializeToFile(std::string("myKey") , PublicKey , lbcrypto::SerType::BINARY) == 0)
	{
		std::cerr << "Error saving public key.\n";
		return 3;
	}

	if(lbcrypto::Serial::SerializeToFile(std::string("rfKey") , CryptoContext.GetRefreshKey() , lbcrypto::SerType::BINARY) == 0)
	{
		std::cerr << "Error saving public key.\n";
		return 3;
	}

	if(lbcrypto::Serial::SerializeToFile(std::string("ksKey") , CryptoContext.GetSwitchKey() , lbcrypto::SerType::BINARY) == 0)
	{
		std::cerr << "Error saving public key.\n";
		return 3;
	}

	std::cout << "Completed.\n";

	return 0;

}



int encrypt(const char* dirName)

{

	lbcrypto::LWEPrivateKey sk;

	lbcrypto::BinFHEContext cc;

	lbcrypto::Serial::DeserializeFromFile("secretKey" , sk , lbcrypto::SerType::BINARY);

	lbcrypto::Serial::DeserializeFromFile("CC" , cc , lbcrypto::SerType::BINARY);

	std::vector <data_> data;

	FILE* fptr = fopen("data.csv" , "r");

	if(fptr == nullptr)

	{

		std::cout << "Error when open file " << "data.csv" << "\n";

		return 0;

	}

	for (int c = 0 ; (c = fgetc(fptr)) != EOF ; )

	{

		data_ temp;

		for(int j = 0 ; j < 9 ; j++)

		{

			temp.name[j] = 0;

		}

		for(int j = 0 ; c != ',' ; j++)

		{

			temp.name[j] = c;

			c = fgetc(fptr);

		}

		fscanf(fptr , "%d,%d,%d\n" , &(temp.caseNum) , &(temp.location) , &(temp.time));

		data.push_back(temp);

	}



	fclose(fptr);



	#if DEBUG



	for(auto i = data.begin() ; i != data.end() ; i++)

	{

		std::cout << i -> name << "\t";

		std::cout << i -> caseNum << "  ";

		std::cout << i -> location << "\t";

		std::cout << i -> time << "\n";

	}



	#endif



	cc.BTKeyGen(sk);

	char* temp;

	asprintf(&temp , "mkdir %s" , dirName);

	system(temp);

	asprintf(&temp , "%s/length" , dirName);

	fptr = fopen(temp , "wb");

	fprintf(fptr , "%zu" , data.size());

	fclose(fptr);



	int thread = 16;

	std::vector <std::future <bool>> threads;

	blockSize = (data.size() - 1) / thread + 1;



	#if DEBUG



	std::cout << "Data size : " << data.size() << "\n";

	std::cout << "Block size : " << blockSize << "\n";



	#endif



	for(int i = 0 ; i < thread ; i++)

	{

		threads.push_back(std::async([&](int i)

		{

			lbcrypto::LWECiphertext tempCipher;

			char* fileName = NULL;

			int decTime[13] = {0};

			int decCase[3] = {0};

			int decName[40] = {0};

			int decLocation[8] = {0};

			for(int b = 0 ; b < blockSize ; b++)

			{

				unsigned long int now = b + i * blockSize;

				if(now >= data.size())

				{

					break;

				}

				decodeName(data[now].name , decName);

				for(int j = 0 ; j < 40 ; j++)

				{

					asprintf(&fileName , "%s/%ldN%02d" , dirName , now , j);

					tempCipher = cc.Encrypt(sk , decName[j]);

					lbcrypto::Serial::SerializeToFile(fileName , tempCipher , lbcrypto::SerType::BINARY);

				}

				decodeCase(data[now].caseNum , decCase);

				for(int j = 0 ; j < 3 ; j++)

				{

					asprintf(&fileName , "%s/%ldC%02d" , dirName , now , j);

					tempCipher = cc.Encrypt(sk , decCase[j]);

					lbcrypto::Serial::SerializeToFile(fileName , tempCipher , lbcrypto::SerType::BINARY);

				}

				decodeTime(data[now].time , decTime);

				for(int j = 0 ; j < 13 ; j++)

				{

					asprintf(&fileName , "%s/%ldT%02d" , dirName , now , j);

					tempCipher = cc.Encrypt(sk , decTime[j]);

					lbcrypto::Serial::SerializeToFile(fileName , tempCipher , lbcrypto::SerType::BINARY);

				}

				decodeLocation(data[now].location , decLocation);

				for(int j = 0 ; j < 8 ; j++)

				{

					asprintf(&fileName , "%s/%ldL%02d" , dirName , now , j);

					tempCipher = cc.Encrypt(sk , decLocation[j]);

					lbcrypto::Serial::SerializeToFile(fileName , tempCipher , lbcrypto::SerType::BINARY);

				}

			}

			free(fileName);

			return true;

		} , i));		

	}



	for(int i = 0 ; i < thread ; i++)

	{

		threads[i].get();

	}



	asprintf(&temp , "zip -r %s %s" , dirName , dirName);

	system(temp);

	asprintf(&temp , "rm -f -R %s" , dirName);

	system(temp);

	free(temp);



	return 0;

}



int decrypt(const char* dirName)

{

	lbcrypto::LWEPrivateKey sk;

	lbcrypto::BinFHEContext cc;

	lbcrypto::Serial::DeserializeFromFile("secretKey" , sk , lbcrypto::SerType::BINARY);

	lbcrypto::Serial::DeserializeFromFile("CC" , cc , lbcrypto::SerType::BINARY);

	cc.BTKeyGen(sk);

	char* temp;

	asprintf(&temp , "unzip %s.zip" , dirName);

	system(temp);

	free(temp);

	std::vector <data_> data;

	FILE *fptr;

	int c;

    char* tempnum;

    asprintf(&tempnum ,"%s/length" , dirName);

    fptr = fopen(tempnum , "r");

    fscanf(fptr , "%d" , &c);

	fclose(fptr);

    fptr = fopen("Result.csv","w");

	int thread = 8;

	std::vector <std::future <bool>> threads;

	blockSize = (c - 1) / thread + 1;

	for(int i = 0 ; i < thread ; i++)

	{

		threads.push_back(std::async([&](int i)

		{

			lbcrypto::LWEPlaintext tempPlain;

			lbcrypto::LWECiphertext tempNameCipher[40];

			lbcrypto::LWECiphertext tempCaseCipher[3];

			lbcrypto::LWECiphertext tempLocationCipher[8];

			lbcrypto::LWECiphertext tempTimeCipher[13];

			char* fileName = NULL;

			int decTime[13] = {0};

			int decCase[3] = {0};

			int decName[40] = {0};

			int decLocation[8] = {0};

			char name[9] = {0};

			for(int b = 0 ; b < blockSize ; b++)

			{

				int now = b + i * blockSize;

				if(now >= c)

				{

					break;

				}

				

				for(int j = 0 ; j < 40 ; j++)

				{

					asprintf(&fileName , "%s/%dN%02d" , dirName , now , j);

					lbcrypto::Serial::DeserializeFromFile(fileName , tempNameCipher[j] , lbcrypto::SerType::BINARY);

					cc.Decrypt(sk , tempNameCipher[j] , &tempPlain);

					decName[j] = (int)tempPlain;					

				}

				encodeName(decName , name);

				for(int j = 0 ; j < 3 ; j++)

				{

					asprintf(&fileName , "%s/%dC%02d" , dirName , now , j);

					lbcrypto::Serial::DeserializeFromFile(fileName , tempCaseCipher[j] , lbcrypto::SerType::BINARY);

					cc.Decrypt(sk , tempCaseCipher[j] , &tempPlain);

					decCase[j] = (int)tempPlain;					

				}

				for(int j = 0 ; j < 8 ; j++)

				{

					asprintf(&fileName , "%s/%dL%02d" , dirName , now , j);

					lbcrypto::Serial::DeserializeFromFile(fileName , tempLocationCipher[j] , lbcrypto::SerType::BINARY);

					cc.Decrypt(sk , tempLocationCipher[j] , &tempPlain);

					decLocation[j] = (int)tempPlain;					

				}

				for(int j = 0 ; j < 13 ; j++)

				{

					asprintf(&fileName , "%s/%dT%02d" , dirName , now , j);

					lbcrypto::Serial::DeserializeFromFile(fileName , tempTimeCipher[j] , lbcrypto::SerType::BINARY);

					cc.Decrypt(sk , tempTimeCipher[j] , &tempPlain);

					decTime[j] = (int)tempPlain;					

				}

				fprintf(fptr , "%s,%d,%d,%d\n" , name , encodeCase(decCase) , encodeLocation(decLocation) , encodeTime(decTime));

				std::cout << name << "," << encodeCase(decCase) << "," << encodeLocation(decLocation) << "," << encodeTime(decTime) << std::endl;

			}

			

			free(fileName);

			return true;

		} , i));		

	}



	for(int i = 0 ; i < thread ; i++)

	{

		threads[i].get();

	}



	fclose(fptr);

	return 0;

}



int add()

{

	system("unzip insert.zip");

	int add = 0;

	FILE* fptr = fopen("insert/length" , "r");

	fscanf(fptr , "%d" , &add);

	fclose(fptr);



	int length = 0;

	fptr = fopen("encData/length" , "r+");

	fscanf(fptr , "%d" , &length);

	fseek(fptr , 0 , SEEK_SET);

	fprintf(fptr , "%d" , length + add);

	fclose(fptr);

	char* command;

	

	for(int i = 0 ; i < add ; i++)

	{

		for(int j = 0 ; j < 40 ; j++)

		{

			asprintf(&command , "cp insert/%dN%02d encData/%dN%02d" , i , j , length + i , j);

			system(command);

		}

		for(int j = 0 ; j < 3 ; j++)

		{

			asprintf(&command , "cp insert/%dC%02d encData/%dC%02d" , i , j , length + i , j);

			system(command);

		}

		for(int j = 0 ; j < 13 ; j++)

		{

			asprintf(&command , "cp insert/%dT%02d encData/%dT%02d" , i , j , length + i , j);

			system(command);

		}

		for(int j = 0 ; j < 8 ; j++)

		{

			asprintf(&command , "cp insert/%dL%02d encData/%dL%02d" , i , j , length + i , j);

			system(command);

		}

	}

	system("rm -f -R cts");

	free(command);

	return 0;

}


