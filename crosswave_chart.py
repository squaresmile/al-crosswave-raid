import os
import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import register_matplotlib_converters

os.chdir("/home/cereal/al/crosswave-raid")

DATA = "parsed_hp.csv"

df = pd.read_csv(DATA, parse_dates=[0])
df = df.dropna()
x = df["Pacific Time"].tolist()
y = df["HP"].tolist()
register_matplotlib_converters()
plt.style.use('seaborn')
fig, ax = plt.subplots(figsize=(14, 7.5))
ax.plot(x, y, marker='o', markersize=3, linestyle="None")
fig.autofmt_xdate()
ax.set_title(f"AL EN Avrora Crosswave raid - updated {x[-1]:%Y-%m-%d %H:%M} PDT")
ax.set_xlabel("Pacific Daylight Time")
ax.set_ylabel("HP (percent)")
fig.savefig("hp_chart.png", dpi=200, bbox_inches='tight')

avg_rate = -(df.iloc[-1, 1] - df.iloc[0, 1])/ (df.iloc[-1, 0] - df.iloc[0, 0]).total_seconds()
total_run_time = df.iloc[0, 1] / avg_rate
total_run_time = pd.to_timedelta(total_run_time, unit="s")
eta = df.iloc[0, 0] + total_run_time
with open("eta.txt", "w") as eta_file:
    eta_file.write(f"{eta:%Y-%m-%d %H:%M:%S} PDT")

fig, ax = plt.subplots(figsize=(14, 7.5))
x = df.iloc[1:, 0]
y = df["HP"].diff()[1:] / df["Pacific Time"].diff().dt.total_seconds()[1:]
y = -y * 3600
print(x[y<0])
#x = x[y>0]
#y = y[y>0]
ax.plot(x, y, marker=".", linestyle="None")
fig.autofmt_xdate()
ax.set_title(f"AL EN Avrora Crosswave raid DPS - updated {df.iloc[-1,0]:%Y-%m-%d %H:%M} PDT")
ax.set_xlabel("Pacific Daylight Time")
ax.set_ylabel("DPS (percent/hour)")
fig.savefig("dps_chart.png", dpi=200, bbox_inches='tight')

df = df[df["HP"].diff() < -0.4]

x = df["Pacific Time"].tolist()
update_time = x[-1]
y = df["HP"].tolist()
register_matplotlib_converters()
plt.style.use('seaborn')
fig, ax = plt.subplots(figsize=(14, 7.5))
ax.plot(x, y, marker='o', markersize=3)#, linestyle="None")
fig.autofmt_xdate()
ax.set_title(f"AL EN Avrora Crosswave raid - updated {update_time:%Y-%m-%d %H:%M} PDT")
ax.set_xlabel("Pacific Daylight Time")
ax.set_ylabel("HP (percent)")
fig.savefig("hp_chart_significant.png", dpi=200, bbox_inches='tight')

fig, ax = plt.subplots(figsize=(14, 7.5))
x = df.iloc[1:, 0]
y = df["HP"].diff()[1:] / df["Pacific Time"].diff().dt.total_seconds()[1:]
y = -y * 3600
ax.plot(x, y, marker=".")#, linestyle="None")
fig.autofmt_xdate()
ax.set_title(f"AL EN Avrora Crosswave raid DPS - updated {update_time:%Y-%m-%d %H:%M} PDT")
ax.set_xlabel("Pacific Daylight Time")
ax.set_ylabel("DPS (percent/hour)")
fig.savefig("dps_chart_significant.png", dpi=200, bbox_inches='tight')
