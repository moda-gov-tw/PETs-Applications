# fhe-police
## How to compile
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
