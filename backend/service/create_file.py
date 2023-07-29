import os
import datetime
import json


def get_filename() -> str:
    """
    返回当前日期信息
    """
    current_date = datetime.date.today()
    return os.path.join('data', f'{current_date}.json')


def creat_file() -> None:
    """
    创建名为当前日期的JSON文件存储数据
    """
    file_path = get_filename()

    if not os.path.exists(file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump({}, file)
