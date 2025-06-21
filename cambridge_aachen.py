import numpy as np
import pandas as pd
import sys
import math
import matplotlib.pyplot as plt

arg1 = sys.argv[1]

data = pd.read_csv(arg1, sep=' ')
print(data)
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
        #c_coords.loc[i,"Mass"] = math.sqrt(math.pow(four_v.loc[i,"E"],2)-math.pow(four_v.loc[i,"Pz"],2)-math.pow(c_coords.loc[i,"PT"],2))
        c_coords.loc[i,"Mass"] = 0.0
    return c_coords

def merge_events(event_1,event_2):
    merged = pd.DataFrame(columns=("E","Px","Py","Pz"))
    merged.loc[0,"E"] = event_1.loc["E"] + event_2.loc["E"]
    merged.loc[0,"Px"] = event_1.loc["Px"] + event_2.loc["Px"]
    merged.loc[0,"Py"] = event_1.loc["Py"] + event_2.loc["Py"]
    merged.loc[0,"Pz"] = event_1.loc["Pz"] + event_2.loc["Pz"]
    return merged 

'''
maybe_thing = four_vectorizer(data.iloc[0], data.iloc[1], data.iloc[2])    #proof that my function is working to read in arguments and returns desired thing 
print(maybe_thing,"if this works then we got a function")
hold_this = collider_convert(maybe_thing)
print(hold_this,"should be back to collider coords")
'''

'''
for i in range(len(data)):
    small, index_location, total, returned_thing = min_finder(i)
    if small <= 0.16:
        print(i, "and", index_location, "would merge")
    else:
        print(i, "and", index_location, "would not merge")
'''#current working spot, come back to this
i = 0
#for i in range(len(data)):
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
        

    #collider_coords = pd.concat([collider_coords,pd.DataFrame(args)], ignore_index=True) #it says this will stop being updated for something


    else:
        
        print("event ",i," and ",index_loc," would NOT merge")
        i += 1
print(data)



'''working prototype    
small, index_location, total, returned_thing = min_finder(0)  
if small <= 0.16:
    print("0 and", index_location, "would merge")
    print(data.iloc[0], "0th row")
    print(data.iloc[index_location], index_location, "row")
    print(small)
    thonlk = four_vectorizer(data.iloc[0],data.iloc[index_location])
    print(thonlk)
    print(merge_events(thonlk.iloc[0],thonlk.iloc[1]), "merged events")
    print(thonlk.loc[0,"E"])
    

else:
    print(i, "and", index_location, "would not merge")
'''

