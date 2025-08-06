#This is an implementation of the anti-kt jet clustering algorithm
#above each line where it is relevent i will include a comment with the same tab indenting as the line it is assigned to
#hopefully these comments help explain each line


import numpy as np
import os
import pandas as pd
import sys
import math
#this allows is to read in the desired text file
arg1 = sys.argv[1]

#this converts the text file that was openend previously into a dataframe for easily manipulation
#currently it is set up for a text file with a header
#if your text file has no header, adjust as needed
data = pd.read_csv(arg1, sep=' ')
#this print statment prints out the original data file you read into the program to check and make sure it is correct
#this is not important to operation and can be removed without consequence
print(data, "this is our starting point")

#this function will find smallest distance between two particles as described in the anti-kt paper
#It will also find the smallest distance between the a particle and the Beam, as described in the anti-kt paper
#it requires two inputs, the first one labeled "value" is how much of the data it will run over: it is almost always best to use the entire length of the data
#the second input, labeled "cone" will be the cone radius, often set to 0.4 -> 0.4^2 = 0.16
def min_finder(value,cone):
    k = 0
    distance = float('inf')
    parent_i = 0
    parent_j = 0
    smallest_PT2 = float('inf')
    smallest_PT2_parent = 0

    stimp = []
    for j in range(value):
        if data['PT'].loc[data.index[j]]**-2 < smallest_PT2:
            smallest_PT2 = data['PT'].loc[data.index[j]]**-2
            smallest_PT2_parent = j
        for i in range(j):
            d_phi = np.abs(data['Phi'].loc[data.index[i]]-data['Phi'].loc[data.index[j]])
            d_eta = data['Eta'].loc[data.index[i]]-data['Eta'].loc[data.index[j]]

            if d_phi > np.pi:
                d_phi = 2*np.pi - d_phi
            r_value = (d_phi**2+d_eta**2)#*min(data['PT'].loc[data.index[i]]**-2,data['PT'].loc[data.index[j]]**-2)
            
            distance_d = min(math.pow(data['PT'].loc[data.index[i]],-2),math.pow(data['PT'].loc[data.index[j]],-2))*(r_value)/cone
            if distance_d < distance:
                distance = distance_d
                parent_j = j
                parent_i = i
            k += 1
    return distance, parent_i, parent_j, smallest_PT2, smallest_PT2_parent

def four_vecterizer_df(df):
    collider_coords = pd.DataFrame(columns=["Eta","Phi","PT","Mass"])
    four_vect = pd.DataFrame(columns=["E","Px","Py","Pz"])
    collider_coords  = pd.concat([collider_coords,df], ignore_index=True)
    
    for q in range(len(collider_coords)):
        four_vect.loc[q,"Px"] = collider_coords.loc[q,'PT'] * math.cos(collider_coords.loc[q,'Phi'])     # Px = Pt*Cos(Phi)
        four_vect.loc[q,"Py"] = collider_coords.loc[q,'PT'] * math.sin(collider_coords.loc[q,'Phi'])     # Py = Pt*Sin(Phi)
        four_vect.loc[q,"Pz"] = collider_coords.loc[q,'PT'] / (math.tan(2*math.atan(math.exp(-1 * collider_coords.loc[q,'Eta'])))) #Pz = Pt/(tan(2tan^-1(e^(-Eta))))
        four_vect.loc[q,"E"] = math.sqrt(math.pow(four_vect.loc[q,"Px"],2)+math.pow(four_vect.loc[q,"Py"],2)+math.pow(four_vect.loc[q,"Pz"],2)+
            math.pow(collider_coords.loc[q,"Mass"],2)) #Energy is built from the momentum componants
    return four_vect

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
        c_coords.loc[i,"PT"] = math.sqrt(math.pow(four_v.loc[i,"Px"],2)+math.pow(four_v.loc[i,"Py"],2)) # Pt = sqrt(Px^2+Py^2)
        c_coords.loc[i,"Eta"] = -1 * math.log(math.tan((1/2)*math.atan2(c_coords.loc[i,"PT"],four_v.loc[i,"Pz"]))) # Eta = -ln(tan((1/2)*(tan^-1(Pt/Pz))))
        c_coords.loc[i,"Phi"] = math.atan2(four_v.loc[i,"Py"],four_v.loc[i,"Px"])                   # Phi = tan^-1(Py/Px)
        c_coords.loc[i,"Mass"] = math.sqrt(math.pow(four_v.loc[i,'E'],2)-math.pow(four_v.loc[i,'Pz'],2)-math.pow(c_coords.loc[i,'PT'],2))
    return c_coords

def merge_events(event_1,event_2):                          #Merges two events E+E,Px+Px,Py+Py,Pz+Pz, and returns the single remaining object
    merged = pd.DataFrame(columns=("E","Px","Py","Pz"))
    merged.loc[0,"E"] = event_1.loc["E"] + event_2.loc["E"]
    merged.loc[0,"Px"] = event_1.loc["Px"] + event_2.loc["Px"]
    merged.loc[0,"Py"] = event_1.loc["Py"] + event_2.loc["Py"]
    merged.loc[0,"Pz"] = event_1.loc["Pz"] + event_2.loc["Pz"]
    return merged



jets = pd.DataFrame(columns=["Eta","Phi","PT","Mass"])
merge = True
merge_history = []
step_counter = 1

while merge == True:
    if len(data) == 1:
        print(jets)
        print(data,"remaining data")
        for item in merge_history:
            print(item)
        break
    d_value, parent_i, parent_j, smallest_PT2, pt2_parent = min_finder(len(data),0.16)
    #print(d_value,parent_i,parent_j,smallest_PT2, pt2_parent)

    if (d_value < smallest_PT2):
        words = "step: " + str(step_counter) + ". merging objects " + str(parent_j) + " & " + str(parent_i)
        step_counter += 1
        merge_history.append(words)
        four_holder = pd.DataFrame(columns=["E","Px","Py","Pz"])
        four_holder = pd.concat([four_vectorizer(data.iloc[parent_j]),four_holder],ignore_index=True)
        four_holder = pd.concat([four_vectorizer(data.iloc[parent_i]),four_holder],ignore_index=True)
        merge_2 = merge_events(four_holder.iloc[0],four_holder.iloc[1])
        colider_merge_2 = collider_convert(merge_2)
        #data = data.drop([data.iloc[parent_i],data.iloc[parent_j]])
        data = data.drop(index=[parent_i,parent_j])
        #data = data.drop([d_values.loc[0,'Parent_i'],d_values.loc[0,'Parent_j']]) #drops the rows by number index
        data = pd.concat([data,colider_merge_2],ignore_index=True)
    if (d_value > smallest_PT2):
        #print("declaring jet from object",data['PT'].idxmax())
        merge_words = "step: " +str(step_counter)+ ". declaring jet from object " + str(pt2_parent)
        merge_history.append(merge_words)
        step_counter += 1
        jets = pd.concat([jets,data.iloc[[pt2_parent]]],ignore_index=True, axis = 0)
        data = data.drop(data.index[pt2_parent])
        data = data.reset_index(drop = True)
    

