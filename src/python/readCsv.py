import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys
import math

cvsfile = sys.argv[1] if len(sys.argv)>1 else '2011-2020'

months = np.array(['jan','feb','mar','apr','maj','jun','jul','aug','sep','okt','nov','dec'])

colors = []
for i in range(12):
    colors.append('#448aff')
    
filename = 'n' + cvsfile + '.csv' 
file = "../../data/" + filename
fdata = pd.read_csv(file, delimiter=';', header=None)
fvalues = fdata[1].to_numpy()
data = np.zeros(12)
sum = 0
sumdata = np.zeros(12)
for i,fv in enumerate(fvalues):
    val = 0 if pd.isna(fv) else fv    
    data[i] = float(val)
    sum += float(val)   
    sumdata[i] = sum   
    colors[i] = '#448aff' if val<100 else '#0d47a1'

median = np.mean(data)

plt.subplot(1, 2, 1)   
bplot = plt.bar(months,data,color=colors)    
plt.ylabel("mm")
ax = plt.gca()
ax.axhline(median,ls=':',color='red')
ax.bar_label(bplot,fmt='{:.1f}')
ax.set_xmargin(0.01)
ax.set_ymargin(0.1)
plt.title(f'Nedbør {cvsfile}, Median = {median:.1f}')

plt.subplot(1, 2, 2)
plt.plot(months,sumdata)
plt.ylabel("mm")
plt.title(r'$\sum$' + f' {cvsfile} = {sum:.1f} mm')   

afig = plt.gcf()
afig.set_layout_engine('constrained')
afig.set_figwidth(12)

plt.show()