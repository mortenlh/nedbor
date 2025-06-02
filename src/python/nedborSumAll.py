import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
import modules.myutils as myutils

#csvfiles = ['2011-2020', '2018', '2019','2020','2021','2022','2023','2024']
cvsPath = "../../data/"
csvfiles = myutils.getNedborFiles(cvsPath)
months = np.array(['jan','feb','mar','apr','maj','jun','jul','aug','sep','okt','nov','dec'])

yearTotal = np.zeros(len(csvfiles))
mData = np.zeros( (len(months), len(csvfiles)) )
for j,file in enumerate(csvfiles):
    f = cvsPath + file
    ftext = str(file)[1:-4]
    fdata = pd.read_csv(f, delimiter=';', header=None)
    fvalues = fdata[1].to_numpy()
    sum = 0
    sumdata = np.zeros(12)    
    for i,fv in enumerate(fvalues):
        val = 0 if pd.isna(fv) else fv  
        mval = -1.0 if pd.isna(fv) else float(fv)    
        sum += float(val)        
        sumdata[i] = sum            
        mData[i,j] = mval
    yearTotal[j] = sum
    plt.plot(months, sumdata, label=ftext + ": " + f"{round(sumdata.max(),1):.1f} mm", marker='o')        
    plt.title(r'$\sum$ Nedbør')

sumMonthMean = np.zeros(len(months))
for i,md in enumerate(mData):
    t = [v for v in md if v > -1.0]
    x = np.mean(t)
    sumMonthMean[i] = round(x,3) if i==0 else sumMonthMean[i-1] + round(x,3)
plt.plot(months, sumMonthMean, label="Mean: " + f"{round(sumMonthMean.max(),1):.1f} mm", marker='o',linestyle = 'dotted')

maxNedbor = yearTotal.max()
#print(maxNedbor)
ax = plt.gca()
maxY = 100 + (math.ceil(maxNedbor/100) * 100)
#print(maxY)
ax.set_ylim([0,maxY])
ax.set_yticks(np.arange(0,maxY,100))
ax.legend(shadow=True,fancybox=True)
plt.ylabel("mm")
plt.grid(axis='y')

plt.show()