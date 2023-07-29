from service.create_file import creat_file
from service.data_addition import data_addition
from service.data_augmentation import data_augmentation
from models import Settings


def handle_data(settings: Settings, raw_dialog: list) -> None:
    """
    1. 创建json文件
    2. 数据增强
    3. 添加数据
    """
    creat_file()
    processed_dialog = data_augmentation(settings, raw_dialog)
    data_addition(settings.title, settings.author, processed_dialog)
