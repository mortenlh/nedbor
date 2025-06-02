import matplotlib.pyplot as plt
import modules.nedborUtils as nedborutils

path = "../../data/"
nbu = nedborutils.NedborUtil(path)
df = nbu.nedborDataframe()
columns = df.columns

p2011_2020 = df.iloc[1:11] #2011 til 2020, jan til dec
p2011_2020_min = p2011_2020.min().to_numpy()
p2011_2020_max = p2011_2020.max().to_numpy()
p2011_2020_mean = p2011_2020.mean().to_numpy()

p2021_2024 = df.iloc[11:15] #2021 til 2024, jan til dec
#print(p2021_2024)
p2021_2024_min = p2021_2024.min().to_numpy()
p2021_2024_max = p2021_2024.max().to_numpy()
p2021_2024_mean = p2021_2024.mean().to_numpy()

plt.plot(p2011_2020.columns,p2011_2020_min)
plt.plot(p2011_2020.columns,p2011_2020_max)
plt.plot(p2011_2020.columns,p2011_2020_mean,linestyle='dotted')
plt.fill_between(p2011_2020.columns,p2011_2020_min,p2011_2020_max, alpha=0.2)

plt.plot(p2021_2024.columns,p2021_2024_min)
plt.plot(p2021_2024.columns,p2021_2024_max)
plt.plot(p2021_2024.columns,p2021_2024_mean,linestyle='dashed')
plt.fill_between(p2021_2024.columns,p2021_2024_min,p2021_2024_max, alpha=0.2)

plt.xticks(rotation=45)

df["min"] = df[columns].min(axis=1)
df["max"] = df[columns].max(axis=1)

plt.title(f'Min:{df["min"].min():.1f} mm, Max:{df["max"].max():.1f} mm')
#plt.gca().axhline(df["min"].min(),color="red")
#plt.gca().axhline(df["max"].max(),color="purple")

plt.gca().set_ylim(0,df["max"].max() + 10)

df["total"] = df[columns].sum(axis=1)

df.to_json(path+"alldata.json",orient="index")
df[columns].describe().to_json(path+"alldatainfo.json",orient="columns")

plt.show()