# -*- coding: utf-8 -*-
"""
Created on Wed Mar  9 15:37:11 2022

@author: soyrl
"""

#https://stackoverflow.com/questions/50655738/how-do-i-resolve-a-tesseractnotfounderror
import pytesseract 
# Set the path to Tesseract OCR executable
pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

import cv2
import numpy as np
import os
import pydicom as dicom
import time
import warnings

warnings.filterwarnings("ignore") # Ignore warnings in the code

start=time.time()

path_images="C:/Users/soyrl/Desktop/ocr/" #Path to DICOM slices

#Path to save line with nodule id
path_to_save="C:/Users/soyrl/Desktop/ocr_images/"

#Create this folder if it does not exist
if not os.path.exists(path_to_save):
    os.mkdir(path_to_save)

#Settings and characters that can be used to recognize the nodule id
custom_config = r'-c tessedit_char_whitelist=L0123456789 --oem 1 --psm 6'
L_nod_names=['L01','L02','L03','L04','L05','L06','L07','L08','L09','L10']
nod_names=['01','02','03','04','05','06','07','08','09','10']

#Initialize empty lists to be filled below with nodules and slices with errors
final_class={}
errors=[]

for file in os.listdir(path_images): #Loop through all DICOM slices

        path=path_images+file #Get the path of the current DICOM slice
    
        dicom_file_final=dicom.dcmread(path) #Read it
        img=dicom_file_final.pixel_array #Load pixel data
        
        img2=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #Convert to grayscale
        
        thresh = cv2.threshold(img2,150,255,cv2.THRESH_BINARY)[1] #Get a thresholded image with only nodules

        thresh=thresh[0:30,:] #Get first lines/rows of the image with the nodule id number
    
        #if this line contains a nodule id (it is not empty)    
        if (len(np.unique(thresh[0:30,50:150]))>1 and 
            len(np.where(thresh[0:30,50:150]==255)[0])>2):#and '5' in file.split('.')[4]:#'138' in file: #0,120
        
            print(file) #Print the file name/slice that contains the nodule id
            cv2.imwrite(path_to_save+str(file)+'.png',thresh) #Save yellow mask - range from 0-255
    
    
            #Get contours for each object and create a rectangle around them
            contours = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            contours = contours[0] if len(contours) == 2 else contours[1]
            ymin=1024
            ymax=0
            xmin=1024
            xmax=0
            
            Lclass=[]
            others=[]
            
            for cntr in contours:
                x,y,w,h = cv2.boundingRect(cntr)
                if x<xmin:
                    xmin=x
                if y<ymin:
                    ymin=y
                if x+w>xmax:
                    xmax=x+w
                if y+h>ymax:
                    ymax=y+h
                cv2.rectangle(img, (x-1, y-1), (x+w+1, y+h+1), (0, 0, 255), 1) #last argument thickness - was 2
          
                #Ensure that we are on the limits of the image
                if y-10<0:
                    new_y=0
                else:
                    new_y=y-10
                    
                character=img[new_y:y+h+10,x-10:x+w+10,:] #extract part of the image with the characters
                character = cv2.resize(character, (50, 50)) #resize image with the characters
                character2=cv2.cvtColor(character, cv2.COLOR_BGR2GRAY) #convert to gray

                #Use pytesseract for OCR
                if len(pytesseract.image_to_string(character2, config=custom_config))!=0:
                    for elem in pytesseract.image_to_string(character2, config=custom_config).split('\n'):
                        if elem in L_nod_names:
                            Lclass.append(elem)
                        elif elem in nod_names:
                            others.append(elem)

            #Just a check to confirm that we didn't miss characters
            if len(others)>len(Lclass):
                final_class[file.split('.')[4]]=others
            
            if Lclass in final_class.values() and len(Lclass)==1 and len(others)!=0:
                    for oelem in others:
                        if oelem not in list(final_class.values())[:-11]: 
                            final_class[file.split('.')[4]]=oelem
                           
                        else:
                            print('ERROR in {}'.format(file.split('.')[4]))
                            errors.append(file.split('.')[4])
            
            elif Lclass!=[] and file.split('.')[4] not in final_class:
                final_class[file.split('.')[4]]=Lclass
    
                
            print("\n")   
    
   
# Define a new list to store the modified values          
new_value=[] 

# Loop over the values of final_class dictionary
for slice_elem in list(final_class.values()):
    if isinstance(slice_elem, list):
        temp_list=[]
        for elem in slice_elem:
            if elem not in temp_list and 'L'+elem not in temp_list:
                if 'L' not in elem :
                    elem='L'+elem
                    temp_list.append(elem)
                else:
                    temp_list.append(elem)

        # Append the modified list to the new_value list                    
        new_value.append(temp_list)
    
    else:
        # If the value is not a list, modify it and append as a list to new_value
        if 'L' not in slice_elem :
            slice_elem='L'+slice_elem
            new_value.append(list([slice_elem]))
        else:
            new_value.append(list([slice_elem]))

# Update the values of final_class dictionary with the modified values in new_value                
for index,value in enumerate(new_value):
        final_class[list(final_class.items())[index][0]]=value

# Convert the sublists in new_value to single values, if possible
if isinstance(new_value[0],list):
    new_value=[elem[0] for elem in new_value]

# Define a list to store the unique nodules    
nodules=[]
# Get the unique values from new_value and store in nodules list
for unique in np.unique(new_value):
    for elem in unique:
        if elem not in nodules and elem.isdigit():
            nodules.append(elem)

nodules.sort() # Sort the nodules list

nod_num=[1,2,3,4,5,6,7,8,9,10] # Define the expected nodule ids

# Convert the nodules to integer values
for index,val in enumerate(nodules):
    nodules[index]=int(val[-2:])  
    
pos_errors=[] # Define a list to store the missing nodule ids
# Check for missing nodule ids
for miss_val in nod_num:
    if miss_val not in nodules:
        pos_errors.append(miss_val)
        
# Print the missing nodules information
if len(pos_errors)==1:
    print("Slices {} may contain nodule with id {}".format(errors,pos_errors[0]))
else:
    print("Slices with errors are {} and nodule ids that they might contain are {}".format(errors,pos_errors))
    
    
end=time.time()
print("Total time to run: {} sec".format(end-start))                
      