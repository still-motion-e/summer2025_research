import numpy as np
import pandas as pd
import sys
import math
import matplotlib.pyplot as plt

arg1 = sys.argv[1]

data = pd.read_csv(arg1, sep=' ')
#print(data)  #prints entire data file

'''
#proof of function for the math to work, it does and this returns a value of 15.544~
R_value = math.pow(data['Eta'].loc[data.index[1]]-data['Eta'].loc[data.index[0]],2) + math.pow(data['Phi'].loc[data.index[1]]-data['Phi'].loc[data.index[0]],2)
print(R_value) #please just work you beast of wires and circuitry
'''


test = []
for j in range(len(data)):                                                         #this loops through all the values using the length of the data table 
    test.append(math.pow(data['Eta'].loc[data.index[0]]-data['Eta'].loc[data.index[j]],2) + 
        math.pow(data['Phi'].loc[data.index[0]]-data['Phi'].loc[data.index[j]],2)) #this puts all the R^2 values into a list
smallest = min(filter(lambda x: x != 0, test))                                     #this picks out the smallest value in that smallest_1
print(smallest, "this is the smallest value")                                      #prints the value of the list
index = test.index(smallest)                                                       #picks out the index location of the other merged item that makes the lowest R^2
print(index, "this is the index location")

'''
#######this is a proof of function for the for loop aboves function
q_value = math.pow(data['Eta'].loc[data.index[0]]-data['Eta'].loc[data.index[34]],2) + math.pow(data['Phi'].loc[data.index[34]]-data['Phi'].loc[data.index[0]],2)
print(q_value, "index test")
'''

def min_finder():
    val = []                                                                                        #
    for j in range(len(data)):                                                                      #runs the legnth of the data
        val.append(math.pow(data['Eta'].loc[data.index[0]]-data['Eta'].loc[data.index[j]],2) +
            math.pow(data['Phi'].loc[data.index[0]]-data['Phi'].loc[data.index[j]],2))
    smallest_1 = min(filter(lambda x: x != 0, test))                                                #
    index_1 = val.index(smallest_1)                                                                 #
    return smallest_1, index_1, val                                                                 #

flamp, hell, splat = min_finder()                                                                   #these are joke names i am using to hold returned values
print(flamp, hell, "my function")

