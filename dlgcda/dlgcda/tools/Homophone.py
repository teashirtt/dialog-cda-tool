from dlgcda.tools.Basetool import Basetool
from dlgcda.config import homophone_path


class Homophone(Basetool):
    '''
    同音-意字，用于大致不改变原文下，【字级别的】，增强数据
    '''

    def __init__(self, base_file=homophone_path, create_num=5, change_rate=0.05, seed=1):
        super(Homophone, self).__init__(
            base_file, create_num, change_rate, seed)

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
            merge_word = seperate_word + \
                last_line_seperate_word if seperate_word[0][-1] == '2' else seperate_word
            
            # 建立索引
            num = len(seperate_word)
            for i in range(1, num):
                combine_dict[merge_word[i]] = merge_word[1:]
            last_line_seperate_word = seperate_word[1:]
        print('load :%s done' % (self.base_file))
        return combine_dict

    def replace(self, replace_str: str):
        replace_str = replace_str.replace('\n', '').strip()
        words = list(replace_str)
        sentences = [replace_str]
        t = 0
        while len(sentences) < self.create_num:
            t += 1
            a_sentence = ''
            for word in words:
                if word in self.base_file_mapobj and self.random.random() < self.change_rate:
                    wi = self.random.randint(
                        0, len(self.base_file_mapobj[word]) - 1)
                    place = self.base_file_mapobj[word][wi]
                else:
                    place = word
                a_sentence += place
            if a_sentence not in sentences:
                sentences.append(a_sentence)
            if t > self.create_num * self.loop_t / self.change_rate:
                break
        return sentences


def test(test_str, create_num=10000, change_rate=0.3):
    hoe = Homophone(create_num=create_num, change_rate=change_rate)
    try:
        return hoe.replace(test_str)
    except:
        print('error in Homophone.replace')
        return [test_str]


if __name__ == '__main__':
    ts = '''吗是一场疫情防控的人民战争、总体战、阻击战，习近平总书记亲自指挥、亲自部署。运筹帷幄 指挥若定始终把人民群众生命安全和身体健康放在第一位'''
    rs = test(ts)
    ss = set()
    for s in rs:
        # print(s)
        ss.add(s[0])
    print(ss)
