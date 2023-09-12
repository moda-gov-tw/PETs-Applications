# fhe-police
## Scene
This repository aims to simulate the application of fully homomorphic encryption (FHE) technique on criminal database. We will demonstrate how to use FHE technique to perform various database operations without decrypting the criminal data, such as counting the number of crimes or querying specific criminal data based on encrypted names.

## How to compile
### method 1:
step 1: 
Build and install OpenFHE using “make install”. If you don't know how to do it, please check
[OpenFHE documentation](https://openfhe-development.readthedocs.io/en/latest/sphinx_rsts/intro/installation/linux.html).

step 2:
Clone this repo.

step 3: 
Create the build directory from the root directory of this repo, and cd to it.
```
mkdir build
cd build
```
step 4: 
Run
```
cmake ..
```

step 5: 
Run “make” to build the executable.
```
make
```

### method 2
You can compile with run.sh:  
step 1: 
Build and install OpenFHE using “make install”. If you don't know how to do it, please check
[OpenFHE documentation](https://openfhe-development.readthedocs.io/en/latest/sphinx_rsts/intro/installation/linux.html).  
  
step 2:  
Clone this repo.

step 3:  
Change to the root directory of this repo.s
```
cd tfhe-rs
```

step 4:  
Run "run.sh". 
```
bash run.sh
```
If your shell is not bash shell, please use your own shell to run the file. Otherwise, please check if there is executable file "clang" and "clang++" in /usr/bin. If your executable file about clang is not named "clang" or "clang++", please modify "run.sh" in this repo to make the file name correspond to your clang file.

step 5:  
Change to build directory.
```
cd build
```

## Related settings
The deault security strength is MEDIUM

The deault thread number is 8

If you would like to run counter(), remember to add this statement to CMakeLists.txt.
```
target_link_libraries(server PRIVATE pthread)
```
web section url:
```
https://github.com/GGGCI/node.js
```
