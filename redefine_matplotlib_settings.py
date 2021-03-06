"""
Brian Blaylock
29 April 2016

Redefine some matplotlib default settings for 
publication quality figures.
"""

import matplotlib as mpl

# Specify universal figure sizes acceptable for publication
    # J.AtmosEnv
    #        Figure width     |   Inches wide       
    #   ----------------------+---------------------
    #     minimumal size      |  1.18 in. ( 30 mm)
    #   1/2 page (1 column)   |  3.54 in. ( 90 mm)   
    #   3/4 page (1.5 column) |  5.51 in. (140 mm)    
    #   1   page (2 column)   |  7.48 in. (190 mm)    
    #   ---------------------------------------------
    # Image Resolution:  line drawing = 1000 dpi
    #                    colorfilled  = 500 dpi         
    #                    photographs  = 300 dpi                                 
    #                    for web      = 72 dpi

    label_font  = 10    
    tick_font   = 8 
    legend_font = 7
    
    width=3.5  # refer to above table
    height=3   # adjust as needed, but bbox="tight" should take care of most of this
    
    
    ## Reset the defaults (see more here: http://matplotlib.org/users/customizing.html)
    mpl.rcParams['xtick.labelsize'] = tick_font
    mpl.rcParams['ytick.labelsize'] = tick_font
    mpl.rcParams['axes.labelsize'] = label_font
    mpl.rcParams['legend.fontsize'] = legend_font
    
    mpl.rcParams['figure.figsize'] = [width,height] 
    
    mpl.rcParams['grid.linewidth'] = .25
    
    mpl.rcParams['savefig.bbox'] = 'tight'
    mpl.rcParams['savefig.dpi'] = 1000
