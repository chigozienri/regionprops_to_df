# -*- coding: utf-8 -*-
"""
Takes list containing regionprops objects output by
    skimage.measure.regionprops, converts to a Pandas DataFrame

Created on Fri Sep 18 21:53:42 2015

@author: Chigozie Nri, Anders Knight, Priya Choudhry
"""

import numpy as np
import pandas as pd


# Make list of all non-dunder attributes of regionprops object
def scalar_attributes_list(im_props):
    """
    Makes list of all scalar, non-dunder, non-hidden
    attributes of skimage.measure.regionprops object
    """
    attributes_list = []
    for i, test_attribute in enumerate(dir(im_props[0])):
        if test_attribute[:1] != '_' and \
                np.isscalar(getattr(im_props[0], test_attribute)):
            attributes_list += [test_attribute]
    return attributes_list


def regionprops_to_df(im_props):
    """
    Read content of all attributes for every item in a list
    output by skimage.measure.regionprops
    """

    attributes_list = scalar_attributes_list(im_props)

    # Initialise list of lists for parsed data
    parsed_data = []

    # Put data from im_props into list of lists
    for i, _ in enumerate(im_props):
        parsed_data += [[]]
        for j in range(len(attributes_list)):
            parsed_data[i] += [getattr(im_props[i], attributes_list[j])]

    # Return as a Pandas DataFrame
    return pd.DataFrame(parsed_data, columns=attributes_list)
