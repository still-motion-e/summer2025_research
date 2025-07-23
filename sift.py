import numpy as np
import os
import pandas as pd
import sys
import math

arg1 = sys.argv[1]

data = pd.read_csv(arg1, sep=' ')
print(data, "this is our starting point")

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

def sift_measure(object_A,object_b):


