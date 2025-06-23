'''

'''
import numpy as np
import pandas as pd
import sys
import math
import matplotlib.pyplot as plt

arg1 = sys.argv[1]

data = pd.read_csv(arg1, sep=' ')
print(data, "this is our starting point")

def min_finder(max_val):
    val = []                                                                                        #
    for j in range(len(data)):                                                                      #runs the legnth of the data
        val.append(math.pow(data['Eta'].loc[data.index[max_val]]-data['Eta'].loc[data.index[j]],2) +
            math.pow(data['Phi'].loc[data.index[max_val]]-data['Phi'].loc[data.index[j]],2))
    smallest_value = min(filter(lambda x: x != 0, val))                                             #the lambda function prevents self merger, which would = 0
    index = val.index(smallest_value)                                                               #finds the row that would be merged with
    return smallest_value, index, val, max_val                                                      #returns important values

def four_vectorizer(*args):
    collider_coords = pd.DataFrame()
    four_vect = pd.DataFrame(columns=["E","Px","Py","Pz"])
    collider_coords = pd.concat([collider_coords,pd.DataFrame(args)], ignore_index=True)            #it says this will stop being updated for something

    for q in range(len(collider_coords)):
        four_vect.loc[q,"Px"] = collider_coords.iloc[q,2] * math.cos(collider_coords.iloc[q,1])     # Px = Pt*Cos(Phi)
        four_vect.loc[q,"Py"] = collider_coords.iloc[q,2] * math.sin(collider_coords.iloc[q,1])     # Py = Pt*Sin(Phi)
        four_vect.loc[q,"Pz"] = collider_coords.iloc[q,2] / (math.tan(2*math.atan(math.exp(-1 * collider_coords.iloc[q,0])))) #Pz = Pt/(tan(2tan^-1(e^(-Eta))))
        four_vect.loc[q,"E"] = math.sqrt(math.pow(four_vect.loc[q,"Px"],2)+math.pow(four_vect.loc[q,"Py"],2)+math.pow(four_vect.loc[q,"Pz"],2)+
            math.pow(collider_coords.loc[q,"Mass"],2)) #Energy is built from the momentum componants
    return four_vect

def collider_convert(args):
    c_coords = pd.DataFrame(columns=["Eta","Phi","PT","Mass"])
    four_v = pd.DataFrame()
    four_v = pd.concat([four_v,pd.DataFrame(args)], ignore_index=True) #it says this will stop being updated for something

    for i in range(len(four_v)):
        c_coords.loc[i,"PT"] = math.sqrt(math.pow(four_v.loc[i,"Px"],2)+math.pow(four_v.loc[i,"Py"],2)) # Pt = sqrt(Px^2+Py^2)
        c_coords.loc[i,"Eta"] = -1 * math.log(math.tan((1/2)*math.atan2(c_coords.loc[i,"PT"],four_v.loc[i,"Pz"]))) # Eta = -ln(tan((1/2)*(tan^-1(Pt/Pz))))
        c_coords.loc[i,"Phi"] = math.atan2(four_v.loc[i,"Py"],four_v.loc[i,"Px"])                   # Phi = tan^-1(Py/Px)
        c_coords.loc[i,"Mass"] = 0.0                                                                # Hard set the mass to 0, i was getting extra float 
    return c_coords

def merge_events(event_1,event_2):                          #Merges two events E+E,Px+Px,Py+Py,Pz+Pz, and returns the single remaining object
    merged = pd.DataFrame(columns=("E","Px","Py","Pz"))
    merged.loc[0,"E"] = event_1.loc["E"] + event_2.loc["E"]
    merged.loc[0,"Px"] = event_1.loc["Px"] + event_2.loc["Px"]
    merged.loc[0,"Py"] = event_1.loc["Py"] + event_2.loc["Py"]
    merged.loc[0,"Pz"] = event_1.loc["Pz"] + event_2.loc["Pz"]
    return merged 


i = 0           #counter 
merge_hold = [0]            #this holds R^2 values for each subsequent pass

while all(x >= 0.16 for x in merge_hold) == False:          #once all R^2 values are in range, stop merging

    while i < len(data):                                                    #runs to the end list and then ends
        sml_R, index_loc, total, original_input = min_finder(i)             #getting the R^2 value for each possible combo 
        if sml_R <= 0.16:                                                   #merge condition
            fr_vct = four_vectorizer(data.iloc[i],data.iloc[index_loc])     #convert merging events to 4 vectors
            mrgd = merge_events(fr_vct.iloc[0],fr_vct.iloc[1])              #merge the two events as 4 vectors
            cc = collider_convert(mrgd)                                     #convert back to collider coordinates
            data = data.drop([i])                                           #drop the the merged objects
            data = data.drop([index_loc])                                   #drop the merged objects
            data = pd.concat([data,cc], ignore_index=True)                  #add the new object to the end of the original_input
            i += 1                                                          #add one to the counter
        else:                                                                   #does not meet merge condition
            i += 1                                                              #add one to the counter

    merge_hold.clear()                                                      #after each pass, clear the previous R^2 values
    for i in range(len(data)):                                              #use the current length of the data as loop length
        a,b,c,d = min_finder(i)                                             #find the the lowest R^2 values off all possible combos
        merge_hold.append(a)                                                #put all those R^2 values into the list to use
    i = 0                                                                   #reset counter
print(data)
print("this is the final result")                                           #print final results
