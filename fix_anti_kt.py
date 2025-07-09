'''
this only works for n = 0
'''
import numpy as np
import os
import pandas as pd
import sys
import math
import matplotlib.pyplot as plt
pd.set_option('display.precision',10)
arg1 = sys.argv[1]

data = pd.read_csv(arg1, sep=' ')
print(data, "this is our starting point")

n = int(sys.argv[2])

def min_finder(value):
    k = 0
    test_df = pd.DataFrame(columns=["R","Parent_1","Parent_2","PT_1","PT_2","min",'d'])

    stimp = []
    for j in range(value):
        for i in range(j):
            d_phi = np.abs(data['Phi'].loc[data.index[i]]-data['Phi'].loc[data.index[j]])
            d_eta = data['Eta'].loc[data.index[i]]-data['Eta'].loc[data.index[j]]
            if d_phi > np.pi:
                d_phi = 2*np.pi - d_phi
            test_df.loc[k,'R'] = (d_phi**2+d_eta**2)#*min(data['PT'].loc[data.index[i]]**-2,data['PT'].loc[data.index[j]]**-2)
            test_df.loc[k,'min'] = min(math.pow(data['PT'].loc[data.index[i]],n),math.pow(data['PT'].loc[data.index[j]],n))
            test_df.loc[k,'Parent_1'] = i
            test_df.loc[k,'Parent_2'] = j
            test_df.loc[k,'PT_1'] = data['PT'].loc[data.index[i]]
            test_df.loc[k,'PT_2'] = data['PT'].loc[data.index[j]]
            test_df.loc[k,'d'] = test_df.loc[k,'R']*test_df.loc[k,'min']

            k += 1
    test_df = test_df.sort_values(by='d')
    test_df = test_df.reset_index(drop = True)
    #print(test_df)
    return test_df

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
    
    #print(collider_coords,"the input")
    #print(four_vect,"the output")
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


#print(min_finder(len(data)),"this is all of our important values")

#d_values = min_finder(len(data))
#print(d_values)

#print(d_values['d'].min())
#data = pd.concat([data,four_vecterizer_df(data)],axis=1)
#print(data.loc[0])
#print(data.loc[0])
#print(four_vectorizer(data.iloc[0]),"this should be the first one")
flag = 0
#while d_values['d'].min() < 0.16:
while flag < 0.16:
    #break
    inner_d = min_finder(len(data))
    flag = inner_d['d'].min()
    #print(flag,"this is the flag!!!")
    if flag <= 0.16:
        four_holder = pd.DataFrame(columns=["E","Px","Py","Pz"])
        four_holder = pd.concat([four_vectorizer(data.loc[inner_d.loc[0,'Parent_1']]),four_holder],ignore_index=True)
        four_holder = pd.concat([four_vectorizer(data.loc[inner_d.loc[0,'Parent_2']]),four_holder],ignore_index=True)
        #print(four_holder,"should be data frame with desired merge events")
        #mrgd_event = merge_events(four_vectorizer(data.loc[inner_d.loc[0,'Parent_1']]),four_vectorizer(data.loc[inner_d.loc[0,'Parent_2']])) #this grabs the desired rows from data, like saying merge data[0] and data[1]
        mrgd_2 = merge_events(four_holder.loc[0],four_holder.loc[1])
        col_merged = collider_convert(mrgd_2)
        #print(col_merged)
        data = data.drop([inner_d.loc[0,'Parent_1'],inner_d.loc[0,'Parent_2']]) #drops the rows by number index
        data = pd.concat([data,col_merged],ignore_index=True)
        print(inner_d)
        #print(inner_d.sort_values(by='R'))
        print(flag)
        print(data)
    elif flag > 0.16:
        print("the buck stops here")
        break
    else:
        print(data)
        print("something went wrong again")
        break








'''
hole = min_finder(len(data))

print(any(x < 0.16 for x in hole.loc[:,'R']))
print(hole.loc[:,'R'])
print(hole)

data = pd.concat([data, four_vecterizer_df(data)],axis=1)
donors = pd.DataFrame(columns=['made_from'])
data = pd.concat([data,donors],axis=1)
data['made_from'] = [[] for _ in range(len(data))]
print(data,"quit here")
hold = 0
skank = []
while hold < 0.16:
    #######while any(x < 0.16 for x in hole.loc[:.'R']):
    slam = min_finder(len(data))
    print(slam)
    print(len(slam))
    print(slam.loc[0,'R'],"what is going on here")
    hold = (slam.loc[0,'R'])
    #print(hold,"this is the hold value")
    #print(slam.loc[0,'R'],"this is what i want to hold value to be")
    #if hold > 0.16:
        #break

    if hold <= 0.16:
        skank.append(slam.loc[0,'R'])
        #######print("merging",data.iloc[slam.loc[0,'Parent_1']],"and",data.iloc[slam.loc[0,'Parent_2']])
        mrgd = merge_events(data.iloc[slam.loc[0,'Parent_1']],data.iloc[slam.loc[0,'Parent_2']])
        mrgd_col = collider_convert(merge_events(data.iloc[slam.loc[0,'Parent_1']],data.iloc[slam.loc[0,'Parent_2']]))
        ########print(mrgd,"this is the magic")
        data = data.drop([slam.loc[0,'Parent_1'],slam.loc[0,'Parent_2']])
        data = pd.concat([data,pd.concat([mrgd,mrgd_col],axis=1)],ignore_index=True)
        ########data.loc[0,'made_from'].append(5)
        ########print(data,"this is the data")
        ########print(len(data))
        ########print("working")
    else:
        print("thats all folks")

print(data.sort_values(by=('Mass')))
'''
        

