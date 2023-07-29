from models.Settings import Settings
from models.Augmentation import Augmentation
from utils.random_utils import random_strategy

field_map = {
    'homoPhones': {
        'run': Augmentation.homophone,
        'description': '同音字替换'
    },
    'equivalentChar': {
        'run': Augmentation.equivalent_char,
        'description': '等价字替换'
    },
    'characterDelete': {
        'run': Augmentation.random_delete_char,
        'description': '随机字删除'
    },
    'characterExchange': {
        'run': Augmentation.char_position_exchange,
        'description': '邻近字换序'
    },
    'similarWord': {
        'run': Augmentation.similar_word,
        'description': '同义词替换'
    },
    'randomWord': {
        'run': Augmentation.random_word,
        'description': '实体词替换'
    }
}


def data_augmentation(settings: Settings, raw_dialog: list) -> list[str]:
    """
    数据增强
    """
    processed_dialog = [raw_dialog]

    if settings.firstAugmentation and len(raw_dialog) > 2:
        processed_dialog.append(raw_dialog[:2])

    if not settings.enable:
        return processed_dialog

    for _ in range(settings.count):
        dialog = raw_dialog.copy()
        step = 2 if settings.scope == 'question' else 1

        for j in range(0, len(dialog), step):
            strategy = random_strategy(settings.strategy)
            for s in strategy:
                d = Augmentation(dialog[j], settings.changeRate)
                dialog[j] = field_map[s]['run'](d)

        processed_dialog.append(dialog)

    return processed_dialog
