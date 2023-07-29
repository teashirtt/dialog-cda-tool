import dlgcda
from utils.random_utils import random_element


class Augmentation:
    """
    数据增强方法类
    """

    def __init__(self, sentence: str, change_rate: float):
        self.sentence = sentence
        self.change_rate = change_rate
        self.create_num = 3

    def random_word(self) -> str:
        """
        实体替换
        """
        smw = dlgcda.Randomword(
            create_num=self.create_num, change_rate=self.change_rate)
        res = smw.replace(self.sentence)
        return random_element(res)

    def similar_word(self) -> str:
        """
        同义词替换
        """
        smw = dlgcda.Similarword(
            create_num=self.create_num, change_rate=self.change_rate)
        res = smw.replace(self.sentence)
        return random_element(res)

    def homophone(self) -> str:
        """
        同音字替换
        """
        smw = dlgcda.Homophone(create_num=self.create_num,
                               change_rate=self.change_rate)
        res = smw.replace(self.sentence)
        return random_element(res)

    def random_delete_char(self) -> str:
        """
        随机字删除
        """
        smw = dlgcda.Homophone(create_num=self.create_num,
                               change_rate=self.change_rate)
        res = smw.replace(self.sentence)
        return random_element(res)

    def char_position_exchange(self) -> str:
        """
        随机置换邻近字
        """
        smw = dlgcda.CharPositionExchange(
            create_num=self.create_num, change_rate=self.change_rate)
        res = smw.replace(self.sentence)
        return random_element(res)

    def equivalent_char(self) -> str:
        """
        等价字替换
        """
        smw = dlgcda.EquivalentChar(
            create_num=self.create_num, change_rate=self.change_rate)
        res = smw.replace(self.sentence)
        return random_element(res)
