from random import randint
from time import localtime , strftime , mktime

names = []
with open("nameList" , "r") as f:
	temp = f.readlines()
	for n in temp:
		if len(n) <= 9:
			names.append(("").join([n[0] , n[1:-1].lower()]))
startDate = mktime((2008 , 1 , 1 , 0 , 0 , 0 , 0 , 0 , 0))
endDate = mktime((2023 , 12 , 31 , 23 , 59 , 59 , 0 , 0 , 0))

with open("data.csv" , "w") as f:
	for i in range(1000):
		dt = localtime(randint(startDate , endDate))
		n = names[randint(0 , len(names) - 1)]
		c = str(randint(0 , 7))
		l = str(randint(0 , 255))
		t = strftime("%Y%m%d\n" , dt)
		f.write((",").join([n , c , l , t]))
