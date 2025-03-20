import json
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

with open("data.json", "r", encoding="utf-8") as f:
    data = json.loads(f.read())


df = pd.DataFrame(data)
df["event_time"] = pd.to_datetime(df["event_time"], format="%Y-%m-%d %H:%M:%S")
# print(df)

# HDD Error, View Tampering, Video Signal Lost

# date_mask = df["event_time"] >= "2024-10-26"
# df = df[date_mask]
tamp_mask = df["event_type"] == "View Tampering"
hdd_er_mask = df["event_type"] == "HDD Error"
lost_mask = df["event_type"] == "Video Signal Lost"

tamp_df = df[tamp_mask]
tamp_counts = pd.DataFrame(tamp_df["camera_name"].value_counts().head(10))
tamp_counts["camera_name"] = tamp_counts.index
tamp_counts.columns = ["errors", "camera_name"]

hdd_er_df = df[hdd_er_mask]
hdd_er_counts = pd.DataFrame(hdd_er_df["dvr_name"].value_counts().head(10))
hdd_er_counts["dvr_name"] = hdd_er_counts.index
hdd_er_counts.columns = ["errors", "dvr_name"]

lost_df = df[lost_mask]
lost_count = pd.DataFrame(lost_df["camera_name"].value_counts().head(10))
lost_count["camera_name"] = lost_count.index
lost_count.columns = ["errors", "camera_name"]


plt.figure(figsize=(16, 8))
plt.title("Ошибки Детектора тампера")
bar = sns.barplot(x="camera_name", y="errors", data=tamp_counts)
[item.set_rotation(8) for item in bar.get_xticklabels()]
plt.savefig("tamp.png")


plt.figure(figsize=(16, 8))
plt.title("Ошибки Детектора Проблем с Жестким Диском")
bar = sns.barplot(x="dvr_name", y="errors", data=hdd_er_counts)
[item.set_rotation(8) for item in bar.get_xticklabels()]
plt.savefig("hdd_err.png")

plt.figure(figsize=(16, 8))
plt.title("Ошибки Детектора Потери Видео")
bar = sns.barplot(x="camera_name", y="errors", data=lost_count)
[item.set_rotation(8) for item in bar.get_xticklabels()]
plt.savefig("lost.png")
