from config import config
import json
from frames import get_frames
class sentence(): # 定义句子类
    def __init__(self, obj) -> None:
        self.sentence_id = obj["sentence_id"] 
        self.cfn_spans = obj["cfn_spans"]
        self.frame = obj["frame"]
        self.target = obj["target"]
        self.text = obj["text"]
        self.word = obj["word"] # list[{},{}]
    
    def get_segmented_text(self): # 获取分好词的句子和对应的词性
        words, labels = [], []
        w_idx_range = []
        # print(self.word, type(self.word))
        index = -1
        for i in self.word:
            # i :{'start': 0, 'end': 1, 'pos': 'nt'}
            start = i['start']
            end = i['end']
            pos = i['pos']
            words.append(self.text[start:end+1])
            labels.append(pos)
            index += 1
            w_idx_range.append([self.text[start:end+1], index, [start, end]])
        # 分好词的句子
        sen = " ".join(words)
        # print(labels)

        return sen, words, labels, w_idx_range

    def get_pred_idx(self): # 返回 ：一个基于分好词计算的下标和谓词
        # print(self.target) # {'start': 6, 'end': 7, 'pos': 'v'}
        idx = []
        start = self.target["start"]
        end = self.target["end"]
        pos = self.target["pos"]
        _,words,_,w_idx_range = self.get_segmented_text()
        for i in w_idx_range:
            if start == i[2][0]:
                idx.append(i[1])
                if end == i[2][1]: #论元找完啦～                     
                    break
                elif end > i[2][1]:
                    continue
                else:
                    print("error!")
            elif end == i[2][1]:
                idx.append(i[1])
        if len(idx) == 1:
            return idx[0], words[idx[0]]
        else:
            print("谓词是片段！")

    def get_cfn_spans(self): # 返回 ：一个分好词的论元id+论元片段，一个没有分好词的论元id+论元片段
        '''
        分好词后的cfn片段
        '''
        # print(type(self.cfn_spans), self.cfn_spans[0]) 
        arg_char_index = [] # 保存的是字的下标
        arg_word_index = []
        _,words,_,w_idx_range = self.get_segmented_text()
        # print(self.text) # 原始文本
        # print(self.word) # 有分词index和pos
        # print(w_idx_range) # [词, 词下标, [原始文本开始index, 原始文本结束index]]
        for element in self.cfn_spans:# 遍历每一个论元
            # print(element)
            start = element['start']
            end = element['end']
            fe_name = element['fe_name']
            fe_abbr = element['fe_abbr']
            arg = []
            for i in w_idx_range:
                if start == i[2][0]:
                    arg.append(i[1])
                    if end == i[2][1]: #论元找完啦～                     
                        break
                    elif end > i[2][1]:
                        continue
                    else:
                        print("error!")
                elif end == i[2][1]:
                    arg.append(i[1])
            # print(arg)
            if len(arg) == 1: # 论元是单个词
                arg_word_index.append([arg[0], arg[0], words[arg[0]], fe_name])
            elif len(arg) ==2: # 论元是多个词
                # print(arg[0],arg[1])
                arg_word_index.append([arg[0], arg[1], " ".join(words[arg[0]:(arg[1]+1)]), fe_name])
            else:
                print("error!")      
            arg_char_index.append([start, end, fe_name])
        # print(arg_char_index) # 没有分词的下标 [[0, 1, '时间'], [3, 8, '赛事名称'], [57, 60, '参赛者'], [61, 64, '差额'], [66, 68, '对手']]
        # print(arg_word_index) # 分好词的下标 [[0, 0, '今天'], [2, 4, '女子 水球 预赛'], [33, 33, '俄罗斯队'], [34, 37, '以 ７ ： ６'], [39, 39, '荷兰队']]
        return arg_word_index, arg_char_index

    def intersect(self, a, b): # 范围是否交叉，不交叉返回0
        return max(0, min(a[1], b[1]) - max(a[0], b[0]))
    
    def check_overlap(self): # 检查该句子中有无重叠的论元
        arg_word_index , _= self.get_cfn_spans()
        for i in range(len(arg_word_index[:-1])):
            for j in range(i+1, len(arg_word_index)):
                # print(arg_word_index[i][:2], arg_word_index[j][:2])
                if self.intersect(arg_word_index[i][:2], arg_word_index[j][:2])!=0: # 有交集
                    return "overlap"
                     
