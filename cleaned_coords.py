'''
This is the guide to what each variable is refering to in the data provided
data[i,0] = Eta values
data[i,1] = Phi values
data[i.2] = Pt values
data[i,3] = Mass values

four_vect[i,0] = Energy
four_vect[i,1] = Px
four_vect[i,2] = Py
four_vect[i,3] = Pz
'''

import numpy as np
import sys
import math
import matplotlib.pyplot as plt

arg1 = sys.argv[1]

data = np.loadtxt(arg1)

four_vect = np.empty((62,4)) #make adjustable


for i in range(0,62):
    four_vect[i,1] = data[i,2] * math.cos(data[i,1]) #building Px -> Pt*Cos(Phi)
    four_vect[i,2] = data[i,2] * math.sin(data[i,1]) #building Py -> Pt*Sin(Phi)
    four_vect[i,3] = data[i,2] /(math.tan(2*math.atan(math.exp(-1 * data[i,0])))) #building Pz -> Pt/(tan(2tan^-1(e^(-Eta))))
    four_vect[i,0] = math.sqrt(math.pow(four_vect[i,1],2) + math.pow(four_vect[i,2],2) + math.pow(four_vect[i,3],2)+math.pow(data[i,3],2))
mass = []
for j in range(62): #MAKE THIS VARIABLE WITH THE LENGTH OF THE LIST
    for k in range(j): #this prevents merging with self
        mass.append(math.sqrt(max(0.0,(math.pow(four_vect[j,0] + four_vect[k,0],2)-math.pow(four_vect[j,1]+four_vect[k,1],2)-
            math.pow(four_vect[j,2]+four_vect[k,2],2)-math.pow(four_vect[j,3]+four_vect[k,3],2)))))
print(len(mass),"this is the length of the list of masses")

plt.hist(mass, bins = 25, range=[0,50])
plt.yscale('log')
plt.xlabel("mass(GeV)")
plt.ylabel("number")
plt.show()

