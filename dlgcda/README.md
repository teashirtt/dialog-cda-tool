# Dialog Chinese Data Augmentation

本项目在[nlpcda: 一键中文数据增强包](https://github.com/425776024/nlpcda)的基础上，针对`构建中文对话数据集`的领域，进行了数据更新以及模块调整

请先了解原项目的使用方法 [nlpcda/README.md](https://github.com/425776024/nlpcda/blob/master/README.md)

---


## 使用

- 安装

```
python setup.py install
```

- 使用

`dlgcda`中的`Homophone`, `RandomDeleteChar`, `Randomword`, `Similarword`, `CharPositionExchange`, `EquivalentChar`模块与`nlpcda`对应模块使用方法相同


## 主要改动

`dlgcda`相比于`nlpcda`对于中文对话数据增强领域更具针对性，但在其他领域可能存在一定局限性，请根据实际情况进行选择和调整

### 1.同音字数据清洗

删除了绝大部分中文对话不会用到的生僻字以及繁体字

- 这将会极大减少训练时的模型规模
- 几乎不会影响对话模型的泛化性能

### 2.优化同音字建立索引的模式

在对同音字的数据清洗的基础上，根据同音字的使用频率将其分为两组

```
# 原来
yao	要	药	咬	腰	妖	姚	摇	邀	遥	舀	瑶	耀	尧	窑	曜	谣	夭	杳	钥	肴	鹞	窈

# 现在
yao1	要	药	咬	腰	妖	姚	摇	邀	遥
yao2	舀	瑶	耀	尧	窑	曜	谣	夭	杳	钥	肴	鹞	窈
```

同音字中排在上面A组是常用字集合，B组是相较于A频率较少的字的集合

原有的建立索引方式为对于同音字相互建立索引，时间复杂度为 $O(n^2)$

```python
def load_paser_base_file(self):
        combine_dict = {}
        for line in open(self.base_file, "r", encoding='utf-8'):
            seperate_word = line.strip().split("\t")
            num = len(seperate_word)
            for i in range(1, num):
                combine_dict[seperate_word[i]] = seperate_word[1:]
        return combine_dict
```

现在建立索引的方式为A组相互建立索引，B组与A组相互建立索引，时间复杂度为 $O(n_a^2+(n_a+n_b)^2),n=n_a+n_b$

```python
    def load_paser_base_file(self):
        combine_dict = {}
        '''
        这里新增一个trick，同音字按照使用频率分为两组，常用字组A以及不常用字组B
        
        由于用户习惯：不常用字打错的概率远大于常用字打错的概率
        （比如 “那个人叫王伟” 错打成 “那个人叫王韦” 的概率 要远大于 “你为什么要这样” 错打成 “你未什么要这样” 的概率）
        
        我们想要增加模型对生僻字打错成常用字的泛化能力，同时降低对常用字的混淆
        这里将A组内部生成 combine_dict（降低对常用字的混淆），B组与A组合并进行生成 combine_dict（增加模型对生僻字打错成常用字的泛化能力）
        这样做会更加贴合错字逻辑，并且会缩减 combine_dict 的空间和时间复杂度
        '''

        # 这里记录上一行的内容，如果这一行的标记头是以 “2” 结尾的，就要与上一行做拼接操作
        last_line_seperate_word = []
        for line in open(self.base_file, "r", encoding='utf-8'):
            seperate_word = line.strip().split("\t")
            merge_word = seperate_word + last_line_seperate_word if seperate_word[0][-1] == '2' else seperate_word
            num = len(seperate_word)
            for i in range(1, num):
                combine_dict[merge_word[i]] = merge_word[1:]
            last_line_seperate_word = seperate_word[1:]
        return combine_dict
```

- 这将降低对常用字的混淆，并增加模型对生僻字打错成常用字的泛化能力
- 缩减建立索引的时空复杂度

### 3.暂时移除SIMBERT模块

暂时移除`nlpcda`中的`SIMBERT相似句生成`模块

- 这是出于对`dlgcda`轻量性的考虑
- 这将会在一定程度上影响数据增强的质量
- 会在下个版本通过调用接口的方式补充进来

### 4.删除翻译模块

删除了`nlpcda`中的翻译模块

- 这是出于原模块需要用户自行配置`ApiKey`的缘故
- 如需增强模型对中英文的翻译能力，可使用相关数据集进行训练，比如[iwslt2017 · Datasets at Hugging Face](https://huggingface.co/datasets/iwslt2017/viewer/iwslt2017-zh-en/train)

### 5.删除NER模块

删除了`nlpcda`中的`NER`模块

- 这将几乎不会对于数据集的构建产生影响


## 其余改动

- 新增部分等价字

- 删除少量等价词

## 维护计划

- 恢复`SIMBERT相似句生成`模块

- 新增`同音词`模块

- 新增`近音字`模块
