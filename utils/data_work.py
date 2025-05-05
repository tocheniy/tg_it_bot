import json
import logging
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from arq import Retry

from general.schemas import StatSch

logger = logging.getLogger("data_work")
logger.setLevel(logging.DEBUG)
# Настройка консольного вывода
console_handler = logging.StreamHandler()
# Форматтер для логов
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)


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


def search_file(dst_file: Path | str):
    dst_file = Path(dst_file).absolute()
    if not dst_file.exists():
        return None
    return dst_file


def make_graphic(data, mask_name, chat_id, date, chat_name):
    try:
        fig = plt.figure(figsize=(16, 8))

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
        plt.close(fig)
        return dst_file
    # statistic graphs
    except Exception as Ex:
        logger.error(f"Ошибка при создании изображения: {Ex}")
        return None


def make_statistic(
    data: list[dict], chat_id: int, date, chat_name: str
) -> list[StatSch | None]:
    if not data or len(data) == 0:
        return []

    df = pd.DataFrame(data)
    if df.empty:
        return []

    df["event_time"] = pd.to_datetime(df["event_time"], format="%Y-%m-%d %H:%M:%S")

    # * HDD Error, View Tampering, Video Signal Lost
    # * date_mask = df["event_time"] >= "2024-10-26"
    # * df = df[date_mask]

    mask_names = ["View Tampering", "HDD Error", "Video Signal Lost"]

    masks_tuple = [(df["event_type"] == item, item) for item in mask_names]
    # files = []
    res = []
    for df_mask, mask_name in masks_tuple:
        data_for_graph = get_counts_and_col_names_by_event_type(df, df_mask, mask_name)
        # print(data)
        if not data_for_graph:
            continue
        # print(mask_name)
        # events_count = data_for_graph[0]["errors"].sum()
        events_count = data_for_graph[0]["errors"].sum()
        # print(events_count)
        # return
        graph_dst = make_graphic(data_for_graph, mask_name, chat_id, date, chat_name)
        find_file = search_file(dst_file=graph_dst)
        if not find_file:
            logger.warning(f"Файл {graph_dst} не найден")
            continue
        # files.append(graph)
        res.append(
            StatSch(
                file_name=graph_dst,
                event_type=mask_name,
                count=events_count,
                data=data_for_graph[0]["errors"].head(5).to_string(),
            )
        )
    # print(res)
    return res
    # return files
