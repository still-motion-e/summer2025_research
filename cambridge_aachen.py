import numpy as np
import pandas as pd
import sys
import math
import matplotlib.pyplot as plt

arg1 = sys.argv[1]

data = pd.read_csv(arg1, sep=' ')
#print(data)  #prints entire data file
'''
four = pd.DataFrame(columns=["E","Px","Py","Pz"])

print(data.iloc[0,2], "is PT") #is PT

four.loc[0,"Px"] = data.iloc[0,2] * math.cos(data.iloc[0,1])
four.loc[0,"Py"] = data.iloc[0,2] * math.sin(data.iloc[0,1])
four.loc[0,"Pz"] = data.iloc[0,2] / (math.tan(2*math.atan(math.exp(-1 * data.iloc[0,0]))))
four.loc[0,"E"] = math.sqrt(math.pow(four.loc[0,"Px"],2)+math.pow(four.loc[0,"Py"],2)+math.pow(four.loc[0,"Pz"],2)+math.pow(data.loc[0,"Mass"],2))
print(data.iloc[0,2] * math.cos(data.iloc[0,1]), "this is px")
print(four,"this is four")
'''
'''
#proof of function for the math to work, it does and this returns a value of 15.544~
R_value = math.pow(data['Eta'].loc[data.index[1]]-data['Eta'].loc[data.index[0]],2) + math.pow(data['Phi'].loc[data.index[1]]-data['Phi'].loc[data.index[0]],2)
print(R_value) #please just work you beast of wires and circuitry
'''

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


'''
#######this is a proof of function for the for loop aboves function
q_value = math.pow(data['Eta'].loc[data.index[0]]-data['Eta'].loc[data.index[34]],2) + math.pow(data['Phi'].loc[data.index[34]]-data['Phi'].loc[data.index[0]],2)
print(q_value, "index test")
'''

def min_finder(max_val):
    val = []                                                                                        #
    for j in range(len(data)):                                                                      #runs the legnth of the data
        val.append(math.pow(data['Eta'].loc[data.index[max_val]]-data['Eta'].loc[data.index[j]],2) +
            math.pow(data['Phi'].loc[data.index[max_val]]-data['Phi'].loc[data.index[j]],2))
    smallest_value = min(filter(lambda x: x != 0, val))                                             #the lambda function prevents self merger, which would = 0
    index = val.index(smallest_value)                                                               #finds the row that would be merged with
    return smallest_value, index, val, max_val                                                      #returns important values
#flamp, hell, splat, hell1 = min_finder(0)                                                          #these are joke names i am using to hold returned values
#print(flamp, hell, hell1, "my function")

def four_vectorizer(*args):
    collider_coords = pd.DataFrame(columns=["Eta","Phi","PT","Mass"])
    four_vect = pd.DataFrame(columns=["E","Px","Py","Pz"])
    collider_coords = pd.concat([collider_coords,pd.DataFrame(args)], ignore_index=True) #it says this will stop being updated for something 
    
    for q in range(len(collider_coords)):
        four_vect.loc[q,"Px"] = collider_coords.iloc[q,2] * math.cos(collider_coords.iloc[q,1])
        four_vect.loc[q,"Py"] = collider_coords.iloc[q,2] * math.sin(collider_coords.iloc[q,1])
        four_vect.loc[q,"Pz"] = collider_coords.iloc[q,2] / (math.tan(2*math.atan(math.exp(-1 * collider_coords.iloc[q,0]))))
        four_vect.loc[q,"E"] = math.sqrt(math.pow(four_vect.loc[q,"Px"],2)+math.pow(four_vect.loc[q,"Py"],2)+math.pow(four_vect.loc[q,"Pz"],2)+
            math.pow(collider_coords.loc[q,"Mass"],2))
        

    #print(args)
    #print(collider_coords, "should have 0 and 1")
    #print(four_vect,"this should have something in it???")
    return four_vect
#maybe_thing = four_vectorizer(data.iloc[0], data.iloc[1], data.iloc[2])    #proof that my function is working to read in arguments and returns desired thing 
#print(maybe_thing,"if this works then we got a function")


'''
for i in range(len(data)):
    small, index_location, total, returned_thing = min_finder(i)
    if small <= 0.16:
        print(i, "and", index_location, "would merge")
    else:
        print(i, "and", index_location, "would not merge")
'''#current working spot, come back to this

small, index_location, total, returned_thing = min_finder(0)
    
if small <= 0.16:
    print("0 and", index_location, "would merge")
    print(data.iloc[0], "0th row")
    print(data.iloc[index_location], index_location, "row")

else:
    print(i, "and", index_location, "would not merge")


