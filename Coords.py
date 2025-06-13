import numpy as np
import sys
import math
import matplotlib.pyplot as plt

arg1 = sys.argv[1]
#print(arg1)

file_path = arg1

data = np.loadtxt(arg1)
#print(data[0,0])

x = math.exp(data[0,0]) + math.exp(data[0,0])
#print(x)
#print(data[:,2])
four_vect = np.empty((62,4)) #make adjustable

four_vect[0,3] = data[0,2] /(math.tan(2*math.atan(math.exp(-1 * data[0,0]))))
print(four_vect[0,3])

'''
four_vect[0,1] = data[0,2] * math.cos(data[0,1]) #building Px 
four_vect[0,2] = data[0,2] * math.sin(data[0,1]) #building Py 
four_vect[0,3] = data[0,2] /(math.tan(2*math.atan(math.exp(-1 * data[0,0])))) #building Pz
four_vect[0,0] = math.pow(four_vect[0,1],2) + math.pow(four_vect[0,2],2) + math.pow(four_vect[0,3],2)
print(four_vect[0,0:4])
'''

#print(four_vect[0,1])
for i in range(0,62):
    four_vect[i,1] = data[i,2] * math.cos(data[i,1]) #building Px 
    four_vect[i,2] = data[i,2] * math.sin(data[i,1]) #building Py 
    four_vect[i,3] = data[i,2] /(math.tan(2*math.atan(math.exp(-1 * data[i,0])))) #building Pz
    four_vect[i,0] = math.sqrt(math.pow(four_vect[i,1],2) + math.pow(four_vect[i,2],2) + math.pow(four_vect[i,3],2)+math.pow(data[i,3],2))
    #print(i)
    #print(four_vect[0,i])
    #print(four_vect[i,0:62])
mass = []
for j in range(62): #MAKE THIS VARIABLE WITH THE LENGTH OF THE LIST
    for k in range(j): #this prevents merging with self
        #print(j,k)
        #print(four_vect[j,0],four_vect[k,0])
        mass.append(math.sqrt(max(0.0,(math.pow(four_vect[j,0] + four_vect[k,0],2)-math.pow(four_vect[j,1]+four_vect[k,1],2)-
            math.pow(four_vect[j,2]+four_vect[k,2],2)-math.pow(four_vect[j,3]+four_vect[k,3],2))))) #LIMIT THE NUMBER OF DECIMALS
#print(mass)
print(len(mass))

#test_array = np.array(mass)
#print(test_array)

plt.hist(mass, bins = 25, range=[0,50])
plt.yscale('log')
plt.xlabel("mass(GeV)")  #ADD UNITS
plt.ylabel("number")
plt.show()

