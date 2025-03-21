import json
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

with open("data.json", "r", encoding="utf-8") as f:
    data = json.loads(f.read())


def get_counts_and_col_names_by_event_type(df: pd.DataFrame, mask, mask_name: str):
    df = df[mask]
    if df.empty:
        return
    field = "camera_name" if "HDD Error" != mask_name else "dvr_name"
    counts = pd.DataFrame(df[field].value_counts().head(10))
    counts[field] = counts.index
    counts.columns = ["errors", field]
    return counts, counts.columns


def get_text_for_title(mask_name, date, chat_name):
    res = ""
    match mask_name:
        case "View Tampering":
            res = "Ошибки Детектора тампера"
        case "HDD Error":
            res = "Ошибки Детектора Проблем с Жестким Диском"
        case "Video Signal Lost":
            res = "Ошибки Детектора Потери Видео"
    res += f"\n{chat_name}"
    res += f"\n{date}"
    return res


def make_graphic(data, mask_name, chat_id, date, chat_name):
    try:
        plt.figure(figsize=(16, 8))

        title = get_text_for_title(
            mask_name=mask_name,
            date=date,
            chat_name=chat_name,
        )
        plt.title(title)
        # mask_name = mask_name.replace(" ", "_")
        counts, column_names = [item for item in data]
        # print(counts, column_names)
        bar = sns.barplot(x=column_names[1], y=column_names[0], data=counts)
        [item.set_rotation(8) for item in bar.get_xticklabels()]

        shot_chat_id = str(chat_id)[-6:]
        short_mask_name = "_".join([item[0] for item in mask_name.split(" ")])

        file_name = f"{shot_chat_id}-{short_mask_name}-{date}.png"

        dst_folder = Path("./statistic/graphs/")
        dst_file = Path(dst_folder, file_name).absolute()

        plt.savefig(dst_file)
        return dst_file
    # statistic graphs
    except Exception as Ex:
        print(Ex)


def make_statistic(data: list[dict], chat_id: int, date, chat_name: str):
    df = pd.DataFrame(data)
    df["event_time"] = pd.to_datetime(df["event_time"], format="%Y-%m-%d %H:%M:%S")

    # * HDD Error, View Tampering, Video Signal Lost
    # * date_mask = df["event_time"] >= "2024-10-26"
    # * df = df[date_mask]

    mask_names = ["View Tampering", "HDD Error", "Video Signal Lost"]

    masks_tuple = [(df["event_type"] == item, item) for item in mask_names]
    files = []
    for df_mask, mask_name in masks_tuple:
        data = get_counts_and_col_names_by_event_type(df, df_mask, mask_name)
        # print(data)
        if not data:
            continue
        graph = make_graphic(data, mask_name, chat_id, date, chat_name)
        files.append(graph)

    return files


# * Надо удалить потом
# tamp_df = df[tamp_mask]
# counts = pd.DataFrame(tamp_df["camera_name"].value_counts().head(10))
# counts["camera_name"] = counts.index
# counts.columns = ["errors", "camera_name"]

# hdd_er_df = df[hdd_er_mask]
# hdd_er_counts = pd.DataFrame(hdd_er_df["dvr_name"].value_counts().head(10))
# hdd_er_counts["dvr_name"] = hdd_er_counts.index
# hdd_er_counts.columns = ["errors", "dvr_name"]

# lost_df = df[lost_mask]
# lost_count = pd.DataFrame(lost_df["camera_name"].value_counts().head(10))
# lost_count["camera_name"] = lost_count.index
# lost_count.columns = ["errors", "camera_name"]


# plt.figure(figsize=(16, 8))
# plt.title("Ошибки Детектора тампера")
# bar = sns.barplot(x="camera_name", y="errors", data=counts)
# [item.set_rotation(8) for item in bar.get_xticklabels()]
# plt.savefig("tamp.png")

# plt.figure(figsize=(16, 8))
# plt.title("Ошибки Детектора Проблем с Жестким Диском")
# bar = sns.barplot(x="dvr_name", y="errors", data=hdd_er_counts)
# [item.set_rotation(8) for item in bar.get_xticklabels()]
# plt.savefig("hdd_err.png")

# plt.figure(figsize=(16, 8))
# plt.title("Ошибки Детектора Потери Видео")
# bar = sns.barplot(x="camera_name", y="errors", data=lost_count)
# [item.set_rotation(8) for item in bar.get_xticklabels()]
# plt.savefig("lost.png")
