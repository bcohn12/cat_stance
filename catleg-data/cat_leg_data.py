# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <markdowncell>

# # Exctracting the cat leg data
# 
# We want to extract the data from [Burkholder and Nichol's model](http://www.ncbi.nlm.nih.gov/pmc/articles/PMC2043500/) into simple manipulatable files. To do this, I first copied the HTML of all the tables into files `table_N.TITLE.html` where `N` is the table number (ranges from 1 to 6) and `TITLE` is the table title, with spaces replaced by underscores.
# 
# We then use `pandas.read_html` from the [pandas](http://pandas.pydata.org/) python library to extract the tabular data from each file.

# <codecell>

import pandas

# <markdowncell>

# ## Table 1: Definitions of segmential coordinates

# <codecell>

table_1 = pandas.read_html('table_1.Definitions_of_segmential_coordinates.html')[0]

# <codecell>

table_1

# <markdowncell>

# ## Table 2: Location and orientation of joint axes in segmential coordinates

# <codecell>

table_2a = pandas.read_html('table_2a.Location_and_orientation_of_joint_axes_in_segmental_coordinates.html', index_col=0)
print(len(table_2a))
table_2a = table_2a[0]
table_2a

# <markdowncell>

# Note that rows 0, 2, 6 and 11 are *title rows*. This data frame should probably be split.

# <codecell>

table_2b = pandas.read_html('table_2b.Location_of_pelvic_points.html', index_col=0, header=0)
table_2b = table_2b[0]
table_2b

# <markdowncell>

# ## Table 3: Location of femoral points

# <codecell>

table_3 = pandas.read_html('table_3.Location_of_femoral_points.html', index_col=0)
print(len(table_3)) # just to make sure there is only one table
table_3 = table_3[0]
table_3

# <markdowncell>

# Note that we have a bunch of `±` signs, so the X, Y and Z columns must be unicode strings by default. If we want to use this data, then we need to handle the `±` sign.

# <markdowncell>

# ## Table 4: Location of tibial points

# <codecell>

table_4 = pandas.read_html('table_4.Location_of_tibial_points.html', index_col=0)
print(len(table_4))
table_4 = table_4[0]
table_4

# <markdowncell>

# ## Table 5: Location of foot points

# <codecell>

table_5 = pandas.read_html('table_5.Location_of_foot_points.html', index_col=0)
print(len(table_5))
table_5 = table_5[0]
table_5

# <markdowncell>

# ## Table 6: Knee and ankle moment arms at stance configurations

# <codecell>

table_6 = pandas.read_html('table_6.Knee_and_ankle_moment_arms_at_stance_configuration.html', index_col=0)
print(len(table_6))
table_6 = table_6[0]
table_6

# <markdowncell>

# This data format allows us to enumerate the muscles and extract their moment arms.

# <codecell>

muscles = table_6.index
num_muscles = len(muscles)
print("Number of muscles: {0}".format(num_muscles))

# <codecell>

table_6.loc['ST']

