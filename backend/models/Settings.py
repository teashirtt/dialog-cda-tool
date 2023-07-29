from pydantic import BaseModel


class Settings(BaseModel):
    """
    用户设置规则类
    """
    title: str
    author: str
    maxTurns: int
    enable: bool
    scope: str
    strategy: list
    count: int
    changeRate: float
    firstAugmentation: bool
