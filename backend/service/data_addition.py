from datetime import datetime
from service.create_file import get_filename
import json


def get_time_key() -> str:
    """
    JSON文件中key为当前时间
    """
    current_time = datetime.now()
    return current_time.strftime("%H:%M:%S")


def json_maker(title: str, author: str, processed_dialog: list) -> dict:
    """
    转为json类型数据
    """
    json_data = {}

    # 如果主题和作者为空就不加入json数据中
    # 作此处理是为了节省空间，如果想保持json数据的一致性可将这段注释掉
    if title.strip():
        json_data['title'] = title
    if author.strip():
        json_data['author'] = author

    dialogs = []
    for dialog in processed_dialog:
        content = []
        for idx in range(0, len(dialog) - 1, 2):
            # idx 为问句 idx+1为答句
            content.append({'Q': dialog[idx], 'A': dialog[idx + 1]})

        dialogs.append(content)

    json_data['data'] = dialogs
    return json_data


def data_addition(title: str, author: str, processed_dialog: list) -> None:
    """
    向文件添加数据
    """
    file_name = get_filename()
    data_key = get_time_key()
    new_data = json_maker(title, author, processed_dialog)

    with open(file_name, 'r+', encoding='utf-8') as f:
        data = json.load(f)

        data.update({
            data_key: new_data
        })
        f.seek(0)
        f.truncate()
        json.dump(data, f, ensure_ascii=False)
