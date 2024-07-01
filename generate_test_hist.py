# -*- coding: utf-8 -*-
"""generate test hist.ipynb


"""

# Importing the required libraries

import numpy as np
import cv2
import os
import pickle
import sys
from scipy import ndimage
from scipy.spatial import distance
from sklearn.cluster import KMeans
from sklearn.cluster import MiniBatchKMeans

n_classes=36
clustering_factor=6

def surf_features(images):
  surf_vectors_list={}
  surf_descriptors_list=[]
  surf=cv2.xfeatures2d.SURF_create()
  for key,value in images.items():
    print(key, "Started")
    features=[]
    for img in value:
      kp,desc=surf.detectAndCompute(img,None)
      surf_descriptors_list.extend(desc)
      features.append(desc)
    surf_vectors_list[key]=features
    print(key," Completed!")
  return [surf_descriptors_list,surf_vectors_list]

# Loading train images into dictionaries which holds all images category by category

def load_images_by_category(folder):
  images={}
  for label in os.listdir(folder):
    print(label," started")
    category=[]
    path=folder+'/'+label
    for image in os.listdir(path):
      img=cv2.imread(path+'/'+image)
      new_img=cv2.resize(img,(128,128))
      if new_img is not None:
        category.append(new_img)
    images[label]=category
    print(label, "ended")
  return images

# Creating histograms for train images

# Function takes 2 parameters. The first one is a dictionary that holds the descriptors that are separated class by class 
# And the second parameter is the clustered model
# Returns a dictionary that holds the histograms for each images that are separated class by class. 

def create_histogram(all_bows,kmeans):
  features_dict={}
  for key,value in all_bows.items():
    print(key," Started!")
    category=[]
    for desc in value:
      visual_words=kmeans.predict(desc)
      hist = np.array(np.bincount(visual_words,minlength=n_classes*clustering_factor))
      category.append(hist)
    features_dict[key]=category
    print(key," Completed!")
  return features_dict

test_folder='ISL Datasets/Train-Test/Test'

# Loading Test images
test_images=load_images_by_category(test_folder)

#Extract SURF features from the image
surf_test=surf_features(test_images)[1]

#print(len(surf_test['a'][0]))

# Create histograms from extracted surf features
bows_test=create_histogram(surf_test,kmeans)

import csv
loc='cnn files/test.csv'
with open(loc,'w',newline='') as file:
  writer=csv.writer(file)
  header=[]
  for i in range (1,n_classes*clustering_factor+1):
    header.append(str('pixel')+str(i))
  header.append('Label')
  writer.writerow(header)
  count=0
  for label in bows_test:
    #print(len(bows_test[label]))
    for i in range(len(bows_test[label])):
      list=[]
      for j in range(150):
        list.append(bows_test[label][i][j])
      list.append(label)
      writer.writerow(list)
