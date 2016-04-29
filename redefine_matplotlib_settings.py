"""
Brian Blaylock
29 April 2016

Redefine some matplotlib default settings for 
publication quality figures.
"""

import matplotlib as mpl

# Specify universal figure sizes acceptable for publication
# J.AtmosEnv
#     Figure Page Width   |   Inches Wide       
#   ----------------------+---------------------
#   1/2 page (1 column)   |  3.54 in. ( 90 mm)   
#   3/4 page (1.5 column) |  5.51 in. (140 mm)    
#   1   page (2 column)   |  7.48 in. (190 mm)    
#   ---------------------------------------------
# Image Resolution:  line graphs : 1000 dpi
#                    colorfilled : 500 dpi         
#                    web images  : 72 dpi             

label_font  = 10    
tick_font   = 8 
legend_font = 7

width=3.5
height=3

## Reset the defaults
mpl.rcParams['axes.labelsize']  = label_font
mpl.rcParams['xtick.labelsize'] = tick_font
mpl.rcParams['ytick.labelsize'] = tick_font
mpl.rcParams['legend.fontsize'] = legend_font

mpl.rcParams['figure.figsize'] = [width,height] 

mpl.rcParams['grid.linewidth'] = .25

mpl.rcParams['savefig.bbox'] = 'tight'
mpl.rcParams['savefig.dpi'] = 1000
