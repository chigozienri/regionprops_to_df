# regionprops_to_df
Takes list containing regionprops objects output by skimage.measure.regionprops,
returns Pandas DataFrame of all non-dunder, non-hidden scalar and tuple attributes.

#regionprops_to_df_testing
Creates a RegionProps object from a skimage.data stock photo, median filtered.
The RegionProps object is then converted to a Pandas DataFrame with regionprops_to_df.
The functions in the testing script create arrays from the RegionProps object and compares them to
the Pandas DataFrame arrays.
