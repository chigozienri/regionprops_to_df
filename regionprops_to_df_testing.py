# -*- coding: utf-8 -*-
"""
Created on Sat Sep 26 12:51:16 2015

@author: anders
Written as testing for the regionprops_to_df module written by 
Chigozie Nri, Anders Knight, and Priya Choudhry 
as an offshoot of Justin Bois' BE 203 course at Caltech.

Currently runs one stock image (moon), though easily altered.
Next step in testing would be creating a function for testing an image
inputted by the end user.


"""
import regionprops_to_df
import numpy as np

#%%
#Generate im_props data from skimage stock

import skimage.filters
import skimage.measure
import skimage.data
import skimage.morphology

#Unsuccessful: astronaut, chelsea, coffee, horse, hubble_deep_field,
#immunohistochemistry, lena
#All unsuccessful have skimage files formatted differently
#(Print skimage.data to see the apparently 3D formatting of unsuccessfuls)
skimage_stock_photos = ['astronaut',
                        'camera',
                         'checkerboard',
                         'chelsea',
                         'clock',
                         'coffee',
                         'coins',
                         'horse',
                         'hubble_deep_field',
                         'immunohistochemistry',
                         'lena',
                         'moon',
                         'page',
                         'text']



#Select a (stock) image
skimage_stock = skimage.data.text()


#Use a median filter of square 3 on the stock image
selem = skimage.morphology.square(3)
im_filt = skimage.filters.median(skimage_stock, selem)

#Generate regionprops object
im_props = skimage.measure.regionprops(skimage_stock, intensity_image=im_filt)

#%%
# Unit testing

def regionprops_attribute_test(im_props, attr):
    '''Returns a pandas array for a given regionprops attribute
    (to compare to those from the module)
    The function was adapted from Justin Bois' BE 203 course material.
    '''
    
    proparray = []
    
    #Iterate through RegionProps object to 
    for prop, _ in enumerate(im_props):
        proparray.append(getattr(im_props[prop], attr))
    return proparray
    





def compare_module_to_loop(im_props, df_module, attribute):
    '''Compares the output of the module and a basic loop
    for a given attribute'''
    
    #Returns an array of the given attribute's data in im_props
    proparray = regionprops_attribute_test(im_props, attribute)
    
    #Returns a boolean of whether the arrays are matching    
    return np.all(proparray == getattr(df_module, attribute))
    
    
    
def compare_all_attributes(im_props, df_module):
    ''' Iterates through the attributes converted to a dataframe
    to validate the module. Also adds a fake attribute to ensure the 
    Attribute errors are printed to the screen.'''
    
    #Generate the attributes list (all non-dunder, non ndarray attributes)
    attributes_list = regionprops_to_df.scalar_attributes_list(im_props)
    
    #Add a fake attribute to the list to ensure it will be caught    
    attributes_list.append('Fake attribute test')
    validated_attributes = []
    print('If test runs properly, the only additional print should be:\
    \nFake attribute test is not in df_module (on next line).')
    for i, attribute in enumerate(attributes_list):
        try: 
            compare_module_to_loop(im_props, df_module, attribute)
            validated_attributes.append(attribute)
        except AttributeError:
            print(str(attribute) + ' is not in df_module.')
            pass
    
    #All validated attributes have equal arrays from both 
    return validated_attributes
    
#Executing scripts to generate the pandas df and validated attributes list
df_module = regionprops_to_df.regionprops_to_df(im_props)
validated_attributes = compare_all_attributes(im_props, df_module)   
    
'''
Supplemental aside:
As of this docstring (20150926) the function will convert all non-ndarray
data from RegionProps to ndarray. However, when written to file it will
write the tuples as one cell. This could be fixed by making separate columns
for the indices in each tuple.


The type of data returned from each RegionProps attribute

'area',                         float64
 'bbox',                        tuple       4        
 'centroid',                    tuple       2
 'convex_area',                 int64
 'convex_image',                ndarray
 'coords',                      ndarray
 'eccentricity',                float
 'equivalent_diameter',         float
 'euler_number',                int
 'extent',                      float64
 'filled_area',                 int64
 'filled_image',                ndarray
 'image',                       ndarray
 'inertia_tensor',              ndarray
 'inertia_tensor_eigvals',      tuple       2
 'intensity_image',             ndarray
 'label',                       int
 'local_centroid',              tuple       2
 'major_axis_length',           float
 'max_intensity',               uint8
 'mean_intensity',              float64
 'min_intensity',               uint8
 'minor_axis_length',           float
 'moments',                     ndarray
 'moments_central',             ndarray
 'moments_hu',                  ndarray
 'moments_normalized',          ndarray
 'orientation',                 float
 'perimeter',                   float64
 'solidity',                    float64
 'weighted_centroid',           tuple       2
 'weighted_local_centroid',     tuple       2
 'weighted_moments',            ndarray
 'weighted_moments_central',    ndarray
 'weighted_moments_hu',         ndarray
 'weighted_moments_normalized'  ndarray


tuples:
    bbox
    centroid
    inertia_tensor_eigvals
    local_centroid
    weighted_centroid
    weighted_local_centroid


'''