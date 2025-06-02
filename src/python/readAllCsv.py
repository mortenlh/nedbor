import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
import sys
import modules.nedborUtils as nedbor

language = sys.argv[1] if len(sys.argv)>1 else 'none'

csvPath = "../../data/"
nbu = nedbor.NedborUtil(csvPath)
csvfiles = nbu.getNedborFiles()

months = np.array(['jan','feb','mar','apr','maj','jun','jul','aug','sep','okt','nov','dec'])

colors = []
for k in range(12):
    colors.append('#448aff')

mdata = np.zeros( (len(months),len(csvfiles)) )

subplotcols = 3
subplotrows = math.floor(len(csvfiles)/subplotcols) + 2

for i,file in enumerate(csvfiles):
    f = csvPath + file
    ftext = str(file)[1:-4]
    fdata = pd.read_csv(f, delimiter=';', header=None)
    fvalues = fdata[1].to_numpy()
    monthsdata = np.zeros(12)
    marray = []   
    for j,fv in enumerate(fvalues):        
        if pd.isna(fv):
            val = 0
            mdata[j, i] = -1.0            
        else:
            val = fv       
            marray.append(val)
            mdata[j, i] = float(val)        
        monthsdata[j] = float(val)            
        colors[j] = '#448aff' if val<100 else '#0d47a1'        
    
    mean = np.mean(marray) # monthsdata might not be a whole year. use marray instaed
    mead = np.median(np.sort(marray))
    plt.subplot(subplotrows, subplotcols, (i+1))  
    bplot = plt.bar(months,monthsdata,color=colors)    
    plt.xticks(rotation=90)
    ax = plt.gca() 
    ymax = 250
    ax.set_ylim((0,ymax))       
    ax.bar_label(bplot,fmt='{:.1f}')
    ax.axhline(mean,ls=':',color='red')    
    ax.set_xmargin(0.01)
    plt.title(f'{ftext}, Mean = {mean:.1f}, median = {mead:.1f}')

medianx = np.zeros(12)
meanx = np.zeros(12)
for i,md in enumerate(mdata):
    a = [e for e in md if e > -1.0]
    x = np.mean(a)
    x2 = np.median(np.sort(a)) 
    meanx[i] = round(x,3)
    medianx[i] = round(x2,3)

plt.subplot(subplotrows, subplotcols, len(csvfiles) + 1 )   
mdplot = plt.bar(months,meanx,color=['#c51162'])
plt.title(f'Mean pr. måned')
plt.xticks(rotation=90)
plt.suptitle('Nedbør mm',fontsize=18)
ax = plt.gca()
ax.bar_label(mdplot,fmt='{:.1f}')
ax.set_xmargin(0.01)
ax.set_ylim((0,100))
afig = plt.gcf()
afig.set_layout_engine('constrained') 
afig.set_figwidth(17)
afig.set_figheight(12) 

plt.subplot(subplotrows, subplotcols, len(csvfiles) + 2 )   
md2plot = plt.bar(months,medianx,color=['#c51162'])
plt.title(f'Median pr. måned')
plt.xticks(rotation=90)
plt.suptitle('Nedbør mm',fontsize=18)
ax = plt.gca()
ax.bar_label(md2plot,fmt='{:.1f}')
ax.set_xmargin(0.01)
ax.set_ylim((0,100))
afig = plt.gcf()
afig.set_layout_engine('constrained') 
afig.set_figwidth(17)
afig.set_figheight(12) 

plt.show()