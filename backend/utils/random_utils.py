import random


def random_int(a: int, b: int) -> int:
    return random.randint(a, b)


def random_float() -> float:
    return random.random()


def random_element(sentence: list) -> str:
    """
    随机选择增强结果的一个元素
    """
    return random.choice(sentence)


def random_strategy(strategy: list) -> list[str]:
    """
    随机选择增强策略
    如果选择的策略方法超过一个则有0.25的概率同时发生两种增强
    """
    if len(strategy) == 1:
        return strategy

    # 是否用两种方法增强同个句子
    rate = random_float()

    if rate < 0.75:
        random_index = random_int(0, len(strategy) - 1)
        return [strategy[random_index]]
    else:
        return random.sample(strategy, 2)
