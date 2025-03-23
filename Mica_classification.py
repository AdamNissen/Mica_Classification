# -*- coding: utf-8 -*-
"""
Making a mica classification plot after Tischendorf et al., (2004, 2006).
"""


import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

#code from online
from collections import OrderedDict

linestyles = OrderedDict(
    [('solid',               (0, ())),
     ('loosely dotted',      (0, (1, 10))),
     ('dotted',              (0, (1, 5))),
     ('densely dotted',      (0, (1, 1))),

     ('loosely dashed',      (0, (5, 10))),
     ('dashed',              (0, (5, 5))),
     ('densely dashed',      (0, (5, 1))),

     ('loosely dashdotted',  (0, (3, 10, 1, 10))),
     ('dashdotted',          (0, (3, 5, 1, 5))),
     ('densely dashdotted',  (0, (3, 1, 1, 1))),

     ('loosely dashdotdotted', (0, (3, 10, 1, 10, 1, 10))),
     ('dashdotdotted',         (0, (3, 5, 1, 5, 1, 5))),
     ('densely dashdotdotted', (0, (3, 1, 1, 1, 1, 1)))])
#code from online over

#Adding point specifics
type_translator = {'1': ['Type 1', '^', 'C1'],
                   '2': ['Type 2', '+', 'C2'],
                   '3a': ['Type 3a', '2', 'C3'],
                   '3b': ['Type 3b', '1', 'C3'],
                   '4': ['Type 4', 'd', 'C0'],
                   '5': ['Type 5', 'o', 'C5'],
                   '5a': ['Type 5', 'o', 'C7'],
                   '5b': ['Type 5', 'o', 'C8'],
                   '6': ['Type 6', 's', 'C6']}


ALPHA = 1

