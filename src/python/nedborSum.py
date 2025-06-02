import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sys

cvsfile = sys.argv[1] if len(sys.argv)>1 else '2011-2020'

months = np.array(['jan','feb','mar','apr','maj','jun','jul','aug','sep','okt','nov','dec'])

filename = 'n' + cvsfile + '.csv' 
file = "../../data/" + filename

fdata = pd.read_csv(file, delimiter=';', header=None)
fvalues = fdata[1].to_numpy()

sumdata = []
sum = 0
for fv in fvalues:
    val = 0 if pd.isna(fv) else fv    
    sum += float(val)
    sumdata.append(sum)

plt.plot(months,sumdata)
plt.ylabel("mm")
plt.title(r'$\sum$ ' + cvsfile + " = " + f"{round(sum,1):.1f} mm")
plt.show()