def get_sentences(filepath): # 计算filepath中的全部句子，每个句子用句子类表示
    sentences, dic = [], {}
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
        for s in data:
            sentences.append(sentence(s))
    print("{} total sentences number {}".format(filepath, len(sentences)))
    for i in sentences:
        # 检查句子中的论元是否有重叠
        if "overlap" == i.check_overlap():
            print("Ops，论元有重叠")
        # 检查每个数据集中是否存在重复句子
        if i.text not in dic.keys():
            dic[i] = 0
        else:
            dic[i] += 1
        # 获得谓词的id, 检查谓词是否有span
        i.get_pred_idx()
    print(len(dic),"无重复的句子")


    return sentences

def get_conllu_form(filepath, sentences, type="org"):
    with open(filepath, "w", encoding="utf-8") as f:
        for s in sentences:
            id = 1
            _, words, labels, _ = s.get_segmented_text()
            p_idx, pred = s.get_pred_idx()
            spans, _ = s.get_cfn_spans()
            # 1	The	The	_	DT	_	_	_	7:B-A1	_
            temp_s = {}
            for arg in spans:
                for i in range(len(words)):
                    if arg[0] == i:
                        if arg[0] == arg[1]:
                            temp = "S-"+arg[3]
                            temp_s[i]=[words[i], ":".join([str(p_idx+1),temp])]
                        else:
                            temp = "B-"+arg[3]
                            temp_s[i]=[words[i], ":".join([str(p_idx+1),temp])]
                    elif arg[1] == i :
                        if arg[0] != arg[1]:
                            temp = "E-"+arg[3]
                            temp_s[i]=[words[i], ":".join([str(p_idx+1),temp])]
            for k in range(len(words)):
                if k == int(p_idx):
                    # print(id, words[k], (p_idx+1),"谓词！")
                    if type == "org":
                        temp = ":".join(["0", s.frame])
                    else:
                        temp = ":".join(["0", '[prd]'])
                    f.write("\t".join([str(id),words[k], words[k], "_", labels[k], "_", "_", "_",temp,"_"]))
                    f.write("\n")
                    id += 1
                    continue
                if k in temp_s.keys():
                    # print(id,temp_s[k])
                    f.write("\t".join([str(id),words[k], words[k], "_", labels[k], "_", "_", "_",temp_s[k][1],"_"]))
                    id += 1
                else:
                    # print(id, words[k], "_")
                    f.write("\t".join([str(id),words[k], words[k], "_", labels[k], "_", "_", "_","_","_"]))
                    id += 1
                f.write("\n")
            f.write("\n")
                        

def update_predicate(orig, final, frame2id):
    with open(orig, "r", encoding="utf-8") as o, open(final, "w", encoding="utf-8") as f:
        for line in o:
            if len(line.strip()) != 0:
                if line.split("\t")[8].split(":")[0] == "0":
                    temp = [1,2,3,4,5,6,7,8,9,10]
                    temp[:8] = line.split("\t")[:8]
                    temp[8]  = ":".join(["0",str(frame2id[line.split("\t")[8].split(":")[1]])])
                    temp[9:] = line.split("\t")[9:]
                    # print("\t".join(temp))
                    # exit()
                    f.write("\t".join(temp))
                else:
                    f.write(line)
            else:
                f.write(line)
    

