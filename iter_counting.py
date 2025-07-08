
import numpy as np
import sys
import math
import matplotlib.pyplot as plt
import itertools

arg1 = sys.argv[1]

arg2 = int(sys.argv[2])

data = np.loadtxt(arg1)

for i in range(2, arg2+1):
    print(i, "combo options")

length = []
for i in range(0,62):
    length.append(i)
    i += 1
print(length)

four_vect = np.empty((62,4)) #make adjustable

for i in range(0,62):
    four_vect[i,1] = data[i,2] * math.cos(data[i,1]) #building Px -> Pt*Cos(Phi)
    four_vect[i,2] = data[i,2] * math.sin(data[i,1]) #building Py -> Pt*Sin(Phi)
    four_vect[i,3] = data[i,2] /(math.tan(2*math.atan(math.exp(-1 * data[i,0])))) #building Pz -> Pt/(tan(2tan^-1(e^(-Eta))))
    four_vect[i,0] = math.sqrt(math.pow(four_vect[i,1],2) + math.pow(four_vect[i,2],2) + math.pow(four_vect[i,3],2)+math.pow(data[i,3],2))
mass = []


for i in range(2, arg2+1):
    print(i,"this is my iteration tool")
    for combo in itertools.combinations(length,arg2):
        g = list(combo)
        en = []
        px = []
        py = []
        pz = []
        for t in range(len(g)):
            print(len(g))
            print(g)
            en.append(four_vect[g[t],0])
            px.append(four_vect[g[t],1])
            py.append(four_vect[g[t],2])
            pz.append(four_vect[g[t],3])
        print(en,"these are my enegy values",g)
        
        mass.append(math.sqrt(max(0.0,(math.pow(sum(en),2)-math.pow(sum(px),2)-math.pow(sum(py),2)-math.pow(sum(pz),2)))))
        #mass.append(math.sqrt(max(0.0,(math.pow(four_vect[g[0],0] + four_vect[g[1],0],2)-math.pow(four_vect[g[0],1]+four_vect[g[1],1],2)-
            #math.pow(four_vect[g[0],2]+four_vect[g[1],2],2)-math.pow(four_vect[g[0],3]+four_vect[g[1],3],2)))))
    #print(len(mass),"length of mass list")

    plt.hist(mass, bins = 25, range=[0,50])
    plt.yscale('log')
    plt.xlabel("mass(GeV)")
    plt.ylabel("number")
    plt.show()
    mass.clear()