def plot_micas(csv_path = None, data = None, save = False):

    if not isinstance(csv_path, type(None)):
        chem = pd.read_csv(csv_path)
        print('nice')
    elif not isinstance(data, type(None)):
        chem = data
    else:
        raise KeyError('Either a path to a csv must be entered, or a dataframe properly formtted must be entered')
        return
    
    #Calculating XY coordinates for each sample
    chem['x'] = chem['Mg_APFU'] - chem['Li_APFU']
    chem['y'] = chem['Fe(ii)_APFU'] + chem['Mn_APFU'] + chem['Ti_APFU'] - chem['Al (VI)_APFU']
    
    chem = chem.reset_index()
    #defining the figure and main axis
    fig, ax1 = plt.subplots()
    fig.set_size_inches(5,6)
    
    #Defining the inset
    x1, x2, y1, y2 = -0.3, 0.2, -4, -3.5
    axins = ax1.inset_axes([0.03, 0.695, 0.275, 0.275], xlim = (x1, x2), ylim = (y1, y2), xticklabels = [], yticklabels=[])

    for i in range(len(chem)):
        #Adding data to the main figure
        ax1.scatter(chem['x'][i], chem['y'][i], color = type_translator[chem['Mica_type'][i]][2], marker = type_translator[chem['Mica_type'][i]][1], alpha = ALPHA)#alpha = chem['Alpha'][i] )
        
        axins.scatter(chem['x'][i], chem['y'][i], color =  type_translator[chem['Mica_type'][i]][2], marker = type_translator[chem['Mica_type'][i]][1], alpha = ALPHA)#alpha = chem['Alpha'][i] )
        #ax2ins.scatter(chem['x'][i], chem['y'][i], color =  type_translator[chem['Mica type'][i]][2], marker = type_translator[chem['Mica type'][i]][1], alpha = ALPHA)#alpha = chem['Alpha'][i] )
    
    #Plotting the inset box
    ax1.plot([x1, x1, x2, x2,x1], [y1, y2, y2, y1, y1], '-', color = 'k')
    
    #The points for tischendorf 1997
    ax1.plot([-4, -2, 0, 6], [-2, 0, 6, 0], '-', color = 'dimgrey') #top limit
    ax1.plot([-4, -3, 0, 2, 4, 6], [-2, -3, -4, -2, -2, 0], '-', color = 'dimgrey') #bottom limit
    axins.plot([-4, -3, 0, 2, 4, 6], [-2, -3, -4, -2, -2, 0], '-', color = 'dimgrey') #bottom limit
    ax1.plot([-2.4, -2.4], [-0.375, -3.2], '--', color = 'dimgrey')#lepidolite bound
    ax1.plot([-2.4, 1], [-3, -3], '--', color = 'dimgrey')# muscovite upper
    ax1.plot([-0.4, -0.4] , [-3.87, 4], '--', color = 'dimgrey')# li bound
    ax1.plot([-1.4, -1.4, 0, 1.5, 2.9, 2.9, 2.4], [-3, -1, 0.4, 0.4, -1, -1.5, -2], linestyle = linestyles['densely dashdotted'], linewidth = 2.5 ,color = 'dimgrey')# trioctahedral bound
    ax1.plot([-1.4, -1.4], [-1, 1.8], '--', color = 'dimgrey')# zinwaldite/protolithionite bound
    ax1.plot([-0.67, 2], [4, 4], '--', color = 'dimgrey')# lepidomelane bound
    ax1.plot([0.6, 0.6], [0.4, 4], '--', color = 'dimgrey')# siderophyllite fe biotite bound
    ax1.plot([2, 2], [4, 0], '--', color = 'dimgrey')#Mg vs Fe biotite bound
    ax1.plot([2, 6], [0, 0], '--', color = 'dimgrey')#alumino bound
    ax1.plot([4, 4], [2, -2], '--', color = 'dimgrey')# plogopite biotite bound
    
    #labels for tischendorf 2004
    ax1.text(0.3, -1.25, "phengite", color = 'dimgrey', fontsize ='small')
    ax1.text(-0.3, -3.25, "muscovite", fontsize = 'xx-small', color = 'dimgrey')
    ax1.text(-2.0, -3.25, "Li-muscovite", fontsize = 'x-small', color = 'dimgrey')
    ax1.text(-1.1, 0.8, "protolithionite", fontsize = 'small', color = 'dimgrey', rotation = 270)
    ax1.text(-1.1, -2.4, "Li-phengite", fontsize = 'small', color = 'dimgrey', rotation = 270)
    ax1.text(-2.1, -2, "zinnwaldite", fontsize = 'small', color = 'dimgrey', rotation = 270)
    ax1.text(-0.1, 1.1, "siderophyllite", fontsize = 'small', color = 'dimgrey', rotation = 270)
    ax1.text(-3.8, -2, "lepidolite", fontsize = 'small', color = 'dimgrey')
    ax1.text(1.08, 2, "Fe-biotite", fontsize = 'small', color = 'dimgrey', rotation = 270)
    ax1.text(2.3, 1, "Mg-biotite", fontsize = 'small', color = 'dimgrey')
    ax1.text(4.15, 0.2, "phlogopite", fontsize = 'small', color = 'dimgrey')
    ax1.text(4.15, -0.3, "alumino-", fontsize = 'x-small', color = 'dimgrey')
    ax1.text(4.15, -0.5, "phlogopite", fontsize = 'x-small', color = 'dimgrey')
    ax1.text(2.7, -0.3, "alumino-", fontsize = 'x-small', color = 'dimgrey')
    ax1.text(2.7, -0.5, "Mg-biotite", fontsize = 'x-small', color = 'dimgrey')
    ax1.text(-0.4, 4.2, "lepidomelane", fontsize = 'small', color = 'dimgrey')

    #Setting plot limits
    plt.xlim(-4, 6)
    plt.ylim(-4, 6)
    
    #Labeling axes
    plt.xlabel ('Mg - Li apfu')
    plt.ylabel('Fe + Mn + Ti (-VI Al) apfu')
    
    #Making lables for the legend that match the labels in the plot
    handles, labels = plt.gca().get_legend_handles_labels()
    class_1 = Line2D([0], [0], label = 'Type 1', marker = '^', color = 'C1', alpha = ALPHA, linestyle = '')
    class_2 = Line2D([0], [0], label = 'Type 2', marker = '+', color = 'C2', alpha = ALPHA, linestyle = '')
    class_3 = Line2D([0], [0], label = 'Type 3a', marker = '2', color = 'C3', alpha = ALPHA, linestyle = '')
    class_4 = Line2D([0], [0], label = 'Type 3b', marker = '1', color = 'C3', alpha = ALPHA, linestyle = '')
    class_5 = Line2D([0], [0], label = 'Type 4', marker = 'd', color = 'C0', alpha = ALPHA, linestyle = '')
    class_6 = Line2D([0], [0], label = 'Type 5', marker = 'o', color = 'C5', alpha = ALPHA, linestyle = '')
    class_7 = Line2D([0], [0], label = 'Type 6', marker = 's', color = 'C6', alpha = ALPHA, linestyle = '')

    #adding a legend
    handles.extend([class_1, class_2, class_3, class_4, class_5, class_6, class_7])#, class_8, class_9])
    ax1.legend(handles = handles)
    
    #Defining tick marks
    axins.set_xticks([])
    axins.set_yticks([])
    
    #Making the layout nice and pretty
    fig.tight_layout()
    
    #Saving the figure
    if save == False:
        pass
    else:
        fig.savefig('Output/mica_classification.jpg', dpi = 300) 

if __name__ == "__main__":
#def main(name = "mica_classification"):
    icpms = pd.read_csv("Example_Data/Microprobe_Data.csv")       
    plot_micas(data = icpms, save = True)

    