def get_zy_conll(file1, file2):
    with open(file1, "r", encoding="utf-8") as f1, open(file2, "w", encoding="utf-8") as f2:
        flag, temp_i = 0, ""
        for line in f1:
            if len(line.strip()) != 0:
                temp = line.strip().split("\t")[8]
                if temp != "_":
                    if temp != "0:[prd]":
                        if temp.split(":")[1].split("-")[0] == "S":
                            label = "".join([temp.split(":")[0], ":", "B-", temp.split(":")[1].split("-")[1]])
                            f2.write("\t".join(["\t".join(line.strip().split("\t")[:8]), label, "\t".join(line.strip().split("\t")[9:])]))
                            f2.write("\n")
                        elif temp.split(":")[1].split("-")[0] == "B":
                            flag = 1
                            temp_i = "".join([temp.split(":")[0], ":", "I-", temp.split(":")[1].split("-")[1]])
                            f2.write(line)
                        elif temp.split(":")[1].split("-")[0] == "E":
                            flag = 0
                            temp_i = "".join([temp.split(":")[0], ":", "I-", temp.split(":")[1].split("-")[1]])
                            f2.write("\t".join(["\t".join(line.strip().split("\t")[:8]), temp_i, "\t".join(line.strip().split("\t")[9:])]))
                            f2.write("\n")
                    else:                          
                        f2.write(line)
                else:
                    if flag == 0:
                        f2.write(line)
                    else:
                        f2.write("\t".join(["\t".join(line.strip().split("\t")[:8]), temp_i, "\t".join(line.strip().split("\t")[9:])]))
                        f2.write("\n")  
            
            else:
                f2.write(line)

def get_zy_task123(file1, file2):
    with open(file1, "r", encoding="utf-8") as f1, open(file2, "w", encoding="utf-8") as f2:
        flag, temp_i = 0, ""
        for line in f1:
            if len(line.strip()) != 0:
                temp = line.strip().split("\t")[8] # 15:S-认知者
                if temp != "_":
                    if str.isdigit(temp.split("0:")[-1]) == False:
                        if temp.split(":")[1].split("-")[0] == "S":
                            label = "".join([temp.split(":")[0], ":", "B-", temp.split(":")[1].split("-")[1]])
                            f2.write("\t".join(["\t".join(line.strip().split("\t")[:8]), label, "\t".join(line.strip().split("\t")[9:])]))
                            f2.write("\n")
                        elif temp.split(":")[1].split("-")[0] == "B":
                            flag = 1
                            temp_i = "".join([temp.split(":")[0], ":", "I-", temp.split(":")[1].split("-")[1]])
                            f2.write(line)
                        elif temp.split(":")[1].split("-")[0] == "E":
                            flag = 0
                            temp_i = "".join([temp.split(":")[0], ":", "I-", temp.split(":")[1].split("-")[1]])
                            f2.write("\t".join(["\t".join(line.strip().split("\t")[:8]), temp_i, "\t".join(line.strip().split("\t")[9:])]))
                            f2.write("\n")
                    else:                          
                        f2.write(line)
                else:
                    if flag == 0:
                        f2.write(line)
                    else:
                        f2.write("\t".join(["\t".join(line.strip().split("\t")[:8]), temp_i, "\t".join(line.strip().split("\t")[9:])]))
                        f2.write("\n")  
            
            else:
                f2.write(line)


if __name__=="__main__":

    # 获取task1的训练数据和开发数据
    train_s = get_sentences(config["train"])
    get_conllu_form(config["train_v1"], train_s)
    dev_s = get_sentences(config["dev"])
    get_conllu_form(config["dev_v1"], dev_s)
    _, frame2id, _ = get_frames(config["frame_info"])
    update_predicate(config["train_v1"], config["train_v2"], frame2id)
    update_predicate(config["dev_v1"], config["dev_v2"], frame2id)

    # 获取task2/3的训练数据和开发数据
    get_zy_task123(config["train_v2"], config["zy_train_final"])
    get_zy_task123(config["dev_v2"], config["zy_dev_final"])

    # 获取评测数据
    testB_s = get_sentences(config["testB"])
    get_conllu_form(config["testB_v1_p"], testB_s,  type="0:[prd]")


