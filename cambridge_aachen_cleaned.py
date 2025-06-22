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
    collider_coords = pd.concat([collider_coords,pd.DataFrame(args)], ignore_index=True) #it says this will stop being updated for something

    for q in range(len(collider_coords)):
        four_vect.loc[q,"Px"] = collider_coords.iloc[q,2] * math.cos(collider_coords.iloc[q,1])
        four_vect.loc[q,"Py"] = collider_coords.iloc[q,2] * math.sin(collider_coords.iloc[q,1])
        four_vect.loc[q,"Pz"] = collider_coords.iloc[q,2] / (math.tan(2*math.atan(math.exp(-1 * collider_coords.iloc[q,0]))))
        four_vect.loc[q,"E"] = math.sqrt(math.pow(four_vect.loc[q,"Px"],2)+math.pow(four_vect.loc[q,"Py"],2)+math.pow(four_vect.loc[q,"Pz"],2)+
            math.pow(collider_coords.loc[q,"Mass"],2))
    return four_vect

def collider_convert(args):
    c_coords = pd.DataFrame(columns=["Eta","Phi","PT","Mass"])
    four_v = pd.DataFrame()
    four_v = pd.concat([four_v,pd.DataFrame(args)], ignore_index=True) #it says this will stop being updated for something

    for i in range(len(four_v)):
        c_coords.loc[i,"PT"] = math.sqrt(math.pow(four_v.loc[i,"Px"],2)+math.pow(four_v.loc[i,"Py"],2))
        c_coords.loc[i,"Eta"] = -1 * math.log(math.tan((1/2)*math.atan2(c_coords.loc[i,"PT"],four_v.loc[i,"Pz"])))
        c_coords.loc[i,"Phi"] = math.atan2(four_v.loc[i,"Py"],four_v.loc[i,"Px"])
        c_coords.loc[i,"Mass"] = 0.0
    return c_coords

def merge_events(event_1,event_2):
    merged = pd.DataFrame(columns=("E","Px","Py","Pz"))
    merged.loc[0,"E"] = event_1.loc["E"] + event_2.loc["E"]
    merged.loc[0,"Px"] = event_1.loc["Px"] + event_2.loc["Px"]
    merged.loc[0,"Py"] = event_1.loc["Py"] + event_2.loc["Py"]
    merged.loc[0,"Pz"] = event_1.loc["Pz"] + event_2.loc["Pz"]
    return merged 


i = 0
merge_hold = [0]

while all(x >= 0.16 for x in merge_hold) == False:

    while i < len(data):    
        sml_R, index_loc, total, original_input = min_finder(i)
        if sml_R <= 0.16:
            #print("event",i,"and",index_loc,"would merge")
            fr_vct = four_vectorizer(data.iloc[i],data.iloc[index_loc])
            #print(fr_vct,"events",i,"&",index_loc,"as 4 vectors")
            mrgd = merge_events(fr_vct.iloc[0],fr_vct.iloc[1])
            #print(mrgd,"merged event in 4 vector")
            cc = collider_convert(mrgd)
            #print(cc,"back to collider coords")
            #print(original_input)
            data = data.drop([i])
            data = data.drop([index_loc])
            data = pd.concat([data,cc], ignore_index=True)
            i += 1
        else:
            #print("event ",i," and ",index_loc," would NOT merge")
            i += 1

    merge_hold.clear()
    for i in range(len(data)):
        a,b,c,d = min_finder(i)
        merge_hold.append(a)
    #print(merge_hold, "new mins")
    #print(all(x >= 0.16 for x in merge_hold),"should be true")
    i = 0
print(data)
print("this is the final result")
